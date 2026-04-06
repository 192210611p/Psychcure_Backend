from flask import Blueprint, request, jsonify
from database import query_db

from datetime import datetime, timedelta
import mysql.connector

student_bp = Blueprint('student', __name__)

@student_bp.route('/register', methods=['POST'])
def register_student():
    import re
    data = request.json
    
    if not data.get('name') or not re.match(r'^[a-zA-Z\s]{3,}$', data.get('name', '')):
        return jsonify({"status": "error", "message": "Please enter a valid name (only letters, minimum 3 characters)"})
    
    if not data.get('email'):
        return jsonify({"status": "error", "message": "Email is required"})
    
    # Email validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, data.get('email', '')):
        return jsonify({"status": "error", "message": "Please enter a valid email address"})

    if not data.get('student_id'):
        return jsonify({"status": "error", "message": "Student ID/Registration Number is required"})
    if not data.get('department'):
        return jsonify({"status": "error", "message": "Department is required"})
    if not data.get('year'):
        return jsonify({"status": "error", "message": "Year is required"})
    
    # Phone validation (10 digits)
    phone = data.get('phone', '')
    numeric_phone = "".join(filter(str.isdigit, phone))
    if len(numeric_phone) != 10:
        return jsonify({"status": "error", "message": "Phone number must be exactly 10 digits"})
    
    # Use the cleaned numeric phone for the database
    data['phone'] = numeric_phone

    image_url = 'default_profile.jpg'
    
    image_base64 = data.get('profile_image_base64')
    if image_base64:
        import base64, uuid, os
        try:
            image_data = base64.b64decode(image_base64)
            filename = f"student_{uuid.uuid4().hex}.jpg"
            upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'profiles')
            os.makedirs(upload_dir, exist_ok=True)
            with open(os.path.join(upload_dir, filename), 'wb') as f:
                f.write(image_data)
            image_url = f"/static/uploads/profiles/{filename}"
        except Exception as e:
            print("Failed to save image", e)

    try:
        query = """INSERT INTO students (full_name, college_email, student_id, department, year, phone, password, status, profile_image_url)
                   VALUES (%s, %s, %s, %s, %s, %s, 'nopassword', 'pending', %s)"""
        query_db(query, (data['name'], data['email'], data['student_id'], data['department'], data['year'], data['phone'], image_url), commit=True)
        
        # Notify Admin asynchronously to prevent connection timeouts
        try:
            import threading
            from utils.mailer import send_registration_alert
            admin_email = "admin@psychcure.edu" # Fallback or fetch if admins have email
            threading.Thread(target=send_registration_alert, args=(admin_email, data['name'], data['student_id'])).start()
        except: pass

        return jsonify({"status": "success", "message": "Registration successful. Waiting for admin approval."})
    except mysql.connector.Error as err:
        error_msg = str(err)
        if "Duplicate entry" in error_msg and "college_email" in error_msg:
            return jsonify({"status": "error", "message": "This email is already registered. Please login or use a different email."})
        elif "Duplicate entry" in error_msg and "student_id" in error_msg:
            return jsonify({"status": "error", "message": "This Student ID is already registered."})
        return jsonify({"status": "error", "message": "Registration failed: Duplicate information found or database error."})

@student_bp.route('/login', methods=['POST', 'OPTIONS'], strict_slashes=False)
def login_student():
    if request.method == 'OPTIONS':
        return '', 204
    data = request.json
    email = data.get('email') or data.get('email_id')
    if not email:
        return jsonify({"status": "error", "message": "Email is required"})

    student = query_db("SELECT * FROM students WHERE college_email = %s", (email,), one=True)
    if student:
        if student['status'] != 'approved':
            if student['status'] == 'rejected':
                return jsonify({"status": "error", "message": "Unable to login. Your account has been deactivated."})
            return jsonify({"status": "error", "message": f"Your account is {student['status']}"})
        
        student_data = {
            "id": student['id'],
            "full_name": student['full_name'],
            "college_email": student['college_email'],
            "department": student['department'],
            "status": student['status'],
            "phone": student['phone'],
            "profile_image_url": student['profile_image_url']
        }
        return jsonify({"status": "success", "message": "Login successful", "student": student_data})
    return jsonify({"status": "error", "message": "Invalid college email"})

