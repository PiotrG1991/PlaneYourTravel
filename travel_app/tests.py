from datetime import datetime
import pytest
from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from mixer.auto import mixer

from travel_app.forms import TravelForm, DestinationForm, TuristsPlacesForm, AccommodationForm, Activity2Form, \
    TransportForm, ActivityForm
from travel_app.models import Travel, Destination, Activity, Accommodation
from travel_app.views import AddTransportView, AddDestinationView, AddAccommodationView, AddTuristPlacesView, \
    ActivityListView, AddActivity2View, AddNextDestinationView, EditDestinationView


@pytest.mark.django_db
def test_home_view_status():
    client = Client()
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_view_template():
    client = Client()
    response = client.get(reverse('home'))
    assert 'welcome.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_main_view_template(client):
    response = client.get(reverse('main'))
    assert 'travel_list.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_main_view_filters_by_participants(client):
    Travel.objects.create(title="Family Vacation", participants=4)
    Travel.objects.create(title="Solo Adventure", participants=1)
    response = client.get(reverse('main') + '?q=4')
    assert 'Family Vacation' in response.content.decode()
    assert 'Solo Adventure' not in response.content.decode()


@pytest.mark.django_db
def test_display_activity_form(client):
    user = User.objects.create_user(username='piotr', password='11223')
    client.force_login(user)
    response = client.get(reverse('add_activity'))
    assert response.status_code == 200
    assert 'add_activity.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_submit_valid_activity_form(client):
    user = User.objects.create_user(username='piotr', password='11223')
    client.force_login(user)
    data = {
        'name': 'Test Activity',
        'description': 'This is a test activity.'
    }
    response = client.post(reverse('add_activity'), data)
    assert response.status_code == 302
    assert Activity.objects.filter(name='Test Activity').exists()


@pytest.mark.django_db
def test_AddTravel_1(client):
    response = client.get(reverse('add_travel'))
    assert response.status_code == 200
    assert 'main.html' in [template.name for template in response.templates]
    assert isinstance(response.context['form'], TravelForm)


@pytest.mark.django_db
def test_AddTravel2(client):
    data = {
        'title': 'Travel',
        'start_date': '2024-02-06',
        'end_date': '2024-02-15',
        'participants': 'Andrzej Agnieszka'
    }
    response = client.post(reverse('add_travel'), data)
    assert response.status_code == 302
    assert Travel.objects.filter(title='Travel').exists()


@pytest.mark.django_db
def test_add_transport_get(client):
    travel = Travel.objects.create(title="Test Travel", participants=2)
    response = client.get(reverse('add_transport', kwargs={'travel_id': travel.id}))
    assert response.status_code == 200
    assert 'add_transport.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_add_transport_view_post(client):
    travel = Travel.objects.create(title="Test Travel", participants=2)
    data = {
        'transport_name': 'Bus',
        'transport_description': 'A comfortable bus with AC',
        'transport_cost': 50,
    }
    response = client.post(reverse('add_transport', kwargs={'travel_id': travel.id}), data)
    assert response.status_code == 302
    assert response.url == reverse('add_destination', kwargs={'travel_id': travel.id})


@pytest.mark.django_db
def test_add_destination_view_get(client):
    travel = mixer.blend(Travel)
    response = client.get(reverse('add_destination', kwargs={'travel_id': travel.id}))
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], DestinationForm)
    assert response.context['travel'] == travel


