import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from filter import load_config
import os


def send_report(report_file: str):
    config = load_config()
    email_cfg = config.get("email", {})

    sender = email_cfg.get("sender")
    receiver = email_cfg.get("receiver")
    app_password = email_cfg.get("app_password")

    if not all([sender, receiver, app_password]):
        print("⚠️  Configura la sección 'email' en config.json")
        return

    if not os.path.exists(report_file):
        print(f"⚠️  No se encontró el reporte: {report_file}")
        return

    with open(report_file, "r") as f:
        body = f.read()

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "🤖 Job Hunter — Reporte diario"
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, receiver, msg.as_string())

    print(f"✅ Reporte enviado a {receiver}")