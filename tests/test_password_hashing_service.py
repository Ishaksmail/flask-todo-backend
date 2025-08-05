import pytest
import bcrypt
from app.services.password_hashing_service import PasswordHashingService
from app.constants.error_messages import ERROR_MESSAGES


@pytest.fixture
def password_service_no_pepper():
    return PasswordHashingService()


@pytest.fixture
def password_service_with_pepper():
    return PasswordHashingService(pepper="mysecretpepper")


def test_hash_password_success(password_service_no_pepper):
    password = "strongpass123"
    hashed = password_service_no_pepper.hash_password(password)

    assert isinstance(hashed, str)
    assert bcrypt.checkpw(password.encode(), hashed.encode())


def test_hash_password_with_pepper(password_service_with_pepper):
    password = "strongpass123"
    hashed = password_service_with_pepper.hash_password(password)

    combined = (password + "mysecretpepper").encode()
    assert bcrypt.checkpw(combined, hashed.encode())


def test_hash_password_invalid_length(password_service_no_pepper):
    with pytest.raises(ValueError) as exc:
        password_service_no_pepper.hash_password("short")
    assert str(exc.value) == ERROR_MESSAGES["INVALID_PASSWORD_LENGTH"]


def test_verify_password_success(password_service_no_pepper):
    password = "strongpass123"
    hashed = password_service_no_pepper.hash_password(password)

    assert password_service_no_pepper.verify_password(password, hashed) is True


def test_verify_password_wrong(password_service_no_pepper):
    password = "strongpass123"
    wrong_password = "wrongpass123"
    hashed = password_service_no_pepper.hash_password(password)

    assert password_service_no_pepper.verify_password(wrong_password, hashed) is False


def test_verify_password_invalid_inputs(password_service_no_pepper):
    with pytest.raises(ValueError) as exc:
        password_service_no_pepper.verify_password("", "")
    assert str(exc.value) == ERROR_MESSAGES["INVALID_PASSWORD_INPUTS"]
