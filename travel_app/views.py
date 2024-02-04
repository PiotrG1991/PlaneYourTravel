from django.views import View
from django.shortcuts import render, redirect

from travel_app.forms import TravelForm, ActivityForm, TransportForm, DestinationForm
from travel_app.models import Travel, Transport, Destination


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'welcome.html')


class MainView(View):
    model = Travel
    template_name = 'latest_travels_list.html'
    context_object_name = 'latest_travels'
    ordering = ['-created']

    def get(self, request):
        return render(request, 'travel_list.html')

class AddActivityView(View):
    def get(self, request):
        form = ActivityForm()
        return render(request, 'add_activity.html', {'form':form})

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
            destination = Destination.objects.create(transport=transport, travel=travel)

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
            return redirect('next_view_or_page')

        return render(request, self.template_name, {'travel': travel, 'form': form})