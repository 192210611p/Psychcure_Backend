from flask import Blueprint, request, jsonify
from database import query_db

session_request_bp = Blueprint('session_requests', __name__)

@session_request_bp.route('/request_to_join_session', methods=['POST'])
def request_to_join_session():
    data = request.json
    student_id = data.get('student_id')
    session_id = data.get('session_id')
    
    # 1. Insert join request
    try:
        query_db("INSERT INTO session_requests (student_id, session_id, status) VALUES (%s, %s, 'pending')", 
                 (student_id, session_id), commit=True)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to insert request: {str(e)}"}), 400

    # 2. Fetch student details
    student = query_db("SELECT full_name FROM students WHERE id = %s", (student_id,), one=True)
    student_name = student['full_name'] if student else "A student"

    # 3. Fetch counsellor email (Joining sessions with counselors table)
    counselor = query_db("""SELECT c.email FROM counselors c 
                           JOIN sessions s ON s.counselor_id = c.id 
                           WHERE s.id = %s""", (session_id,), one=True)
    counselor_email = counselor['email'] if counselor else None

    # 4. Send notification to counsellor
    if counselor_email:
        try:
            from utils.mailer import send_generic_email
            subject = "New Session Join Request"
            body = f"Hello,\n\nStudent {student_name} has requested to join your session.\n\nPlease review and take action."
            send_generic_email(counselor_email, subject, body)
        except: pass

    return jsonify({"status": "success", "message": "Session request sent to counsellor successfully"})

@session_request_bp.route('/approve_session_request', methods=['POST'])
def approve_session_request():
    data = request.json
    request_id = data.get('request_id')

    # 1. Update request status
    query_db("UPDATE session_requests SET status = 'approved' WHERE id = %s", (request_id,), commit=True)

    # 2. Fetch student_id and session_id
    req_info = query_db("SELECT student_id, session_id FROM session_requests WHERE id = %s", (request_id,), one=True)
    if not req_info:
        return jsonify({"status": "error", "message": "Request not found"}), 404
    
    student_id = req_info['student_id']
    session_id = req_info['session_id']

    # 3. Fetch student email
    student = query_db("SELECT college_email FROM students WHERE id = %s", (student_id,), one=True)
    student_email = student['college_email'] if student else None

    # 4. Fetch session "name" (Mapping session reason to name)
    session = query_db("SELECT reason FROM sessions WHERE id = %s", (session_id,), one=True)
    session_name = session['reason'] if session and session['reason'] else "the counseling session"

    # 5. Send notification to student
    if student_email:
        try:
            from utils.mailer import send_generic_email
            subject = "Session Request Approved"
            body = f"Hello,\n\nYour request to join the session \"{session_name}\" has been approved.\n\nYou can now attend the session.\n\nThank you."
            send_generic_email(student_email, subject, body)
        except: pass

    return jsonify({"status": "success", "message": "Student notified successfully"})