@student_bp.route('/send_reset_code', methods=['POST'])
def send_reset_code():
    data = request.json
    import random
    code = str(random.randint(100000, 999999))
    expires_at = datetime.now() + timedelta(minutes=10)
    query_db("INSERT INTO password_resets (email, code, expires_at) VALUES (%s, %s, %s)", 
             (data['email'], code, expires_at), commit=True)
    
    # Send actual email
    try:
        from utils.mailer import send_password_reset_email
        send_password_reset_email(data['email'], code)
    except: pass
    
    return jsonify({"status": "success", "message": f"Reset code sent to {data['email']}"})

@student_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    reset = query_db("SELECT * FROM password_resets WHERE email = %s AND code = %s AND expires_at > NOW()", 
                     (data['email'], data['code']), one=True)
    if reset:
        # Check students table first
        student = query_db("SELECT id FROM students WHERE college_email = %s", (data['email'],), one=True)
        if student:
            query_db("UPDATE students SET password = %s WHERE college_email = %s", (data['password'], data['email']), commit=True)
        else:
            # Check counselors table
            counselor = query_db("SELECT id FROM counselors WHERE email = %s", (data['email'],), one=True)
            if counselor:
                query_db("UPDATE counselors SET password = %s WHERE email = %s", (data['password'], data['email']), commit=True)
            else:
                return jsonify({"status": "error", "message": "Email not found in our records"})
        
        query_db("DELETE FROM password_resets WHERE email = %s", (data['email'],), commit=True)
        return jsonify({"status": "success", "message": "Password reset successful"})
    return jsonify({"status": "error", "message": "Invalid or expired reset code"})

@student_bp.route('/checkin', methods=['POST'])
def student_checkin():
    data = request.json
    student_id = data.get('student_id')
    mood = data.get('mood')
    notes = data.get('notes', '')
    
    # New fields for trends
    sleep_hours = data.get('sleep_hours', 7.0)
    stress_level = data.get('stress_level', 5)
    energy_level = data.get('energy_level', 3)
    
    # Save to checkins table
    query_db("INSERT INTO checkins (student_id, mood, notes) VALUES (%s, %s, %s)", 
             (student_id, mood, notes), commit=True)
    
    # Also save to lifestyle table to update wellbeing reports/trends
    query_db("INSERT INTO lifestyle (student_id, sleep_hours, stress_level, mood_score) VALUES (%s, %s, %s, %s)",
             (student_id, sleep_hours, stress_level, energy_level), commit=True)
             
    return jsonify({"status": "success", "message": "Check-in saved and trends updated"})

@student_bp.route('/checkins', methods=['GET'])
def get_student_checkins():
    sid = request.args.get('student_id')
    checkins = query_db("SELECT * FROM checkins WHERE student_id = %s ORDER BY created_at DESC", (sid,))
    for c in checkins: c['created_at'] = c['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"status": "success", "checkins": checkins})

@student_bp.route('/profile', methods=['GET'])
def get_student_profile():
    sid = request.args.get('student_id')
    student = query_db("SELECT id, full_name, college_email, department, status, phone, profile_image_url FROM students WHERE id = %s", (sid,), one=True)
    return jsonify({"status": "success", "student": student})

@student_bp.route('/update_profile', methods=['POST'])
def update_student_profile():
    data = request.json
    image_base64 = data.get('profile_image_base64')
    if image_base64:
        import base64, uuid, os
        try:
            image_data = base64.b64decode(image_base64)
            filename = f"student_{uuid.uuid4().hex}.jpg"
            upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'profiles')
            os.makedirs(upload_dir, exist_ok=True)
            with open(os.path.join(upload_dir, filename), 'wb') as f:
                f.write(image_data)
            image_url = f"/static/uploads/profiles/{filename}"
            query_db("UPDATE students SET full_name = %s, phone = %s, profile_image_url = %s WHERE id = %s", 
                     (data['full_name'], data['phone'], image_url, data['student_id']), commit=True)
        except Exception as e:
            print("Failed to save image", e)
            query_db("UPDATE students SET full_name = %s, phone = %s WHERE id = %s", 
                 (data['full_name'], data['phone'], data['student_id']), commit=True)
    else:
        query_db("UPDATE students SET full_name = %s, phone = %s WHERE id = %s", 
                 (data['full_name'], data['phone'], data['student_id']), commit=True)
    return jsonify({"status": "success", "message": "Profile updated"})

