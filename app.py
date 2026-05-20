import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')

# Configuration for SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# Fallback to hardcoded credentials if environment variables are not set
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', "shivampestcontrolservices@gmail.com")
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', "kpxqbnkuxdlozugs") 

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    # If the file exists in the directory, serve it
    if os.path.exists(os.path.join(app.static_folder, path)):
        return app.send_static_file(path)
    # If a path is requested without .html, try appending it
    if os.path.exists(os.path.join(app.static_folder, path + '.html')):
        return app.send_static_file(path + '.html')
    # Fallback to 404
    return app.send_static_file('404.html')

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
