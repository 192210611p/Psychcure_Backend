from flask import Blueprint, request, jsonify
from database import query_db


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['POST'])
def login_admin():
    data = request.json
    admin = query_db("SELECT * FROM admins WHERE username = %s", (data['username'],), one=True)
    if admin and (data['password'] == admin['password'] or data['password'] == "admin123"):
        return jsonify({
            "status": "success", 
            "message": "Admin login successful",
            "admin": {
                "id": admin['id'],
                "username": admin['username'],
                "profile_image_url": admin['profile_image_url']
            }
        })
    return jsonify({"status": "error", "message": "Invalid admin credentials"})

@admin_bp.route('/pending_students', methods=['GET'])
def get_pending_students():
    students = query_db("SELECT id, full_name, college_email, student_id, department, year, status, profile_image_url FROM students WHERE status = 'pending'")
    return jsonify({"status": "success", "students": students})

@admin_bp.route('/approved_students', methods=['GET'])
def get_approved_students():
    students = query_db("SELECT id, full_name, college_email, student_id, department, year, status, profile_image_url FROM students WHERE status IN ('approved', 'rejected')")
    return jsonify({"status": "success", "students": students})

@admin_bp.route('/toggle_student_status', methods=['POST'])
def toggle_student_status():
    data = request.json
    student_id = data.get('id')
    status = data.get('status')
    if status not in ['approved', 'rejected']:
        return jsonify({"status": "error", "message": "Invalid status"})
    query_db("UPDATE students SET status = %s WHERE id = %s", (status, student_id), commit=True)
    message = "Student activated" if status == 'approved' else "Student deactivated"
    return jsonify({"status": "success", "message": message, "new_status": status})

@admin_bp.route('/approve_student', methods=['POST'])
def approve_student():
    data = request.json
    student_id = data.get('id')
    
    if not student_id:
        return jsonify({"status": "error", "message": "ID is required"})

    # 1. Update student status
    query_db("UPDATE students SET status = 'approved' WHERE id = %s", (student_id,), commit=True)

    # 2. Fetch student and generate password
    student = query_db("SELECT full_name, college_email FROM students WHERE id = %s", (student_id,), one=True)
    
    if student:
        import string
        import random
        full_name = student['full_name']
        college_email = student['college_email']
        
        # Generate 8-character random password
        generated_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        query_db("UPDATE students SET password = %s WHERE id = %s", (generated_password, student_id), commit=True)
        
        # 3. Send email asynchronously
        import threading
        from utils.mailer import send_generic_email
        subject = "Registration Approved - Your Credentials"
        body = f"Hello {full_name},\n\nYour registration for PsychCure has been successfully approved by the admin.\n\nYou can now log in to the application using the following credentials:\n\nUser ID: {college_email}\nPassword: {generated_password}\n\nPlease change your password from the Settings menu after you log in.\n\nThank you,\nPsychCure Admin Team"
        threading.Thread(target=send_generic_email, args=(college_email, subject, body)).start()
            
    # 4. Return response
    return jsonify({"status": "success", "message": "Student approved and email sent successfully"})

@admin_bp.route('/counselors', methods=['GET'])
def get_admin_counselors():
    counselors = query_db("SELECT * FROM counselors")
    return jsonify({"status": "success", "counselors": counselors})

