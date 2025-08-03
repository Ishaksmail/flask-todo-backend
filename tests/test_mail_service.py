import os

import pytest
from app.services.mail_service import MailService
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def mail_service():
    
    return MailService(
        host=os.getenv("EMAIL_HOST"),
        port=os.getenv("EMAIL_PORT"),
        username=os.getenv("EMAIL_HOST_USER"),
        password=os.getenv("EMAIL_HOST_PASSWORD")
    )

def test_send_email(mail_service):
    result = mail_service.send_email(
        subject="اختبار",
        receivers=["test@example.com"],
        message="هذه رسالة اختبارية"
    )
    assert result is True or False
