import smtplib
from email.mime.text import MIMEText
from typing import List
import json
import requests

from ..core.config import get_settings

settings = get_settings()


class NotificationService:
    def __init__(self) -> None:
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.from_email = settings.smtp_from_email
        self.telegram_bot_token = settings.telegram_bot_token
        self.telegram_channel_id = settings.telegram_channel_id

    def send_email(self, recipients: List[str], subject: str, body: str) -> None:
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = self.from_email
        message["To"] = ", ".join(recipients)
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            if self.smtp_username:
                server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.from_email, recipients, message.as_string())

    def send_telegram(self, message: str) -> None:
        if not self.telegram_bot_token or not self.telegram_channel_id:
            return
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {"chat_id": self.telegram_channel_id, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)

    def notify_call(self, call: dict, recipients: List[str]) -> None:
        body = json.dumps(call, indent=2, ensure_ascii=False)
        subject = f"Nueva convocatoria: {call['title']}"
        if recipients:
            self.send_email(recipients, subject, body)
        self.send_telegram(f"Nueva convocatoria disponible: {call['title']} -> {call['source_url']}")
