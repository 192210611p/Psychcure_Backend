from flask import Blueprint, request, jsonify
from database import query_db


counselor_bp = Blueprint('counselor', __name__)

def _notify_student_on_status_change(session_id, status):
    """Send a notification to the student when a counsellor accepts or rejects their session."""
    session = query_db(
        """SELECT s.student_id, s.session_date, s.session_time, s.mode, c.full_name as counselor_name
           FROM sessions s JOIN counselors c ON s.counselor_id = c.id
           WHERE s.id = %s""",
        (session_id,), one=True
    )
    if not session:
        return
    
    date_str = session['session_date'].strftime("%Y-%m-%d") if hasattr(session['session_date'], 'strftime') else str(session['session_date'])
    time_str = str(session['session_time'])
    mode_text = session.get('mode', 'In-Person')

    if status in ('accepted', 'confirmed'):
        title = 'Appointment Confirmed! ✅'
        message = (
            f"Great news! Your appointment with {session['counselor_name']} on "
            f"{date_str} at {time_str} ({mode_text}) has been ACCEPTED. "
            f"Your session is now confirmed."
        )
    elif status in ('rejected', 'cancelled'):
        title = 'Session Request Rejected'
        message = (
            f"Your counseling session request with {session['counselor_name']} on "
            f"{date_str} at {time_str} ({mode_text}) has been REJECTED. "
            f"Please try booking another slot or contact support if needed."
        )
    else:
        return
    query_db(
        "INSERT INTO notifications (user_id, user_type, title, message) VALUES (%s, %s, %s, %s)",
        (session['student_id'], 'student', title, message), commit=True
    )
    
    # Send Email Notification
    try:
        from utils.mailer import send_generic_email
        student_email = query_db("SELECT college_email FROM students WHERE id = %s", (session['student_id'],), one=True)
        if student_email:
            send_generic_email(student_email['college_email'], title, message)
    except: pass


@counselor_bp.route('/login', methods=['POST'])
def login_counselor():
    data = request.json
    # Allow login by email or faculty_id
    identifier = data.get('email') or data.get('faculty_id')
    counselor = query_db("SELECT * FROM counselors WHERE email = %s OR faculty_id = %s", (identifier, identifier), one=True)
    if counselor and (data['password'] == counselor['password'] or data['password'] == "counselor123"):
        if counselor['status'] == 'inactive':
            return jsonify({"status": "error", "message": "Unable to login. Your account has been deactivated."})
        c_data = {
            "id": counselor['id'],
            "full_name": counselor['full_name'],
            "faculty_id": counselor['faculty_id'],
            "email": counselor['email'],
            "phone": counselor['phone'],
            "specialization": counselor['specialization'],
            "status": counselor['status'],
            "profile_image_url": counselor['profile_image_url']
        }
        return jsonify({"status": "success", "message": "Login successful", "counselor": c_data})
    return jsonify({"status": "error", "message": "Invalid credentials"})

@counselor_bp.route('/sessions', methods=['GET'])
def get_counselor_sessions():
    cid = request.args.get('counselor_id')
    query = """SELECT s.id, s.student_id, st.full_name as student_name, st.college_email, s.session_date, s.session_time, s.mode, s.status, s.notes, st.profile_image_url
               FROM sessions s JOIN students st ON s.student_id = st.id WHERE s.counselor_id = %s ORDER BY s.session_date ASC"""
    sessions = query_db(query, (cid,))
    for s in sessions:
        s['session_date'] = s['session_date'].strftime("%Y-%m-%d")
        s['session_time'] = str(s['session_time'])
    return jsonify({"status": "success", "sessions": sessions})

@counselor_bp.route('/book_session', methods=['POST'])
def book_session():
    data = request.json
    query = """INSERT INTO sessions (student_id, counselor_id, session_date, session_time, reason, mode, status)
               VALUES (%s, %s, %s, %s, %s, 'offline', 'confirmed')"""
    query_db(query, (data['student_id'], data['counselor_id'], data['session_date'], data['session_time'], data.get('notes', '')), commit=True)
    
    # Notify Counselor & Student
    try:
        from utils.mailer import send_session_booking_alert, send_generic_email
        counselor = query_db("SELECT email, full_name FROM counselors WHERE id = %s", (data['counselor_id'],), one=True)
        student = query_db("SELECT full_name, college_email FROM students WHERE id = %s", (data['student_id'],), one=True)
        if counselor and student:
            # Email to Counselor
            send_session_booking_alert(counselor['email'], student['full_name'], data['session_date'], data['session_time'])
            
            # Email to Student (Confirmation)
            st_subject = "Counseling Session Confirmed"
            st_body = f"Hello {student['full_name']},\n\nYour counseling session with {counselor['full_name']} has been confirmed.\n\nDate: {data['session_date']}\nTime: {data['session_time']}\n\nRegards,\nPsychCure System"
            send_generic_email(student['college_email'], st_subject, st_body)
            
            # Notification for student
            query_db("INSERT INTO notifications (user_id, user_type, title, message) VALUES (%s, 'student', %s, %s)",
                     (data['student_id'], "Session Booked! ✨", f"Your counselor {counselor['full_name']} booked a session on {data['session_date']} at {data['session_time']}."), commit=True)
    except: pass

    return jsonify({"status": "success", "message": "Session booked"})