@student_bp.route('/wellbeing_reports', methods=['GET'])
def get_wellbeing_reports():
    sid = request.args.get('student_id')
    
    # Calculate last 7 days for the weekly summary
    today = datetime.now().date()
    start_date = today - timedelta(days=7)
    end_date = today
    
    # Filter by last 7 days
    moods = query_db("SELECT mood, COUNT(*) as count FROM checkins WHERE student_id = %s AND DATE(created_at) BETWEEN %s AND %s GROUP BY mood", (sid, start_date, end_date))
    recent = query_db("SELECT * FROM checkins WHERE student_id = %s AND DATE(created_at) >= %s ORDER BY created_at ASC", (sid, start_date))
    for r in recent: r['created_at'] = r['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    
    # Lifestyle trends for last 7 days
    lifestyle = query_db("SELECT sleep_hours, stress_level, mood_score as energy_level, created_at FROM lifestyle WHERE student_id = %s AND DATE(created_at) >= %s ORDER BY created_at ASC", (sid, start_date))
    for l in lifestyle: l['created_at'] = l['created_at'].strftime("%Y-%m-%d")

    # Lifestyle logs (contains screen time and activity)
    logs = query_db("SELECT sleep_hours, screen_time_before_sleep as screen_time, activity_level, created_at FROM lifestyle_logs WHERE student_id = %s AND DATE(created_at) >= %s ORDER BY created_at ASC", (sid, start_date))
    for l in logs: l['created_at'] = l['created_at'].strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "status": "success", 
        "mood_distribution": moods, 
        "recent": recent,
        "lifestyle_trends": lifestyle,
        "lifestyle_logs": logs,
        "week_start": start_date.strftime("%Y-%m-%d"),
        "week_end": end_date.strftime("%Y-%m-%d")
    })

@student_bp.route('/ai_insight', methods=['POST'])
def get_ai_insight():
    data = request.json
    sid = data.get('student_id')
    # Simple logic to simulate AI insight
    last_lifestyle = query_db("SELECT * FROM lifestyle WHERE student_id = %s ORDER BY created_at DESC LIMIT 1", (sid,), one=True)
    
    if not last_lifestyle:
        return jsonify({"status": "success", "insight": "No data yet. Start tracking your habits to get AI insights!"})
    
    sleep = last_lifestyle['sleep_hours']
    stress = last_lifestyle['stress_level']
    
    if sleep < 6:
        insight = "You've been getting less than 6 hours of sleep. This significantly impacts mood. Try setting a 'no-screen' rule 30 mins before bed."
    elif stress > 7:
        insight = "Your stress levels are high. Consider a 5-minute breathing exercise or booking a session with a counselor."
    else:
        insight = "Your habits look stable. Keep maintaining your routine!"
        
    return jsonify({"status": "success", "insight": insight})

@student_bp.route('/available_counselors', methods=['GET'])
def get_available_counselors():
    counselors = query_db("SELECT id, full_name, specialization, profile_image_url FROM counselors WHERE status = 'active'")
    return jsonify({"status": "success", "counselors": counselors})

