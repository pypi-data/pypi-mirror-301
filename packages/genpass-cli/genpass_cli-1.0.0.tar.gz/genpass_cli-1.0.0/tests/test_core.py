import pytest
from genpass.core import generate_password

def test_password_length():
    """Test if generated password has correct length"""
    length = 16
    password = generate_password(length=length)
    assert len(password) == length

def test_password_characteristics():
    """Test if password contains required characters"""
    password = generate_password(
        length=12,
        use_special=True,
        use_numbers=True,
        use_uppercase=True
    )
    print(f"Password: {password}")
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    assert has_upper, "Password does not contain uppercase letter"
    assert has_lower, "Password does not contain lowercase letter"
    assert has_digit, "Password does not contain digit"
    assert has_special ,"Password does not contain special character"

def test_password_no_special():
    """Test password generation without special characters"""
    password = generate_password(use_special=False)
    has_special = any(not c.isalnum() for c in password)
    assert not has_special

def test_different_passwords():
    """Test if multiple generated passwords are different"""
    passwords = [generate_password() for _ in range(5)]
    assert len(set(passwords)) == 5  # All passwords should be unique