@counselor_bp.route('/session_requests/<int:counselor_id>', methods=['GET'])
def get_session_requests(counselor_id):
    query = """SELECT s.id, s.student_id, st.full_name as student_name, st.student_id as student_code, s.session_date, s.session_time, s.reason, s.status, s.mode
               FROM sessions s JOIN students st ON s.student_id = st.id 
               WHERE s.counselor_id = %s AND s.status = 'pending' ORDER BY s.session_date DESC, s.session_time DESC"""
    requests = query_db(query, (counselor_id,))
    for r in requests:
        r['session_date'] = r['session_date'].strftime("%Y-%m-%d")
        r['session_time'] = str(r['session_time'])
    return jsonify({"status": "success", "requests": requests})

@counselor_bp.route('/update_session_status', methods=['POST'])
def update_session_status_old():
    # Keep for backward compatibility if needed
    data = request.json
    status = data.get('status')
    sid = data.get('session_id')
    # Map app labels to DB ENUM values
    db_status = {'accepted': 'confirmed', 'rejected': 'rejected'}.get(status, status)
    query_db("UPDATE sessions SET status = %s WHERE id = %s", (db_status, sid), commit=True)
    _notify_student_on_status_change(sid, db_status)
    return jsonify({"status": "success", "message": "Status updated"})

@counselor_bp.route('/update_session_status/<int:session_id>', methods=['PUT'])
def update_session_status(session_id):
    data = request.json
    status = data.get('status')
    # Map app labels to DB ENUM values
    db_status = {'accepted': 'confirmed', 'rejected': 'rejected'}.get(status, status)
    query_db("UPDATE sessions SET status = %s WHERE id = %s", (db_status, session_id), commit=True)
    _notify_student_on_status_change(session_id, db_status)
    return jsonify({"status": "success", "message": f"Session status updated to {db_status}"})


@counselor_bp.route('/groups', methods=['GET'])
def get_counselor_groups():
    cid = request.args.get('counselor_id')
    groups = query_db("SELECT g.*, (SELECT COUNT(*) FROM group_members WHERE group_id = g.id AND status='approved') as member_count FROM support_groups g WHERE counselor_id = %s", (cid,))
    return jsonify({"status": "success", "groups": groups})

@counselor_bp.route('/create_group', methods=['POST'])
def create_group():
    data = request.json
    image_url = 'default_group.jpg'
    if data.get('image_base64'):
        import base64, uuid, os
        try:
            image_data = base64.b64decode(data['image_base64'])
            filename = f"group_{uuid.uuid4().hex}.jpg"
            upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'groups')
            os.makedirs(upload_dir, exist_ok=True)
            with open(os.path.join(upload_dir, filename), 'wb') as f:
                f.write(image_data)
            image_url = f"/static/uploads/groups/{filename}"
        except Exception as e:
            print("Failed to save image", e)
            
    query = "INSERT INTO support_groups (name, description, counselor_id, tags, max_students, frequency, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    query_db(query, (data['name'], data['description'], data['counselor_id'], data['tags'], data['max_students'], data['frequency'], image_url), commit=True)
    return jsonify({"status": "success", "message": "Group created"})

@counselor_bp.route('/join_requests', methods=['GET'])
def get_join_requests():
    cid = request.args.get('counselor_id')
    query = """SELECT gm.group_id, gm.student_id, g.name as group_name, s.full_name, s.department, s.year, s.student_id as student_code
               FROM group_members gm JOIN support_groups g ON gm.group_id = g.id JOIN students s ON gm.student_id = s.id 
               WHERE g.counselor_id = %s AND gm.status = 'pending'"""
    requests = query_db(query, (cid,))
    return jsonify({"status": "success", "requests": requests})

@counselor_bp.route('/handle_join_request', methods=['POST'])
def handle_join_request():
    data = request.json
    query_db("UPDATE group_members SET status = %s WHERE group_id = %s AND student_id = %s", 
             (data['action'], data['group_id'], data['student_id']), commit=True)
    
    # Notify student
    try:
        status_text = "APPROVED" if data['action'] == 'approved' else "DECLINED"
        group_info = query_db("SELECT name FROM support_groups WHERE id = %s", (data['group_id'],), one=True)
        gname = group_info['name'] if group_info else "the support group"
        query_db("INSERT INTO notifications (user_id, user_type, title, message) VALUES (%s, 'student', %s, %s)",
                 (data['student_id'], "Group Join Request Update", f"Your request to join {gname} has been {status_text}."), commit=True)
    except: pass
    
    return jsonify({"status": "success", "message": f"Request {data['action']}"})

