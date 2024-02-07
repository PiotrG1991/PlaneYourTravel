import pytest
from django.utils import timezone
from mixer.backend.django import mixer
from travel_app.models import Destination, Travel

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