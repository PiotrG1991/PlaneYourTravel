from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView

from travel_app.forms import TravelForm, ActivityForm, TransportForm, DestinationForm, AccommodationForm, \
    TuristsPlacesForm, Activity2Form
from travel_app.models import Travel, Transport, Destination, Activity


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'welcome.html')


class MainView(View):
    model = Travel
    template_name = 'travel_list.html'
    context_object_name = 'latest_travels'
    ordering = ['-created']

    def get(self, request):
        latest_travels = Travel.objects.order_by('-created')[:5]
        context = {'latest_travels': latest_travels}
        return render(request, self.template_name, context)


class AddActivityView(View):
    def get(self, request):
        form = ActivityForm()
        return render(request, 'add_activity.html', {'form': form})

    def post(self, request):
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.save()
            return redirect('add_activity')
        return render(request, 'add_activity.html', {'form': form})


class AddTravelView(View):
    template_name = 'add_travel.html'

    def get(self, request):
        form = TravelForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TravelForm(request.POST)

        if form.is_valid():
            travel = form.save(commit=False)

            # Automatyczne utworzenie nowego obiektu Destination
            destination = Destination.objects.create()

            # Przypisanie destination do obiektu Travel
            travel.destination = destination

            # Pozostałe dane z formularza
            travel.title = form.cleaned_data['title']
            travel.start_date = form.cleaned_data['start_date']
            travel.end_date = form.cleaned_data['end_date']
            travel.participants = form.cleaned_data['participants']

            travel.save()

            # Przekieruj na kolejny etap lub na stronę podsumowania, itp.
            # Przykład: przekieruj na stronę dodawania transportu z przekazaniem travel_id
            return redirect('add_transport', travel_id=travel.id)

        return render(request, self.template_name, {'form': form})


class AddTransportView(View):
    template_name = 'add_transport.html'

    def get(self, request, travel_id):
        travel = Travel.objects.get(id=travel_id)
        form = TransportForm()
        return render(request, self.template_name, {'travel': travel, 'form': form})

    def post(self, request, travel_id):
        travel = Travel.objects.get(id=travel_id)
        form = TransportForm(request.POST)

        if form.is_valid():
            transport = form.save()

            # Utwórz nowy destination i przypisz go do travel
            destination, created = Destination.objects.get_or_create(travel=travel)
            destination.transport = transport
            destination.save()
            # Przekieruj na stronę destination, przekazując travel_id
            return redirect('add_destination', travel_id=travel_id)

        return render(request, self.template_name, {'travel': travel, 'form': form})

class AddDestinationView(View):
    template_name = 'add_destination.html'

    def get(self, request, travel_id):
        travel = Travel.objects.get(id=travel_id)
        form = DestinationForm()
        return render(request, self.template_name, {'travel': travel, 'form': form})

    def post(self, request, travel_id):
        travel = Travel.objects.get(id=travel_id)
        form = DestinationForm(request.POST)

        if form.is_valid():
            # Pobierz lub utwórz destination dla podanego travel_id
            destination, created = Destination.objects.get_or_create(travel=travel)

            # Zaktualizuj dane destination na podstawie formularza
            destination.name = form.cleaned_data['name']
            destination.description = form.cleaned_data['description']
            destination.start_date = form.cleaned_data['start_date']
            destination.end_date = form.cleaned_data['end_date']
            # Dodaj inne pola destination z formularza

            # Zapisz zmiany
            destination.save()

            # Przekieruj na kolejny widok lub strony
            return redirect('add_accommodation', travel_id=travel_id)

        return render(request, self.template_name, {'travel': travel, 'form': form})


class AddAccommodationView(View):
    template_name = 'add_accommodation.html'

    def get(self, request, travel_id):
        travel = Travel.objects.get(id=travel_id)
        form = AccommodationForm()
        return render(request, self.template_name, {'travel': travel, 'form': form})

    def post(self, request, travel_id):
        travel = Travel.objects.get(id=travel_id)
        form = AccommodationForm(request.POST)

        if form.is_valid():
            accommodation = form.save()

            # Pobierz lub utwórz destination dla podanego travel_id
            destination, created = Destination.objects.get_or_create(travel=travel)

            # Zaktualizuj dane destination o accommodation id
            destination.accommodation = accommodation
            destination.save()

            return redirect('add_turists_places', travel_id=travel_id)

        return render(request, self.template_name, {'travel': travel, 'form': form})

class AddTuristPlacesView(View):
    template_name = 'add_turist_places.html'

    def get(self, request, travel_id):
        travel = Travel.objects.get(id=travel_id)
        form = TuristsPlacesForm()
        return render(request, self.template_name, {'travel': travel, 'form': form})

    def post(self, request, travel_id):
        travel = Travel.objects.get(id=travel_id)
        form = TuristsPlacesForm(request.POST)

        if form.is_valid():
            turists_places = form.save()

            # Pobierz lub utwórz destination dla podanego travel_id
            destination, created = Destination.objects.get_or_create(travel=travel)

            # Zaktualizuj dane destination o turists_places id
            destination.turists_places = turists_places
            destination.save()

            return redirect('add_activity2', travel_id=travel_id)

        return render(request, self.template_name, {'travel': travel, 'form': form})


class AddActivity2View(View):
    template_name = 'add_activity2.html'

    def get(self, request, travel_id):
        travel = Travel.objects.get(id=travel_id)
        form = Activity2Form()
        return render(request, self.template_name, {'travel': travel, 'form': form})

    def post(self, request, travel_id):
        travel = Travel.objects.get(id=travel_id)
        form = ActivityForm(request.POST)

        if form.is_valid():
            # Pobierz lub utwórz destination dla podanego travel_id
            destination, created = Destination.objects.get_or_create(travel=travel)

            # Zaktualizuj dane destination o activity id
            selected_activities = form.cleaned_data['name']
            destination.activity.set(selected_activities)
            destination.save()

            return redirect('main')

        return render(request, self.template_name, {'travel': travel, 'form': form})


class TravelDeleteView(View):
    template_name = 'travel_delete.html'
    model = Travel
    success_url = reverse_lazy('travel_list')

    def get(self, request, travel_id):
        travel = get_object_or_404(Travel, id=travel_id)
        return render(request, self.template_name, {'travel': travel})

    def post(self, request, travel_id):
        travel = get_object_or_404(Travel, id=travel_id)
        travel.delete()
        return redirect('main')


class AllTravelsView(View):
    template_name = 'all_travel_list.html'
    context_object_name = 'all_travels'

    def get(self, request):
        all_travels = Travel.objects.all()
        context = {'all_travels': all_travels}
        return render(request, self.template_name, context)

    def post(self, request):
        travel_id = request.POST.get('travel_id')
        # Przekieruj do widoku obsługującego edycję, zakładając, że jest on nazwany EditTravelView
        return redirect('edit_travel', travel_id=travel_id)


class TravelDetailView(DetailView):
    model = Travel
    template_name = 'travel_detail.html'
    context_object_name = 'travel'

    def get(self, request, *args, **kwargs):
        travel_id = self.kwargs.get('pk')
        travel = Travel.objects.get(id=travel_id)
        return render(request, self.template_name, {'travel': travel})

