from flask import Blueprint, request, jsonify
from database import query_db

group_bp = Blueprint('groups', __name__)

@group_bp.route('/browse', methods=['GET'])
def browse_groups():
    tag = request.args.get('tag', '')
    search = request.args.get('search', '')
    query = """SELECT g.id, g.name, g.description, g.tags, c.full_name as counselor_name, c.profile_image_url as counselor_profile_image_url,
               (SELECT COUNT(*) FROM group_members WHERE group_id = g.id AND status='approved') as member_count, g.max_students, g.image_url
               FROM support_groups g JOIN counselors c ON g.counselor_id = c.id WHERE g.status = 'active'"""
    args = []
    if tag:
        query += " AND g.tags LIKE %s"
        args.append(f"%{tag}%")
    if search:
        query += " AND (g.name LIKE %s OR g.description LIKE %s)"
        args.extend([f"%{search}%", f"%{search}%"])
    groups = query_db(query, tuple(args))
    return jsonify({"status": "success", "groups": groups})

@group_bp.route('/request_join', methods=['POST'])
def request_join():
    data = request.json
    try:
        query_db("INSERT INTO group_members (group_id, student_id, status) VALUES (%s, %s, 'pending')", 
                 (data['group_id'], data['student_id']), commit=True)
        
        # Notify Counselor
        try:
            group_info = query_db("SELECT name, counselor_id FROM support_groups WHERE id = %s", (data['group_id'],), one=True)
            student_info = query_db("SELECT full_name FROM students WHERE id = %s", (data['student_id'],), one=True)
            if group_info and student_info:
                notif_msg = f"Student {student_info['full_name']} is requesting to join in {group_info['name']} group."
                query_db("INSERT INTO notifications (user_id, user_type, title, message) VALUES (%s, 'counselor', %s, %s)",
                         (group_info['counselor_id'], "Group Join Request", notif_msg[:255]), commit=True)
        except: pass

        return jsonify({"status": "success", "message": "Join request submitted"})
    except:
        return jsonify({"status": "error", "message": "Already requested or member"})

@group_bp.route('/my_groups', methods=['GET'])
def get_my_groups():
    sid = request.args.get('student_id')
    query = """SELECT g.id, g.name, g.description, g.tags, gm.status as membership_status, c.full_name as counselor_name, c.profile_image_url as counselor_profile_image_url,
               (SELECT COUNT(*) FROM group_members WHERE group_id = g.id AND status='approved') as member_count, g.image_url
               FROM group_members gm JOIN support_groups g ON gm.group_id = g.id JOIN counselors c ON g.counselor_id = c.id WHERE gm.student_id = %s"""
    groups = query_db(query, (sid,))
    return jsonify({"status": "success", "groups": groups})

@group_bp.route('/details', methods=['GET'])
def get_group_details():
    gid = request.args.get('group_id')
    group = query_db("""SELECT g.id, g.name, g.description, g.tags, c.full_name as counselor_name, c.specialization, g.max_students, g.frequency, c.profile_image_url as counselor_profile_image_url 
                        FROM support_groups g JOIN counselors c ON g.counselor_id = c.id WHERE g.id = %s""", (gid,), one=True)
    members = query_db("""SELECT s.full_name, s.department, s.year, s.profile_image_url FROM group_members gm JOIN students s ON gm.student_id = s.id 
                          WHERE gm.group_id = %s AND gm.status = 'approved'""", (gid,))
    return jsonify({"status": "success", "group": group, "members": members})

