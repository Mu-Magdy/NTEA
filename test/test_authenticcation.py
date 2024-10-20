import pytest
from helper.authentication import authenticate_employee  

def test_correct_credentials():
    result = authenticate_employee('monica00@example.net', '123')
    assert isinstance(result, int)  

def test_incorrect_password():
    result = authenticate_employee('monica00@example.net', 'wrongpassword')
    assert result is False  

def test_user_not_found():
    result = authenticate_employee('nonexistent@example.com', '123')
    assert result == "User not found"  
