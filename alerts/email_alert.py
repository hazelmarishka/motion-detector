import smtplib
import ssl
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def send_email_alert(
    snapshot_path=None,
    sender_email=None,
    receiver_email=None,
    app_password=None
):

    if not all([
        sender_email,
        receiver_email,
        app_password
    ]):
        print("[EMAIL] Missing credentials")
        return

    subject = "🚨 Motion Detected!"
    body = "Motion detected by your webcam."

    msg = MIMEMultipart()

    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    if snapshot_path and os.path.exists(snapshot_path):

        with open(snapshot_path, "rb") as img_file:

            img = MIMEImage(
                img_file.read(),
                name=os.path.basename(snapshot_path)
            )

            msg.attach(img)

    context = ssl.create_default_context()

    try:

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            context=context
        ) as server:

            server.login(sender_email, app_password)

            server.sendmail(
                sender_email,
                receiver_email,
                msg.as_string()
            )

        print("[EMAIL] Alert sent!")

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")