import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from mixer.backend.django import mixer
from travel_app.models import Destination, Travel, Activity, TuristsPlaces, Accommodation, Transport


@pytest.fixture
def travel_data():
    return {
        'title': 'Test Travel',
        'start_date': '2024-02-10',
        'end_date': '2024-02-15',
    }

@pytest.fixture
def sample_travel():
    destination = Destination.objects.create(name='Destination', description='Description', start_date=timezone.now(),
                                             end_date=timezone.now())
    return Travel.objects.create(title='Test Travel', start_date=timezone.now(), end_date=timezone.now(),
                                  participants='Test participant', destination=destination)

@pytest.fixture
def sample_travell():
    travel = Travel.objects.create(title='Test Travel', start_date=timezone.now(), end_date=timezone.now(),
                                  participants='Test participant')
    return travel


@pytest.fixture
def sample_destination():
    return mixer.blend('travel_app.Destination')

@pytest.fixture
def user():
    # Tworzenie użytkownika
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def travel(user):
    # Tworzenie podróży
    return Travel.objects.create(title="Test Travel", start_date="2024-01-01", end_date="2024-01-07", participants=2, user=user)


@pytest.fixture
def destination():
    transport = Transport.objects.create(
        transport_name="Test Transport",
        transport_description="Test Description",
        transport_cost=100.00
    )
    accommodation = Accommodation.objects.create(
        accommodation_name="Test Accommodation",
        accommodation_description="Test Description",
        accommodation_address="Test Address",
        price_per_night=200.00
    )
    turists_places = TuristsPlaces.objects.create(
        turists_places_description="Test Description"
    )

    destination = Destination.objects.create(
        destination_name="Test Destination",
        destination_description="Test Description",
        start_date="2024-01-01",
        end_date="2024-01-07",
        transport=transport,
        accommodation=accommodation,
        turists_places=turists_places
    )
    return destination

@pytest.fixture
def activity():
    return Activity.objects.create(name="Test Activity")
