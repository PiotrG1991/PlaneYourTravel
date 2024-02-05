import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.forms import LoginForm


@pytest.mark.django_db
def test_login_view_get(client):
    response = client.get(reverse('login_view'))
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], LoginForm)


@pytest.mark.django_db
def test_login_view_post(client, create_user, user_data):
    post_data = {'username': user_data['username'], 'password': user_data['password']}
    response = client.post(reverse('login_view'), data=post_data)
    assert response.status_code == 302
    assert response.url == reverse('main')
    user = User.objects.get(username=user_data['username'])
    assert user.is_authenticated


@pytest.mark.django_db
def test_logout_view(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('logout_view'))
    assert response.status_code == 302
    assert response.url == reverse('home')
    response = client.get(reverse('home'))
    assert not response.context['user'].is_authenticated


@pytest.mark.django_db
def test_registration_view(client, valid_registration_data):
    response = client.post(reverse('register_view'), data=valid_registration_data)
    assert response.status_code == 302
    assert response.url == reverse('main')
    assert response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_registration_view_invalid_data(client):
    response = client.post(reverse('register_view'), data={})
    assert response.status_code == 200
    assert 'form' in response.context
    form = response.context['form']
    assert form.errors
    assert 'Wpisano dwa różne hasła' in form.errors['__all__'][0]