@pytest.mark.django_db
def test_add_destination_view_invalid_post(client):
    travel = mixer.blend(Travel)
    data = {
        'destination_name': '',
        'destination_description': '',
        'start_date': '',
        'end_date': '',
    }
    response = client.post(reverse('add_destination', kwargs={'travel_id': travel.id}), data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors


@pytest.mark.django_db
def test_add_accommodation_view_invalid_post(client):
    travel = mixer.blend(Travel)
    data = {
        'accommodation_name': '',
        'accommodation_description': '',
        'accommodation_address': '',
        'accommodation_cost': '',
    }

    response = client.post(reverse('add_accommodation', kwargs={'travel_id': travel.id}), data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors


@pytest.mark.django_db
def test_accommodation_form_valid():

    form_data = {
        'accommodation_name': 'Test Accommodation',
        'accommodation_description': 'Test description',
        'accommodation_address': 'Test address',
        'price_per_night': 100
    }

    form = AccommodationForm(data=form_data)
    assert form.is_valid() == True


@pytest.mark.django_db
def test_add_turist_places_get():
    travel = Travel.objects.create(title="Test Travel", start_date="2024-01-01", end_date="2024-01-07", participants=2)
    destination = Destination.objects.create(travel=travel)
    factory = RequestFactory()
    request = factory.get('/add_turist_places/{}/'.format(travel.id))
    view = AddTuristPlacesView()
    response = view.get(request, travel_id=travel.id)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_turist_places_post_valid_data():
    travel = Travel.objects.create(title="Test Travel", start_date="2024-01-01", end_date="2024-01-07", participants=2)
    destination = Destination.objects.create(travel=travel)
    factory = RequestFactory()
    request = factory.post('/add_turist_places/{}/'.format(travel.id), {'turists_places_description': 'Test description'})
    view = AddTuristPlacesView()
    response = view.post(request, travel_id=travel.id)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_activity2_get():
    travel = Travel.objects.create(title="Test Travel", start_date="2024-01-01", end_date="2024-01-07", participants=2)
    destination = Destination.objects.create(travel=travel)
    factory = RequestFactory()
    request = factory.get('/add_activity2/{}/'.format(travel.id))
    view = AddActivity2View()
    response = view.get(request, travel_id=travel.id)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_activity2_invalid_form():
    travel = Travel.objects.create(title="Test Travel", start_date="2024-01-01", end_date="2024-01-07", participants=2)
    factory = RequestFactory()
    url = reverse('add_activity2', kwargs={'travel_id': travel.id})
    request = factory.post(url, {})
    view = AddActivity2View()
    response = view.post(request, travel_id=travel.id)
    assert response.status_code == 200


@pytest.mark.django_db
def test_travel_delete_view_post_invalid_travel_id():
    client = Client()
    user = User.objects.create(username='testuser')
    client.force_login(user)
    response = client.post(reverse('travel_delete', kwargs={'travel_id': 999}))  # Nieprawidłowe travel_id
    assert response.status_code == 404


@pytest.mark.django_db
def test_travel_delete_view_invalid_travel_id():
    client = Client()
    user = User.objects.create(username='testuser')
    client.force_login(user)
    response = client.get(reverse('travel_delete', kwargs={'travel_id': 999}))  # Nieprawidłowe travel_id
    assert response.status_code == 404

@pytest.mark.django_db
def test_get_all_travels_view():
    client = Client()
    response = client.get(reverse('all_travel_list'))
    assert response.status_code == 200
    assert 'all_travels' in response.context
    assert len(response.context['all_travels']) == 0


@pytest.mark.django_db
def test_get_all_travels_view_with_data():
    Travel.objects.create(title="Test Travel 1", start_date="2024-01-01", end_date="2024-01-07")
    Travel.objects.create(title="Test Travel 2", start_date="2024-02-01", end_date="2024-02-07")

    client = Client()
    response = client.get(reverse('all_travel_list'))
    assert response.status_code == 200
    assert 'all_travels' in response.context
    assert len(response.context['all_travels']) == 2


@pytest.mark.django_db
def test_get_travel_detail_view():
    travel = Travel.objects.create(title="Test Travel", start_date="2024-01-01", end_date="2024-01-07")
    client = Client()
    response = client.get(reverse('travel_detail', kwargs={'pk': travel.pk}))
    assert response.status_code == 200
    assert 'travel' in response.context
    assert response.context['travel'].title == "Test Travel"


@pytest.mark.django_db
def test_get_travel_detail_view_context():
    travel = Travel.objects.create(title="Test Travel", start_date="2024-01-01", end_date="2024-01-07")
    client = Client()
    response = client.get(reverse('travel_detail', kwargs={'pk': travel.pk}))
    assert response.context['travel'] == travel


@pytest.mark.django_db
def test_get_edit_travel_view():
    travel = Travel.objects.create(title="Test Travel", start_date="2024-01-01", end_date="2024-01-07")
    client = Client()
    response = client.get(reverse('edit_travel', kwargs={'pk': travel.pk}))
    assert response.status_code == 200
    assert 'travel_form' in response.context
    assert response.context['travel_form'].instance == travel


@pytest.mark.django_db
def test_edit_travel_view_context():
    travel = Travel.objects.create(title="Test Travel", start_date="2024-01-01", end_date="2024-01-07")
    client = Client()
    response = client.get(reverse('edit_travel', kwargs={'pk': travel.pk}))
    assert response.context['travel'] == travel


@pytest.mark.django_db
def test_edit_destination_view_post_invalid_data(destination, activity):
    request = RequestFactory().post(
        reverse('edit_destination', kwargs={'pk': destination.pk}),
        data={
            'destination_name': '',  # Empty field
            'destination_description': 'Updated Description',
            'start_date': '2024-01-01',
            'end_date': '2024-01-07',
            'transport-transport_name': 'Updated Transport',
            'transport-transport_description': 'Updated Description',
            'transport-transport_cost': '150.00',
            'accommodation-accommodation_name': 'Updated Accommodation',
            'accommodation-accommodation_description': 'Updated Description',
            'accommodation-accommodation_address': 'Updated Address',
            'accommodation-price_per_night': '250.00',
            'turists_places-turists_places_description': 'Updated Description',
            'activity-activities': [activity.pk],
        }
    )
    response = EditDestinationView.as_view()(request, pk=destination.pk)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_destination_view_post_invalid_activity(destination):
    request = RequestFactory().post(
        reverse('edit_destination', kwargs={'pk': destination.pk}),
        data={
            'destination_name': 'Updated Destination',
            'destination_description': 'Updated Description',
            'start_date': '2024-01-01',
            'end_date': '2024-01-07',
            'transport-transport_name': 'Updated Transport',
            'transport-transport_description': 'Updated Description',
            'transport-transport_cost': '150.00',
            'accommodation-accommodation_name': 'Updated Accommodation',
            'accommodation-accommodation_description': 'Updated Description',
            'accommodation-accommodation_address': 'Updated Address',
            'accommodation-price_per_night': '250.00',
            'turists_places-turists_places_description': 'Updated Description',
            'activity-activities': [],  # No activity selected
        }
    )
    response = EditDestinationView.as_view()(request, pk=destination.pk)
    assert response.status_code == 200

@pytest.mark.django_db
def test_activity_list_view_get():
    user = User.objects.create_user(username='piotr', password='5555')
    Activity.objects.create(name='Activity 1')
    Activity.objects.create(name='Activity 2')

    request = RequestFactory().get(reverse('activity_list'))
    request.user = user
    view = ActivityListView.as_view()
    response = view(request)

    assert response.status_code == 200
    assert 'Activity 1' in response.content.decode()
    assert 'Activity 2' in response.content.decode()


@pytest.mark.django_db
def test_activity_list_view_post():
    user = User.objects.create_user(username='piotr', password='5555')
    activity1 = Activity.objects.create(name='Activity 1')
    activity2 = Activity.objects.create(name='Activity 2')

    request = RequestFactory().post(reverse('activity_list'), {'activity_id': activity1.id})
    request.user = user
    view = ActivityListView.as_view()
    response = view(request)

    assert response.status_code == 302
    assert not Activity.objects.filter(id=activity1.id).exists()
    assert Activity.objects.filter(id=activity2.id).exists()
