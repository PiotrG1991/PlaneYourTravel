import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture
def user_data():
    return {'username': 'testuser', 'password': 'testpassword'}

@pytest.fixture
def create_user(db, user_data):
    return User.objects.create_user(**user_data)

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def valid_registration_data():
    return {
        'username': 'testuser',
        'password': 'testpassword',
        're_password': 'testpassword',}