@student_bp.route('/book_counselor', methods=['POST'])
def book_counselor():
    data = request.json

    # Map app-side mode labels to DB enum values
    mode_raw = data.get('mode', 'In-Person')
    mode_db = 'offline' if mode_raw in ('In-Person', 'offline') else 'online'

    counselor_id = data.get('counselor_id')
    counselor = query_db("SELECT id, full_name FROM counselors WHERE id = %s", (counselor_id,), one=True)
    if not counselor:
        return jsonify({"status": "error", "message": "Counselor not found"})

    student = query_db("SELECT full_name FROM students WHERE id = %s", (data['student_id'],), one=True)
    student_name = student['full_name'] if student else "A student"

    query = """INSERT INTO sessions (student_id, counselor_id, session_date, session_time, reason, mode, status)
               VALUES (%s, %s, %s, %s, %s, %s, 'pending')"""
    query_db(query, (
        data['student_id'], counselor['id'],
        data['session_date'], data['session_time'],
        data.get('reason', ''), mode_db
    ), commit=True)

    # Get the just-inserted session id
    session_row = query_db(
        "SELECT id FROM sessions WHERE student_id=%s AND counselor_id=%s ORDER BY created_at DESC LIMIT 1",
        (data['student_id'], counselor['id']), one=True
    )
    session_id = session_row['id'] if session_row else None

    # Notify the counsellor
    try:
        notif_msg = f"Student {student_name} is requesting a session on {data['session_date']} at {data['session_time']}. Reason: {data.get('reason', 'N/A')}"
        query_db("INSERT INTO notifications (user_id, user_type, title, message) VALUES (%s, 'counselor', %s, %s)",
                 (counselor['id'], "Session Request", notif_msg[:255]), commit=True)
    except: pass

    return jsonify({"status": "success", "message": "Booking request sent to counsellor. Awaiting approval.", "session_id": session_id})

@student_bp.route('/session_status', methods=['GET'])
def get_session_status():
    """Poll a single session's status so the student knows if the counsellor accepted/rejected."""
    session_id = request.args.get('session_id')
    row = query_db(
        """SELECT s.id, s.status, c.full_name as counselor_name, s.session_date, s.session_time, s.mode
           FROM sessions s JOIN counselors c ON s.counselor_id = c.id
           WHERE s.id = %s""",
        (session_id,), one=True
    )
    if not row:
        return jsonify({"status": "error", "message": "Session not found"})
    row['session_date'] = row['session_date'].strftime("%Y-%m-%d")
    row['session_time'] = str(row['session_time'])
    return jsonify({"status": "success", "session": row})

@student_bp.route('/sessions', methods=['GET'])
def get_student_sessions():
    sid = request.args.get('student_id')
    query = """SELECT s.id, c.full_name as counselor_name, c.specialization, s.session_date, s.session_time, s.status, s.notes, c.profile_image_url
               FROM sessions s JOIN counselors c ON s.counselor_id = c.id WHERE s.student_id = %s ORDER BY s.session_date DESC"""
    sessions = query_db(query, (sid,))
    for s in sessions:
        s['session_date'] = s['session_date'].strftime("%Y-%m-%d")
        s['session_time'] = str(s['session_time'])
    return jsonify({"status": "success", "sessions": sessions})

@student_bp.route('/submit_lifestyle', methods=['POST'])
def submit_lifestyle():
    data = request.json
    query_db("INSERT INTO lifestyle (student_id, sleep_hours, exercise_days, stress_level, mood_score) VALUES (%s, %s, %s, %s, %s)", 
             (data['student_id'], data['sleep_hours'], data['exercise_days'], data['stress_level'], data['mood_score']), commit=True)
    return jsonify({"status": "success", "message": "Lifestyle record saved"})

