import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration for SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', "shivampestcontrolservices@gmail.com")
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', "kpxqbnkuxdlozugs") 

@app.route('/api/send_email', methods=['POST'])
def send_email():
    data = request.json
    subject = data.get('subject')
    body = data.get('body')
    
    if not subject or not body:
        return jsonify({"status": "error", "message": "Missing subject or body"}), 400

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = SMTP_USERNAME

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, [SMTP_USERNAME], msg.as_string())
        server.quit()
        return jsonify({"status": "success", "message": "Email sent successfully!"})
    except Exception as e:
        print(f"Failed to send email: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
