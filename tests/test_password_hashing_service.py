import pytest
from app.services.password_hashing_service import PasswordHashingService

@pytest.fixture
def hashing_service():
    return PasswordHashingService(pepper="mysecretpepper")

def test_hash_and_verify_password_success(hashing_service):
    password = "SecurePassword123"
    hashed = hashing_service.hash_password(password)
    
    assert hashed != password  # يجب ألا يكون نفس النص
    assert hashing_service.verify_password(password, hashed) is True

def test_verify_password_failure_wrong_password(hashing_service):
    password = "SecurePassword123"
    hashed = hashing_service.hash_password(password)
    
    assert hashing_service.verify_password("WrongPassword", hashed) is False

def test_verify_password_failure_invalid_hash(hashing_service):
    password = "SecurePassword123"
    invalid_hash = "not_a_real_hash"
    
    assert hashing_service.verify_password(password, invalid_hash) is False