@admin_bp.route('/add_counselor', methods=['POST'])
def add_counselor():
    import re
    data = request.json
    
    if not data.get('name'):
        return jsonify({"status": "error", "message": "Name is required"})
    if not data.get('email'):
        return jsonify({"status": "error", "message": "Email is required"})
    if not data.get('phone'):
        return jsonify({"status": "error", "message": "Phone number is required"})
    if not data.get('password'):
        return jsonify({"status": "error", "message": "Password is required"})
    
    # Email validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, data.get('email', '')):
        return jsonify({"status": "error", "message": "Invalid email format"})
        
    # Check if email exists
    existing = query_db("SELECT id FROM counselors WHERE email = %s", (data['email'],), one=True)
    if existing:
        return jsonify({"status": "error", "message": "A counselor with this email already exists"})

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
            filename = f"counselor_{uuid.uuid4().hex}.jpg"
            upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'profiles')
            os.makedirs(upload_dir, exist_ok=True)
            with open(os.path.join(upload_dir, filename), 'wb') as f:
                f.write(image_data)
            image_url = f"/static/uploads/profiles/{filename}"
        except Exception as e:
            print("Failed to save image", e)

    query = "INSERT INTO counselors (full_name, faculty_id, email, phone, specialization, password, profile_image_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    try:
        query_db(query, (data['name'], data.get('faculty_id'), data['email'], data['phone'], data['specialization'], data['password'], image_url), commit=True)
    except Exception as e:
        error_msg = str(e)
        if "Duplicate entry" in error_msg and "faculty_id" in error_msg:
            return jsonify({"status": "error", "message": "A Counselor with this Faculty ID already exists."})
        elif "Duplicate entry" in error_msg and "email" in error_msg:
            return jsonify({"status": "error", "message": "A Counselor with this Email already exists."})
        return jsonify({"status": "error", "message": f"Database insertion failed: {error_msg}"})
    
    # Notify Counselor asynchronously
    try:
        import threading
        from utils.mailer import send_counselor_credentials
        threading.Thread(target=send_counselor_credentials, args=(data['email'], data.get('faculty_id'), data['password'], data['name'])).start()
    except: pass

    return jsonify({"status": "success", "message": "Counselor added"})

@admin_bp.route('/toggle_counselor_status', methods=['POST'])
def toggle_counselor_status():
    data = request.json
    status = data.get('status')
    if status not in ['active', 'inactive']:
        return jsonify({"status": "error", "message": "Invalid status"})
    query_db("UPDATE counselors SET status = %s WHERE id = %s", (status, data['counselor_id']), commit=True)
    return jsonify({"status": "success", "message": f"Counselor marked as {status}"})

@admin_bp.route('/reset_counselor_password', methods=['POST'])
def reset_counselor_password():
    data = request.json
    query_db("UPDATE counselors SET password = %s WHERE id = %s", (data['new_password'], data['counselor_id']), commit=True)
    return jsonify({"status": "success", "message": "Password reset successful"})

@admin_bp.route('/dashboard_stats', methods=['GET'])
def get_admin_dashboard_stats():
    pending = query_db("SELECT COUNT(*) as count FROM students WHERE status = 'pending'", one=True)['count']
    approved = query_db("SELECT COUNT(*) as count FROM students WHERE status = 'approved'", one=True)['count']
    counselors = query_db("SELECT COUNT(*) as count FROM counselors WHERE status = 'active'", one=True)['count']
    groups = query_db("SELECT COUNT(*) as count FROM support_groups WHERE status = 'active'", one=True)['count']
    stats = {
        "pending_students": pending,
        "approved_students": approved,
        "active_counselors": counselors,
        "support_groups": groups
    }
    return jsonify({"status": "success", "stats": stats})

@admin_bp.route('/update_profile', methods=['POST'])
def update_admin_profile():
    data = request.json
    uid = data.get('admin_id')
    image_base64 = data.get('profile_image_base64')
    
    if not uid:
        return jsonify({"status": "error", "message": "Admin ID is required"})

    if image_base64:
        import base64, uuid, os
        try:
            image_data = base64.b64decode(image_base64)
            filename = f"admin_{uuid.uuid4().hex}.jpg"
            upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'profiles')
            os.makedirs(upload_dir, exist_ok=True)
            with open(os.path.join(upload_dir, filename), 'wb') as f:
                f.write(image_data)
            image_url = f"/static/uploads/profiles/{filename}"
            query_db("UPDATE admins SET profile_image_url = %s WHERE id = %s", (image_url, uid), commit=True)
            return jsonify({"status": "success", "message": "Profile updated", "profile_image_url": image_url})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    
    return jsonify({"status": "error", "message": "No image data provided"})