@group_bp.route('/leave', methods=['POST'])
def leave_group():
    data = request.json
    try:
        query_db("DELETE FROM group_members WHERE group_id = %s AND student_id = %s", 
                 (data['group_id'], data['student_id']), commit=True)
        return jsonify({"status": "success", "message": "Left the group"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@group_bp.route('/posts', methods=['GET'])
def get_group_posts():
    gid = request.args.get('group_id')
    uid = request.args.get('user_id')
    utype = request.args.get('user_type', 'student')

    query = """
        SELECT gp.id, gp.user_id, gp.user_type, gp.content, gp.is_pinned, gp.created_at,
               CASE 
                   WHEN gp.user_type = 'counselor' THEN (SELECT full_name FROM counselors WHERE id = gp.user_id)
                   ELSE (SELECT full_name FROM students WHERE id = gp.user_id)
               END as author_name,
               CASE 
                   WHEN gp.user_type = 'counselor' THEN (SELECT profile_image_url FROM counselors WHERE id = gp.user_id)
                   ELSE (SELECT profile_image_url FROM students WHERE id = gp.user_id)
               END as author_profile_image_url,
               (SELECT COUNT(*) FROM post_likes WHERE post_id = gp.id) as likes_count,
               (SELECT COUNT(*) FROM post_likes WHERE post_id = gp.id AND user_id = %s AND user_type = %s) as is_liked
        FROM group_posts gp
        WHERE gp.group_id = %s
        ORDER BY gp.is_pinned DESC, gp.created_at DESC
    """
    posts = query_db(query, (uid, utype, gid))
    
    for p in posts:
        p['created_at'] = p['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        # Fetch comments for each post
        p['comments'] = query_db("""
            SELECT pc.id, pc.user_id, pc.user_type, pc.content, pc.created_at,
                   CASE 
                       WHEN pc.user_type = 'counselor' THEN (SELECT full_name FROM counselors WHERE id = pc.user_id)
                       ELSE (SELECT full_name FROM students WHERE id = pc.user_id)
                   END as author_name,
                   CASE 
                       WHEN pc.user_type = 'counselor' THEN (SELECT profile_image_url FROM counselors WHERE id = pc.user_id)
                       ELSE (SELECT profile_image_url FROM students WHERE id = pc.user_id)
                   END as author_profile_image_url
            FROM post_comments pc
            WHERE pc.post_id = %s
            ORDER BY pc.created_at ASC
        """, (p['id'],))
        for c in p['comments']:
            c['created_at'] = c['created_at'].strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({"status": "success", "posts": posts})

@group_bp.route('/create_post', methods=['POST'])
def create_group_post():
    data = request.json
    try:
        query_db("INSERT INTO group_posts (group_id, user_id, user_type, content, is_pinned) VALUES (%s, %s, %s, %s, %s)",
                 (data['group_id'], data['user_id'], data['user_type'], data['content'], data.get('is_pinned', 0)), commit=True)
                 
        if data['user_type'] == 'counselor':
            group_name = query_db("SELECT name FROM support_groups WHERE id = %s", (data['group_id'],), one=True)
            gname = group_name['name'] if group_name else "your group"
            members = query_db("SELECT student_id FROM group_members WHERE group_id = %s AND status = 'approved'", (data['group_id'],))
            for member in members:
                content_preview = data['content'][:200] + "..." if len(data['content']) > 200 else data['content']
                notif_msg = f"Your counselor posted: {content_preview}"
                query_db("INSERT INTO notifications (user_id, user_type, title, message) VALUES (%s, 'student', %s, %s)",
                         (member['student_id'], f"New Post in {gname}", notif_msg[:255]), commit=True)

        return jsonify({"status": "success", "message": "Post created"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@group_bp.route('/like_post', methods=['POST'])
def like_group_post():
    data = request.json
    try:
        # Check if already liked
        existing = query_db("SELECT id FROM post_likes WHERE post_id = %s AND user_id = %s AND user_type = %s",
                            (data['post_id'], data['user_id'], data['user_type']), one=True)
        if existing:
            query_db("DELETE FROM post_likes WHERE id = %s", (existing['id'],), commit=True)
            return jsonify({"status": "success", "message": "Unliked", "action": "unliked"})
        else:
            query_db("INSERT INTO post_likes (post_id, user_id, user_type) VALUES (%s, %s, %s)",
                     (data['post_id'], data['user_id'], data['user_type']), commit=True)
            return jsonify({"status": "success", "message": "Liked", "action": "liked"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@group_bp.route('/comment_post', methods=['POST'])
def comment_group_post():
    data = request.json
    try:
        query_db("INSERT INTO post_comments (post_id, user_id, user_type, content) VALUES (%s, %s, %s, %s)",
                 (data['post_id'], data['user_id'], data['user_type'], data['content']), commit=True)
        return jsonify({"status": "success", "message": "Comment added"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@group_bp.route('/request_to_join_group', methods=['POST'])
def request_to_join_group():
    data = request.json
    student_id = data.get('student_id')
    group_id = data.get('group_id')
    
    # 1. Insert join request
    try:
        query_db("INSERT INTO group_members (student_id, group_id, status) VALUES (%s, %s, 'pending')", 
                 (student_id, group_id), commit=True)
    except:
        return jsonify({"status": "error", "message": "Already requested or member"}), 400

    # 2. Fetch student details
    student = query_db("SELECT full_name FROM students WHERE id = %s", (student_id,), one=True)
    student_name = student['full_name'] if student else "A student"

    # 3. Fetch counsellor email
    counselor = query_db("""SELECT c.email FROM counselors c 
                           JOIN support_groups g ON g.counselor_id = c.id 
                           WHERE g.id = %s""", (group_id,), one=True)
    counselor_email = counselor['email'] if counselor else None

    # 4. Send notification to counsellor
    if counselor_email:
        try:
            from utils.mailer import send_generic_email
            subject = "New Group Join Request"
            body = f"Hello,\n\nStudent {student_name} has requested to join your group.\n\nPlease review and take action."
            send_generic_email(counselor_email, subject, body)
        except: pass

    return jsonify({"status": "success", "message": "Request sent to counsellor successfully"})

@group_bp.route('/approve_group_request', methods=['POST'])
def approve_group_request():
    data = request.json
    request_id = data.get('request_id')

    # 1. Update request status
    query_db("UPDATE group_members SET status = 'approved' WHERE id = %s", (request_id,), commit=True)

    # 2. Fetch student_id, group_id
    member_info = query_db("SELECT student_id, group_id FROM group_members WHERE id = %s", (request_id,), one=True)
    if not member_info:
        return jsonify({"status": "error", "message": "Request not found"}), 404
    
    student_id = member_info['student_id']
    group_id = member_info['group_id']

    # 3. Fetch student email
    student = query_db("SELECT college_email FROM students WHERE id = %s", (student_id,), one=True)
    student_email = student['college_email'] if student else None

    # 4. Fetch group name
    group = query_db("SELECT name FROM support_groups WHERE id = %s", (group_id,), one=True)
    group_name = group['name'] if group else "the group"

    # 5. Send notification to student
    if student_email:
        try:
            from utils.mailer import send_generic_email
            subject = "Group Request Approved"
            body = f"Hello,\n\nYour request to join the group \"{group_name}\" has been approved.\n\nYou can now participate in the group.\n\nThank you."
            send_generic_email(student_email, subject, body)
        except: pass

    return jsonify({"status": "success", "message": "Student notified successfully"})
