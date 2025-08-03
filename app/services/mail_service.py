from redmail import EmailSender


class MailService:
    def __init__(self, host: str, port: int, username: str, password: str):
        
        self.email = EmailSender(
            host=host,
            port=port,
            username=username,
            password=password
        )
        self.sender = username

    
    def send_email(self, subject: str, receivers: list, message: str) -> bool:
        try:
            self.email.send(
                subject=subject,
                sender=self.sender,
                receivers=receivers,
                text=message
            )
            return True
        except Exception as e:
            print(f"❌ فشل إرسال البريد: {e}")
            return False
