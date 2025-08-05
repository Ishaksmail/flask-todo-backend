import pytest
import os
from app.services.mail_service import MailService

@pytest.mark.integration
def test_send_real_email():
    mail_service = MailService(
        host=os.getenv("EMAIL_HOST"),
        port=int(os.getenv("EMAIL_PORT")),
        username=os.getenv("EMAIL_HOST_USER"),
        password=os.getenv("EMAIL_HOST_PASSWORD")
    )

    result = mail_service.send_email(
        subject="Test Email from Pytest",
        receivers=["your_inbox_email@inbox.mailtrap.io"],
        message="This is a real test email sent via Mailtrap SMTP."
    )

    assert result is True
