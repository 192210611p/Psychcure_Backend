from flask import Flask
from flask_cors import CORS
from routes.student_routes import student_bp
from routes.counselor_routes import counselor_bp
from routes.admin_routes import admin_bp
from routes.group_routes import group_bp
from routes.notification_routes import notification_bp
from routes.session_request_routes import session_request_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(counselor_bp, url_prefix='/counselor')
app.register_blueprint(group_bp, url_prefix='/groups')
app.register_blueprint(notification_bp, url_prefix='/notifications')
app.register_blueprint(session_request_bp, url_prefix='/session_requests')

@app.route('/')
def home():
    return {"message": "MINDCARE API is running", "status": "online"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
