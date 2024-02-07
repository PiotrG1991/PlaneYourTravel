from datetime import datetime
import pytest
from django.contrib.auth.models import User
from django.test import Client, RequestFactory
from django.urls import reverse
from travel_app.forms import TravelForm, DestinationForm, TuristsPlacesForm, AccommodationForm, Activity2Form, \
    TransportForm, ActivityForm
from travel_app.models import Travel, Destination, Activity
from travel_app.views import AddTransportView, AddDestinationView, AddAccommodationView, AddTuristPlacesView, \
    ActivityListView


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
def test_main_view_data(client, travel_data):
    destination = Destination.objects.create(name='Test Destination')
    travel_data['destination_id'] = destination.id
    Travel.objects.create(**travel_data)
    response = client.get(reverse('main'))
    assert travel_data['title'] in response.content.decode()
    start_date = datetime.strptime(travel_data['start_date'], '%Y-%m-%d')
    assert start_date.strftime('%b. %d, %Y') in response.content.decode()
    end_date = datetime.strptime(travel_data['end_date'], '%Y-%m-%d')
    assert end_date.strftime('%b. %d, %Y') in response.content.decode()


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
def test_display_travel_form(client):
    response = client.get(reverse('add_travel'))
    assert response.status_code == 200
    assert 'main.html' in [template.name for template in response.templates]
    assert isinstance(response.context['form'], TravelForm)


@pytest.mark.django_db
def test_submit_valid_travel_form(client):
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
def test_submit_invalid_travel_form(client):
    data = {
        'title': '',
        'start_date': '2024-02-06',
        'end_date': '2024-02-15',
        'participants': 'Andrzej Agnieszka'
    }
    response = client.post(reverse('add_travel'), data)
    assert response.status_code == 200
    assert not Travel.objects.filter(title='Test Travel').exists()


@pytest.mark.django_db
def test_display_transport_form():
    destination = Destination.objects.create(name='Destination', description='Description', start_date=datetime.now(),
                                             end_date=datetime.now())
    travel = Travel.objects.create(title='Travel', start_date=datetime.now(), end_date=datetime.now(),
                                   participants='participants', destination=destination)
    request = RequestFactory().get(reverse('add_transport', kwargs={'travel_id': travel.id}))
    view = AddTransportView()
    response = view.get(request, travel_id=travel.id)
    assert response.status_code == 200


@pytest.mark.django_db
def test_submit_valid_transport_form(sample_travel):
    data = {
        'name': 'Transport',
        'description': 'description',
        'transport_cost': '232320'
    }
    request = RequestFactory().post(reverse('add_transport', kwargs={'travel_id': sample_travel.id}), data)
    view = AddTransportView()
    response = view.post(request, travel_id=sample_travel.id)
    assert response.status_code == 302
    assert response.url == reverse('add_destination', kwargs={'travel_id': sample_travel.id})


@pytest.mark.django_db
def test_display_destination_form(sample_travel):
    request = RequestFactory().get(reverse('add_destination', kwargs={'travel_id': sample_travel.id}))
    view = AddDestinationView()
    response = view.get(request, travel_id=sample_travel.id)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_destination(sample_travel):
    client = Client()
    url = reverse('add_destination', kwargs={'travel_id': sample_travel.id})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], DestinationForm)


@pytest.mark.django_db
def test_display_accommodation_form(sample_travel):
    request = RequestFactory().get(reverse('add_accommodation', kwargs={'travel_id': sample_travel.id}))
    view = AddAccommodationView()
    response = view.get(request, travel_id=sample_travel.id)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_accommodation(sample_travel):
    client = Client()
    url = reverse('add_accommodation', kwargs={'travel_id': sample_travel.id})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AccommodationForm)


@pytest.mark.django_db
def test_addturists_places(sample_travel):
    client = Client()
    url = reverse('add_turists_places', kwargs={'travel_id': sample_travel.id})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], TuristsPlacesForm)


@pytest.mark.django_db
def test_submit_valid_turists_places_form(sample_travel):
    data = {
        'name': 'Tourist Place',
        'description': 'Description of tourist place'
    }
    request = RequestFactory().post(reverse('add_turists_places', kwargs={'travel_id': sample_travel.id}), data)
    view = AddTuristPlacesView()
    response = view.post(request, travel_id=sample_travel.id)

    assert response.status_code == 302  # 302 - Redirect status code
    assert response.url == reverse('add_activity2', kwargs={'travel_id': sample_travel.id})


