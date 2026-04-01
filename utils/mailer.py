import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_approval_email(email, student_id, password, full_name):
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not smtp_user or not smtp_pass:
        print("SMTP credentials not set. Email not sent.")
        print(f"To: {email}")
        print(f"Body: Welcome {full_name}, your ID: {student_id}, password: {password}")
        return False

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email
    msg['Subject'] = "PsychCure Registration Approved"

    body = f"""
    Hello {full_name},

    Your PsychCure registration has been approved by the administration.

    Here are your login credentials:
    Student ID: {student_id}
    Temporary Password: {password}

    You can now log in to the application and start your wellbeing journey.

    Regards,
    PsychCure Administration
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_registration_alert(admin_email, student_name, student_id):
    subject = "New Student Registration Pending Approval"
    body = f"Hello Admin,\n\nA new student, {student_name} (ID: {student_id}), has registered and is waiting for your approval.\n\nPlease log in to the admin dashboard to review the request.\n\nRegards,\nPsychCure System"
    return send_generic_email(admin_email, subject, body)

def send_counselor_credentials(email, faculty_id, password, full_name):
    subject = "PsychCure Counselor Account Created"
    body = f"Hello {full_name},\n\nYour PsychCure Counselor account has been created.\n\nYou can login to the application using the following credentials:\n\nUser ID: {email}\nPassword: {password}\n\nPlease use these to log in through the counselor portal.\n\nRegards,\nPsychCure Administration"
    return send_generic_email(email, subject, body)

def send_password_reset_email(email, code):
    subject = "PsychCure Password Reset"
    body = f"Your password reset code is: {code}\n\nThis code will expire in 10 minutes.\n\nRegards,\nPsychCure Team"
    return send_generic_email(email, subject, body)

def send_session_booking_alert(counselor_email, student_name, date, time):
    subject = "New Counseling Session Booked"
    body = f"Hello,\n\nA new counseling session has been booked by {student_name}.\n\nDate: {date}\nTime: {time}\n\nPlease check your appointments list for details.\n\nRegards,\nPsychCure System"
    return send_generic_email(counselor_email, subject, body)

def send_generic_email(to_email, subject, body):
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not smtp_user or not smtp_pass:
        print(f"SMTP not configured. Mock Email to {to_email}: {subject}")
        print(body)
        return False

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send generic email: {e}")
        return False
