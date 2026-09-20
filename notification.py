import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

senderEmail = os.getenv("EMAIL_ADDRESS")
receiverEmail = os.getenv("EMAIL_RECEIVER")
appPassword = os.getenv("EMAIL_APP_PASSWORD")

def sendNotification(job):
    msg = EmailMessage()

    msg["Subject"] = f"🚨 New Internship: {job['company']}"
    msg["From"] = senderEmail
    msg["To"] = receiverEmail

    msg.set_content(
        f"""New Internship

Company: {job['company']}
Role: {job['role']}
Location: {job['location']}
Posted: {job['age']}

Apply: {job['applicationURL']}
"""
    )

    msg.add_alternative(
        f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 30px;">
                <div style="max-width: 600px; margin: auto; padding: 28px;">
                    <h2>🚨 New Internship Found</h2>

                    <h1>{job['company']}</h1>
                    <h3>{job['role']}</h3>

                    <p>
                        📍 <strong>Location:</strong> {job['location']}<br>
                        🕒 <strong>Posted:</strong> {job['age']}
                    </p>

                    <a href="{job['applicationURL']}"
                       style="
                           background-color: #111;
                           color: white;
                           padding: 12px 22px;
                           text-decoration: none;
                           border-radius: 7px;
                           font-weight: bold;
                           display: inline-block;
                       ">
                        Apply Now →
                    </a>
                </div>
            </body>
        </html>
        """,
        subtype="html"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(senderEmail, appPassword)
        smtp.send_message(msg)