@pytest.mark.django_db
def test_addactivity2(sample_travel):
    client = Client()
    url = reverse('add_activity2', kwargs={'travel_id': sample_travel.id})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], Activity2Form)


@pytest.mark.django_db
def test_display_activity2_form(sample_travel):
    request = RequestFactory().get(reverse('add_activity2', kwargs={'travel_id': sample_travel.id}))
    view = AddAccommodationView()
    response = view.get(request, travel_id=sample_travel.id)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_travel_delete_view(client, sample_travel):
    response = client.get(reverse('travel_delete', kwargs={'travel_id': sample_travel.id}))
    assert response.status_code == 200
    assert 'travel_delete.html' in [t.name for t in response.templates]
    assert response.context['travel'] == sample_travel


@pytest.mark.django_db
def test_post_travel_delete_view(client, sample_travel):
    response = client.post(reverse('travel_delete', kwargs={'travel_id': sample_travel.id}))
    assert response.status_code == 302
    assert response.url == reverse('main')
    assert not Travel.objects.filter(id=sample_travel.id).exists()


@pytest.mark.django_db
def test_get_all_travels_view():
    client = Client()
    response = client.get(reverse('all_travel_list'))
    assert response.status_code == 200
    assert 'all_travels' in response.context
    assert len(response.context['all_travels']) == 0


@pytest.mark.django_db  #?????
def test_post_all_travels_view():
    client = Client()
    response = client.post(reverse('all_travel_list'), {'travel_id': 1})
    assert response.status_code == 302
    assert response.url == reverse('edit_travel', kwargs={'travel_id': 1})


@pytest.mark.django_db
def test_travel_detail_view(client, sample_travel):
    response = client.get(reverse('travel_detail', kwargs={'pk': sample_travel.id}))
    assert response.status_code == 200
    assert 'travel_detail.html' in [t.name for t in response.templates]
    assert response.context['travel'] == sample_travel


@pytest.mark.django_db  #????
def test_travel_detail_view_with_invalid_id(client):
    response = client.get(reverse('travel_detail', kwargs={'pk': 20}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_edit_travel_view(sample_travel):
    client = Client()
    response = client.get(reverse('edit_travel', kwargs={'pk': sample_travel.pk}))
    assert response.status_code == 200
    assert 'edit_travel.html' in [template.name for template in response.templates]
    assert 'travel_form' in response.context
    assert 'transport_form' in response.context
    assert 'destination_form' in response.context
    assert 'activity_form' in response.context
    assert 'accommodation_form' in response.context
    assert 'turists_places_form' in response.context
    assert 'travel' in response.context
    assert response.context['travel'].title == 'Test Travel'


@pytest.mark.django_db
def test_edit_travel_view():

    destination = Destination.objects.create(name='Testowe miejsce', description='Opis testowego miejsca',
                                             start_date='2024-01-01', end_date='2024-01-10')
    travel = Travel.objects.create(title='Podróż testowa', start_date='2024-01-01', end_date='2024-01-10',
                                   participants=2, destination=destination)

    travel_data = {'title': 'Nowy tytuł', 'start_date': '2024-01-01', 'end_date': '2024-01-10', 'participants': 3}
    transport_data = {'name': 'Nowa nazwa transportu', 'description': 'Nowy opis transportu', 'transport_cost': 150}
    destination_data = {'name': 'Nowe miejsce', 'description': 'Nowy opis miejsca', 'start_date': '2024-01-01',
                        'end_date': '2024-01-10'}
    accommodation_data = {'name': 'Nowe zakwaterowanie', 'description': 'Nowy opis zakwaterowania',
                          'address': 'Nowy adres', 'price_per_night': 75}
    turists_places_data = {'description': 'Nowy opis miejsca turystycznego'}
    activity_data = {'name': 'pływanie'}

    travel_form = TravelForm(data=travel_data, instance=travel)
    transport_form = TransportForm(data=transport_data, instance=destination.transport)
    destination_form = DestinationForm(data=destination_data, instance=destination)
    accommodation_form = AccommodationForm(data=accommodation_data, instance=destination.accommodation)
    turists_places_form = TuristsPlacesForm(data=turists_places_data, instance=destination.turists_places)
    activity_form = ActivityForm(data=activity_data)

    assert travel_form.is_valid()
    assert transport_form.is_valid()
    assert destination_form.is_valid()
    assert accommodation_form.is_valid()
    assert turists_places_form.is_valid()
    assert activity_form.is_valid()


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
