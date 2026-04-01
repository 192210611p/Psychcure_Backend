from flask import Blueprint, request, jsonify
from database import query_db

notification_bp = Blueprint('notifications', __name__)

@notification_bp.route('/', methods=['GET'])
def get_notifications():
    uid = request.args.get('user_id')
    utype = request.args.get('user_type', 'student')
    notifs = query_db("SELECT * FROM notifications WHERE user_id = %s AND user_type = %s ORDER BY created_at DESC", (uid, utype))
    for n in notifs: n['created_at'] = n['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"status": "success", "notifications": notifs})

@notification_bp.route('/mark_read', methods=['POST'])
def mark_read():
    data = request.json
    query_db("UPDATE notifications SET is_read = 1 WHERE id = %s", (data['notification_id'],), commit=True)
    return jsonify({"status": "success", "message": "Marked as read"})

@notification_bp.route('/send', methods=['POST'])
def send_notification():
    data = request.json
    query = "INSERT INTO notifications (user_id, user_type, title, message) VALUES (%s, %s, %s, %s)"
    query_db(query, (data['user_id'], data['user_type'], data['title'], data['message']), commit=True)
    return jsonify({"status": "success", "message": "Notification sent"})