@student_bp.route('/save_lifestyle_data', methods=['POST'])
def save_lifestyle_data():
    data = request.json
    sid = data.get('student_id')
    sleep = data.get('sleep_hours')
    bedtime = data.get('bedtime')
    screen = data.get('screen_time_before_sleep')
    activity = data.get('activity_level')
    energy = data.get('energy_level')

    try:
        query_db("""INSERT INTO lifestyle_logs 
                    (student_id, sleep_hours, bedtime, screen_time_before_sleep, activity_level, energy_level) 
                    VALUES (%s, %s, %s, %s, %s, %s)""", 
                 (sid, sleep, bedtime, screen, activity, energy), commit=True)
        
        # Also sync to lifestyle table for Trends reporting if sleep or energy/stress is provided
        if sleep is not None:
            # We don't have stress here specifically in this tab, we'll keep previous or default
            query_db("INSERT INTO lifestyle (student_id, sleep_hours, stress_level, mood_score) VALUES (%s, %s, %s, %s)",
                     (sid, sleep, 5, energy if energy else 3), commit=True)
        
        feedback = []
        
        # Sleep Feedback
        if sleep is not None:
            try:
                val = float(sleep)
                if val < 6:
                    feedback.append("You are sleeping less than recommended. Try to get 7–8 hours of sleep.")
                elif 6 <= val < 7:
                    feedback.append("Your sleep is moderate. Try improving your sleep routine.")
                elif 7 <= val <= 9:
                    feedback.append("Great! You are maintaining healthy sleep habits.")
            except: pass
        
        # Screen Time Feedback
        if screen is not None:
            try:
                val = int(screen)
                if val > 120:
                    feedback.append("Your screen time before bed is very high. Try reducing phone usage at night.")
                elif 60 <= val <= 120:
                    feedback.append("Try reducing screen usage before bedtime.")
                elif val < 60:
                    feedback.append("Good job maintaining low screen time before sleep.")
            except: pass
        
        # Activity Feedback
        if activity:
            act_lower = str(activity).lower()
            if "low" in act_lower:
                feedback.append("Your activity level is low today. Try light exercise such as walking.")
            elif "moderate" in act_lower:
                feedback.append("You are maintaining a moderate activity level.")
            elif "high" in act_lower:
                feedback.append("Great job staying active.")

        return jsonify({"status": "success", "message": "Lifestyle monitoring data saved", "feedback": feedback})
    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": str(err)})