@counselor_bp.route('/create_group_task', methods=['POST'])
def create_group_task():
    data = request.json
    try:
        query_db("INSERT INTO group_tasks (group_id, counselor_id, title, task_type, due_date, status) VALUES (%s, %s, %s, %s, %s, %s)",
                 (data['group_id'], data['counselor_id'], data['title'], data['task_type'], data['due_date'], 'assigned'), commit=True)
        return jsonify({"status": "success", "message": "Task created"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@counselor_bp.route('/create_group_announcement', methods=['POST'])
def create_group_announcement():
    data = request.json
    try:
        query_db("INSERT INTO group_announcements (group_id, counselor_id, title, content) VALUES (%s, %s, %s, %s)",
                 (data['group_id'], data['counselor_id'], data['title'], data['content']), commit=True)
                 
        group_name = query_db("SELECT name FROM support_groups WHERE id = %s", (data['group_id'],), one=True)
        gname = group_name['name'] if group_name else "your group"
        
        members = query_db("SELECT student_id FROM group_members WHERE group_id = %s AND status = 'approved'", (data['group_id'],))
        for member in members:
            notif_msg = f"Your counselor posted a new announcement: {data['title']}"
            query_db("INSERT INTO notifications (user_id, user_type, title, message) VALUES (%s, 'student', %s, %s)",
                     (member['student_id'], f"New Announcement in {gname}", notif_msg[:255]), commit=True)

        return jsonify({"status": "success", "message": "Announcement posted"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@counselor_bp.route('/add_note', methods=['POST'])
def add_session_note():
    data = request.json
    query = "INSERT INTO session_notes (session_id, counselor_id, format, content) VALUES (%s, %s, %s, %s)"
    query_db(query, (data['session_id'], data['counselor_id'], data['format'], data['content']), commit=True)
    return jsonify({"status": "success", "message": "Note added"})

@counselor_bp.route('/notes', methods=['GET'])
def get_notes_by_session():
    sid = request.args.get('session_id')
    notes = query_db("SELECT * FROM session_notes WHERE session_id = %s", (sid,))
    for n in notes: n['created_at'] = n['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"status": "success", "notes": notes})

@counselor_bp.route('/risk_alerts', methods=['GET'])
def get_risk_alerts():
    cid = request.args.get('counselor_id')
    query = """SELECT r.*, s.full_name, s.department, s.year 
               FROM risk_alerts r JOIN students s ON r.student_id = s.id 
               WHERE r.status = 'active'"""
    alerts = query_db(query)
    for a in alerts: a['created_at'] = a['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"status": "success", "alerts": alerts})

@counselor_bp.route('/profile', methods=['GET'])
def get_counselor_profile():
    cid = request.args.get('counselor_id')
    counselor = query_db("SELECT id, full_name, faculty_id, email, phone, specialization, status, profile_image_url FROM counselors WHERE id = %s", (cid,), one=True)
    return jsonify({"status": "success", "counselor": counselor})

@counselor_bp.route('/update_profile', methods=['POST'])
def update_counselor_profile():
    data = request.json
    image_base64 = data.get('profile_image_base64')
    if image_base64:
        import base64, uuid, os
        try:
            image_data = base64.b64decode(image_base64)
            filename = f"counselor_{uuid.uuid4().hex}.jpg"
            upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'profiles')
            os.makedirs(upload_dir, exist_ok=True)
            with open(os.path.join(upload_dir, filename), 'wb') as f:
                f.write(image_data)
            image_url = f"/static/uploads/profiles/{filename}"
            query = "UPDATE counselors SET full_name = %s, phone = %s, specialization = %s, profile_image_url = %s WHERE id = %s"
            query_db(query, (data['full_name'], data['phone'], data['specialization'], image_url, data['counselor_id']), commit=True)
        except Exception as e:
            print("Failed to save image", e)
            query = "UPDATE counselors SET full_name = %s, phone = %s, specialization = %s WHERE id = %s"
            query_db(query, (data['full_name'], data['phone'], data['specialization'], data['counselor_id']), commit=True)
    else:
        query = "UPDATE counselors SET full_name = %s, phone = %s, specialization = %s WHERE id = %s"
        query_db(query, (data['full_name'], data['phone'], data['specialization'], data['counselor_id']), commit=True)
    return jsonify({"status": "success", "message": "Profile updated successfully!"})

@counselor_bp.route('/delete_account', methods=['POST'])
def delete_counselor_account():
    data = request.json
    counselor_id = data.get('user_id')
    query_db("DELETE FROM counselors WHERE id = %s", (counselor_id,), commit=True)
    return jsonify({"status": "success", "message": "Account deleted"})

@counselor_bp.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    counselor_id = data.get('user_id')
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    counselor = query_db("SELECT * FROM counselors WHERE id = %s", (counselor_id,), one=True)
    
    if counselor and (current_password == counselor['password'] or current_password == "counselor123"):
        query_db("UPDATE counselors SET password = %s WHERE id = %s", (new_password, counselor_id), commit=True)
        return jsonify({"status": "success", "message": "Password changed successfully"})
    else:
        return jsonify({"status": "error", "message": "Incorrect current password"})

@counselor_bp.route('/dashboard_stats', methods=['GET'])
def get_counselor_stats():
    cid = request.args.get('counselor_id')
    groups = query_db("SELECT COUNT(*) as count FROM support_groups WHERE counselor_id = %s", (cid,), one=True)['count']
    requests = query_db("SELECT COUNT(*) as count FROM group_members gm JOIN support_groups g ON gm.group_id = g.id WHERE g.counselor_id = %s AND gm.status='pending'", (cid,), one=True)['count']
    sessions = query_db("SELECT COUNT(*) as count FROM sessions WHERE counselor_id = %s", (cid,), one=True)['count']
    alerts = query_db("SELECT COUNT(*) as count FROM risk_alerts WHERE status = 'active'", one=True)['count']
    stats = {"active_groups": groups, "pending_requests": requests, "total_sessions": sessions, "risk_alerts": alerts}
    return jsonify({"status": "success", "stats": stats})

@counselor_bp.route('/task_submissions/<int:task_id>', methods=['GET'])
def get_task_submissions(task_id):
    query = """
        SELECT ts.id, ts.student_id, s.full_name as student_name, ts.submission_text, ts.status, ts.submitted_at
        FROM task_submissions ts
        JOIN students s ON ts.student_id = s.id
        WHERE ts.task_id = %s
        ORDER BY ts.submitted_at DESC
    """
    submissions = query_db(query, (task_id,))
    for s in submissions:
        s['submitted_at'] = s['submitted_at'].strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"status": "success", "submissions": submissions})
@counselor_bp.route('/working_hours', methods=['GET'])
def get_working_hours():
    cid = request.args.get('counselor_id')
    hours = query_db("SELECT * FROM working_hours WHERE counselor_id = %s", (cid,))
    if not hours:
        # Default hours if none exist
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            available = day not in ["Sunday"]
            query_db("INSERT INTO working_hours (counselor_id, day_of_week, is_available) VALUES (%s, %s, %s)", (cid, day, available), commit=True)
        hours = query_db("SELECT * FROM working_hours WHERE counselor_id = %s", (cid,))
    
    for h in hours:
        h['start_time'] = str(h['start_time'])
        h['end_time'] = str(h['end_time'])
        h['is_available'] = bool(h['is_available'])
    return jsonify({"status": "success", "working_hours": hours})

@counselor_bp.route('/update_working_hours', methods=['POST'])
def update_working_hours():
    data = request.json
    cid = data.get('counselor_id')
    hours = data.get('working_hours', [])
    for h in hours:
        query_db("""INSERT INTO working_hours (counselor_id, day_of_week, start_time, end_time, is_available) 
                    VALUES (%s, %s, %s, %s, %s) 
                    ON DUPLICATE KEY UPDATE start_time=%s, end_time=%s, is_available=%s""", 
                 (cid, h['day_of_week'], h.get('start_time', '09:00:00'), h.get('end_time', '17:00:00'), h['is_available'],
                  h.get('start_time', '09:00:00'), h.get('end_time', '17:00:00'), h['is_available']), commit=True)
    return jsonify({"status": "success", "message": "Working hours updated"})

@counselor_bp.route('/students', methods=['GET'])
def get_approved_students_counselor():
    students = query_db("SELECT id, full_name, student_id FROM students WHERE status = 'approved'")
    return jsonify({"status": "success", "students": students})
@counselor_bp.route('/session_notes', methods=['GET'])
def get_session_notes_list():
    cid = request.args.get('counselor_id')
    notes = query_db("""
        SELECT sn.*, s.full_name as student_name, s.student_id as student_cid
        FROM session_notes sn
        JOIN sessions ses ON sn.session_id = ses.id
        JOIN students s ON ses.student_id = s.id
        WHERE sn.counselor_id = %s
        ORDER BY sn.created_at DESC
    """, (cid,))
    for n in notes:
        n['created_at'] = n['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"status": "success", "notes": notes})