@student_bp.route('/generate_exam_plan', methods=['POST'])
def generate_exam_plan():
    data = request.get_json()
    try:
        student_id = data.get('student_id')
        exam_date_str = data.get('exam_date')
        stress_level = int(data.get('stress_level', 0))
        subjects_str = data.get('subjects', '')
        preparation_level = int(data.get('preparation_level', 0))
        study_hours = int(data.get('study_hours', 4))  # New input

        # 1. Date Calculation
        exam_date = datetime.strptime(exam_date_str, '%m/%d/%Y')
        days_left = (exam_date.date() - datetime.now().date()).days
        days_left = max(0, days_left)

        # 2. Dynamic Suggestion Logic (Combined into a Strategy)
        if stress_level >= 8:
            strategy = "Aggressive recovery and targeted study. Priority: Stress reduction."
        elif preparation_level < 40:
            strategy = "Foundation building and summary-based learning."
        elif days_left <= 3:
            strategy = "High-velocity revision and mock testing."
        else:
            strategy = "Balanced mastery and consistent practice."

        # 3. Personalized Schedule Generation
        subj_list = [s.strip() for s in subjects_str.split(',') if s.strip()]
        num_subjects = len(subj_list)
        
        full_plan = []
        if num_subjects > 0:
            # Generate local plan for the next 3 relevant days
            for d in range(1, min(4, days_left + 1)):
                day_tasks = []
                morning_subj = subj_list[(d-1) % num_subjects]
                afternoon_subj = subj_list[d % num_subjects] if num_subjects > 1 else morning_subj
                
                morning_hours = int(study_hours * 0.4)
                afternoon_hours = int(study_hours * 0.4)
                evening_hours = study_hours - morning_hours - afternoon_hours

                day_tasks.append(f"Day {d} Morning ({morning_hours}h): Master {morning_subj} core concepts")
                day_tasks.append(f"Day {d} Afternoon ({afternoon_hours}h): Solve {afternoon_subj} practice set")
                day_tasks.append(f"Day {d} Evening ({evening_hours}h): Review mistakes and {subj_list[0]} formulas")
                
                full_plan.append({"day": d, "tasks": day_tasks})

        # 4. Study Checklist (Behavioral/Health)
        checklist = ["Drink 2L water", "7h sleep", "No social media during study blocks"]
        if stress_level >= 7:
            checklist.append("Take 4-7-8 breathing breaks")

        # 5. Subject Guidance
        subject_guidance = {}
        for subj in subj_list:
            if preparation_level < 50:
                subject_guidance[subj] = f"Need focus on units 1 & 2."
            else:
                subject_guidance[subj] = "Focus on advanced problems."

        # Flatten full_plan for the checklist UI component
        flat_plan = []
        for d_plan in full_plan:
            tasks = d_plan.get('tasks', [])
            if isinstance(tasks, list):
                flat_plan.extend(tasks)

        return jsonify({
            "status": "success",
            "stress_suggestion": strategy,
            "preparation_suggestion": f"Focus on {subj_list[0] if subj_list else 'main subjects'} primarily.",
            "date_suggestion": f"{days_left} days remaining. Every hour counts.",
            "checklist": flat_plan,
            "subject_guidance": subject_guidance
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@student_bp.route('/save_time_management', methods=['POST'])
def save_time_management():
    data = request.get_json()
    try:
        student_id = data.get('student_id')
        classes_per_week = int(data.get('classes_per_week', 20))
        pending_assignments = int(data.get('pending_assignments', 3))
        study_hours_per_day = float(data.get('study_hours_per_day', 4))
        sleep_hours_per_night = float(data.get('sleep_hours_per_night', 7))

        # 1. Productive Efficiency Calculation
        daily_class_avg = classes_per_week / 5.0
        total_commitment = daily_class_avg + study_hours_per_day
        
        if pending_assignments >= 7 or total_commitment > 12:
            status = "High Workload"
            assignment_focus = 0.6  # 60% of study time to assignments
        elif pending_assignments >= 4 or total_commitment > 8:
            status = "Moderate Workload"
            assignment_focus = 0.4
        else:
            status = "Low Workload"
            assignment_focus = 0.2

        # 2. Personalized "Generated" Schedule
        schedule = []
        # Assumption: Standard student day starts at 8 AM
        current_hour = 8
        
        # Morning Block: Classes
        if daily_class_avg > 0:
            cl_hrs = int(daily_class_avg)
            schedule.append({"time": f"{current_hour:02d}:00 - {current_hour+cl_hrs:02d}:00", "task": "University Classes & Lectures"})
            current_hour += cl_hrs + 1 # +1 for lunch/break
        
        # Study Block Split
        assign_time = study_hours_per_day * assignment_focus
        core_study_time = study_hours_per_day - assign_time
        
        if assign_time > 0:
            schedule.append({"time": f"{current_hour:02d}:00 - {current_hour+max(1, int(assign_time)):02d}:00", "task": f"Assignment Focus ({pending_assignments} pending)"})
            current_hour += max(1, int(assign_time))
            
        if core_study_time > 0:
            schedule.append({"time": f"{current_hour:02d}:00 - {current_hour+max(1, int(core_study_time)):02d}:00", "task": "Deep Study/Revision Block"})
            current_hour += max(1, int(core_study_time))
            
        # Night Routine
        bed_t = 24 - int(sleep_hours_per_night)
        if current_hour < bed_t:
            schedule.append({"time": f"{current_hour:02d}:00 - {bed_t:02d}:00", "task": "Relaxation & Prep for Tomorrow"})
        schedule.append({"time": f"{bed_t:02d}:00 onwards", "task": f"Sleep cycle ({sleep_hours_per_night}h objective)"})

        # 3. Dynamic Generated Suggestions
        suggestions = []
        if total_commitment > 14:
            suggestions.append(f"Your total daily commitment ({total_commitment:.1f}h) is very high. Prioritize assignments today.")
        elif study_hours_per_day < (pending_assignments * 0.5):
            suggestions.append(f"With {pending_assignments} assignments, your {study_hours_per_day}h study time is limited.")
            
        if sleep_hours_per_night < 7:
            suggestions.append(f"To stay alert for {classes_per_week}h of classes/week, try to aim for 7.5h of sleep.")
        
        if not suggestions:
            suggestions.append("Your schedule currently shows a very healthy balance.")

        # Save to database
        import json
        query_db("""INSERT INTO time_management_plans 
                    (student_id, classes_per_week, pending_assignments, study_hours_per_day, sleep_hours_per_night, 
                     workload_status, suggestions, schedule) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                 (student_id, classes_per_week, pending_assignments, study_hours_per_day, sleep_hours_per_night,
                  status, json.dumps(suggestions), json.dumps(schedule)), commit=True)

        return jsonify({
            "status": "success",
            "workload_status": status,
            "suggestions": suggestions,
            "schedule": schedule
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@student_bp.route('/ai_first_aid', methods=['POST'])
def ai_first_aid():
    data = request.get_json()
    message = data.get('message', '').lower()
    
    # 1. App Navigation & Features
    if "book" in message or "counselor" in message or "appointment" in message:
        response = "To book a counselor, click 'Book Counselor' on your dashboard. You can see available experts, choose a mode (Online/In-Person), and pick a slot. Your counselor will review and confirm!"
    elif "lifestyle" in message or "track" in message or "sleep" in message or "screen" in message:
        response = "You can monitor your daily habits in the 'Lifestyle Monitor' section. Track your sleep hours, activity levels, and screen time to receive personalized feedback and insights."
    elif "mood" in message or "check-in" in message or "feeling" in message:
        response = "Use the 'Daily Check-in' on your dashboard to log your mood and notes. You can view your emotional trends over time in the 'Wellbeing Reports' section."
    elif "group" in message or "support" in message or "peers" in message:
        response = "PsychCure offers support groups! Browse available groups in 'Support Groups' and request to join. It's a great way to share experiences with fellow students."
    elif "exam" in message or "stress" in message or "study" in message or "academic" in message:
        response = "For academic pressure, check out our 'Academic Stress Tools'. We have a rule-based Exam Stress Plan and a Time Management Planner to help you organize your studies."
    elif "meditation" in message or "breathing" in message or "exercise" in message:
        response = "Visit 'Self-Help Tools' for guided meditations, deep breathing exercises, and night routines designed to help you relax and stay mindful."
    elif "password" in message or "reset" in message:
        response = "If you've forgotten your password, use the 'Forgot Password' link on the login screen. We'll send a 6-digit code to your registered college email."
    elif "profile" in message or "edit" in message or "details" in message:
        response = "You can update your personal details and phone number in the 'Profile' section. Just click on your profile icon and select 'Edit Profile'."
    elif "notification" in message or "alert" in message:
        response = "Stay updated via the 'Notifications' bell icon on your dashboard. You'll get alerts for counselor approvals, group updates, and daily reminders."
        
    # 2. Mental Health Support
    elif "anxious" in message or "anxiety" in message or "panic" in message:
        response = "I'm sorry you're feeling anxious. Try the 4-7-8 breathing exercise in our Self-Help section. If it feels overwhelming, consider booking a quick session with a counselor."
    elif "sad" in message or "depressed" in message or "lonely" in message:
        response = "It's okay to feel this way sometimes. Talking to someone helps—why not join one of our support groups or message a counselor? You don't have to face this alone."
    elif "help" in message or "emergency" in message or "crisis" in message or "danger" in message:
        response = "🚨 EMERGENCY: If you are in immediate distress or danger, please click the 'Emergency Support' (Red Icon) on your dashboard immediately to access 24/7 helpline numbers."
        
    # 3. About the App
    elif "what" in message and "app" in message:
        response = "PsychCure (MINDCARE) is a comprehensive mental health platform for students. We provide counselor booking, mood tracking, lifestyle monitoring, and academic stress management tools."
        
    # Default Response
    else:
        response = "I'm here to help you navigate PsychCure and support your mental wellbeing. You can ask me about booking counselors, tracking lifestyle, exam stress, or joining support groups!"

    return jsonify({
        "status": "success",
        "response": response
    })

@student_bp.route('/group_tasks', methods=['GET'])
def get_group_tasks():
    gid = request.args.get('group_id')
    sid = request.args.get('student_id')
    query = """
        SELECT gt.id, gt.title, gt.task_type, gt.due_date, 
               IFNULL(ts.status, gt.status) as status
        FROM group_tasks gt
        LEFT JOIN task_submissions ts ON ts.task_id = gt.id AND ts.student_id = %s
        WHERE gt.group_id = %s
        ORDER BY gt.created_at DESC
    """
    tasks = query_db(query, (sid, gid))
    return jsonify({"status": "success", "tasks": tasks})

@student_bp.route('/submit_group_task', methods=['POST'])
def submit_group_task():
    data = request.json
    try:
        existing = query_db("SELECT id FROM task_submissions WHERE task_id = %s AND student_id = %s", 
                            (data['task_id'], data['student_id']), one=True)
        if existing:
            query_db("UPDATE task_submissions SET submission_text = %s, status = 'submitted', submitted_at = CURRENT_TIMESTAMP WHERE id = %s",
                     (data['submission_text'], existing['id']), commit=True)
        else:
            query_db("INSERT INTO task_submissions (task_id, student_id, submission_text, status) VALUES (%s, %s, %s, 'submitted')",
                     (data['task_id'], data['student_id'], data['submission_text']), commit=True)
        return jsonify({"status": "success", "message": "Task submitted successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@student_bp.route('/delete_account', methods=['POST'])
def delete_student_account():
    data = request.json
    student_id = data.get('user_id')
    query_db("DELETE FROM students WHERE id = %s", (student_id,), commit=True)
    return jsonify({"status": "success", "message": "Account deleted"})

@student_bp.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    student_id = data.get('user_id')
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    student = query_db("SELECT id FROM students WHERE id = %s AND password = %s", (student_id, current_password), one=True)
    if student:
        query_db("UPDATE students SET password = %s WHERE id = %s", (new_password, student_id), commit=True)
        return jsonify({"status": "success", "message": "Password changed successfully"})
    else:
        return jsonify({"status": "error", "message": "Incorrect current password"})

@student_bp.route('/group_announcements', methods=['GET'])
def get_group_announcements():
    gid = request.args.get('group_id')
    if not gid:
        return jsonify({"status": "error", "message": "Group ID required"}), 400
        
    query = """
        SELECT a.title, a.content, a.created_at as time, c.full_name as author_name
        FROM group_announcements a
        LEFT JOIN counselors c ON a.counselor_id = c.id
        WHERE a.group_id = %s
        ORDER BY a.created_at DESC
    """
    try:
        announcements = query_db(query, (gid,))
        for a in announcements:
            if a['time']:
                a['time'] = a['time'].strftime("%Y-%m-%d %H:%M:%S")
            else:
                a['time'] = "Recent"
        return jsonify({"status": "success", "announcements": announcements})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
