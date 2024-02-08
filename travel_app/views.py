from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from travel_app.forms import TravelForm, ActivityForm, TransportForm, DestinationForm, AccommodationForm, \
    TuristsPlacesForm, Activity2Form, EditActivityForm
from travel_app.models import Travel, Destination, Activity


class HomeView(View):
    def get(self, request):
        return render(request, 'welcome.html')


class MainView(ListView):
    model = Travel
    template_name = 'travel_list.html'
    context_object_name = 'travels'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Travel.objects.filter(
                Q(title__icontains=query) |
                Q(participants__icontains=query)
            ).order_by('-created')
        else:
            latest_travels = Travel.objects.order_by('-created')[:5]
            return latest_travels


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

            # Tworzenie nowej destynacji
            destination = Destination.objects.create()

            travel.title = form.cleaned_data['title']
            travel.start_date = form.cleaned_data['start_date']
            travel.end_date = form.cleaned_data['end_date']
            travel.participants = form.cleaned_data['participants']

            travel.save()

            # Ustawienie destynacji dla podróży
            travel.destination.set([destination])

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

            # Sprawdź, czy istnieje już destynacja dla danej podróży
            destinations = Destination.objects.filter(travel=travel).order_by('-id')

            if destinations.exists():
                destination = destinations.first()
            else:

                destination = Destination.objects.create(travel=travel)

            destination.transport = transport
            destination.save()

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
            # Sprawdź, czy istnieje już destynacja dla danej podróży
            destinations = Destination.objects.filter(travel=travel).order_by('-id')

            if destinations.exists():
                destination = destinations.first()
            else:
                # Jeśli nie ma jeszcze żadnej destynacji, utwórz nową
                destination = Destination.objects.create(travel=travel)

            # Ustaw dane destynacji na podstawie formularza
            destination.destination_name = form.cleaned_data['destination_name']
            destination.destination_description = form.cleaned_data['destination_description']
            destination.start_date = form.cleaned_data['start_date']
            destination.end_date = form.cleaned_data['end_date']

            destination.save()

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
            destinations = Destination.objects.filter(travel=travel).order_by('-id')

            if destinations.exists():
                destination = destinations.first()
            else:
                destination = Destination.objects.create(travel=travel)

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

            destinations = Destination.objects.filter(travel=travel).order_by('-id')
            if destinations.exists():
                destination = destinations.first()
            else:
                destination = Destination.objects.create(travel=travel)

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
        form = Activity2Form(request.POST)

        if 'finish' in request.POST:
            if form.is_valid():
                destination = Destination.objects.filter(travel=travel).latest('id')

                selected_activities = form.cleaned_data['name']
                destination.activity.set(selected_activities)
                destination.save()

                return redirect('main')
            return render(request, self.template_name, {'travel': travel, 'form': form})

        elif 'next_destination' in request.POST:
            if form.is_valid():
                destination = Destination.objects.filter(travel=travel).latest('id')

                selected_activities = form.cleaned_data['name']
                destination.activity.set(selected_activities)
                destination.save()

                next_destination = Destination.objects.create(travel=travel)
                travel.destination.add(next_destination)

                return redirect('add_transport', travel_id=travel.id)

        return render(request, self.template_name, {'travel': travel, 'form': form})


class AddNextDestinationView(View):
    template_name = 'add_next_destination.html'

    def get(self, request, travel_pk):
        travel = get_object_or_404(Travel, pk=travel_pk)
        destination_form = DestinationForm()
        transport_form = TransportForm()
        accommodation_form = AccommodationForm()
        turists_places_form = TuristsPlacesForm()
        activity_form = Activity2Form()  # Użyj formularza Activity2Form
        return render(request, self.template_name, {
            'travel': travel,
            'destination_form': destination_form,
            'transport_form': transport_form,
            'accommodation_form': accommodation_form,
            'turists_places_form': turists_places_form,
            'activity_form': activity_form,
        })

    def post(self, request, travel_pk):
        travel = get_object_or_404(Travel, pk=travel_pk)
        destination_form = DestinationForm(request.POST)
        transport_form = TransportForm(request.POST)
        accommodation_form = AccommodationForm(request.POST)
        turists_places_form = TuristsPlacesForm(request.POST)
        activity_form = Activity2Form(request.POST)

        if destination_form.is_valid() and transport_form.is_valid() and accommodation_form.is_valid() and turists_places_form.is_valid() and activity_form.is_valid():
            destination = destination_form.save(commit=False)
            destination.travel = travel
            destination.save()
            transport = transport_form.save(commit=False)
            transport.save()
            selected_activities = activity_form.cleaned_data.get('name')  # Poprawne uzyskanie cleaned_data
            destination.activity.clear()
            destination.activity.set(selected_activities)
            destination.save()

            return redirect('edit_travel', pk=travel_pk)

        return render(request, self.template_name, {
            'travel': travel,
            'destination_form': destination_form,
            'transport_form': transport_form,
            'accommodation_form': accommodation_form,
            'turists_places_form': turists_places_form,
            'activity_form': activity_form,
        })
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
        return redirect('edit_travel', travel_id=travel_id)


class TravelDetailView(DetailView):
    model = Travel
    template_name = 'travel_detail.html'
    context_object_name = 'travel'

    def get(self, request, *args, **kwargs):
        travel_id = self.kwargs.get('pk')
        travel = Travel.objects.get(id=travel_id)
        return render(request, self.template_name, {'travel': travel})


class EditTravelView(View):
    template_name = 'edit_travel.html'

    def get(self, request, pk):
        travel = Travel.objects.get(pk=pk)
        travel_form = TravelForm(instance=travel)
        destinations = travel.destination.all()
        context = {
            'travel_form': travel_form,
            'travel': travel,
            'destinations': destinations,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        travel = Travel.objects.get(pk=pk)
        travel_form = TravelForm(request.POST, instance=travel)
        if travel_form.is_valid():
            travel_form.save()
            return redirect('edit_travel', pk=pk)
        destinations = travel.destination.all()
        context = {
            'travel_form': travel_form,
            'travel': travel,
            'destinations': destinations,
        }
        return render(request, self.template_name, context)


class EditDestinationView(View):
    template_name = 'edit_destination.html'

    def get(self, request, pk):
        destination = get_object_or_404(Destination, pk=pk)
        destination_form = DestinationForm(instance=destination)
        transport_form = TransportForm(instance=destination.transport)
        accommodation_form = AccommodationForm(instance=destination.accommodation)
        turists_places_form = TuristsPlacesForm(instance=destination.turists_places)
        activity_form = Activity2Form(instance=destination)
        travel_pk = destination.travel_set.first().id

        return render(request, self.template_name, {
            'destination_form': destination_form,
            'transport_form': transport_form,
            'accommodation_form': accommodation_form,
            'turists_places_form': turists_places_form,
            'activity_form': activity_form,
            'destination': destination,
            'travel_pk': travel_pk,

        })

    def post(self, request, pk):
        destination = get_object_or_404(Destination, pk=pk)
        destination_form = DestinationForm(request.POST, instance=destination)
        transport_form = TransportForm(request.POST, instance=destination.transport)
        accommodation_form = AccommodationForm(request.POST, instance=destination.accommodation)
        turists_places_form = TuristsPlacesForm(request.POST, instance=destination.turists_places)
        activity_form = Activity2Form(request.POST, instance=destination)

        if (
                destination_form.is_valid() and
                transport_form.is_valid() and
                accommodation_form.is_valid() and
                turists_places_form.is_valid() and
                activity_form.is_valid()
        ):
            destination_form.save()
            transport_form.save()
            accommodation_form.save()
            turists_places_form.save()
            selected_activities = activity_form.cleaned_data.get('activities')

            if selected_activities:
                destination.activity.clear()
                destination.activity.set(selected_activities)


            related_travels = Travel.objects.filter(destination=destination)
            travel_id = related_travels.first().id if related_travels.exists() else None

            return redirect('edit_travel', pk=travel_id)

        return render(request, self.template_name, {
            'destination_form': destination_form,
            'transport_form': transport_form,
            'accommodation_form': accommodation_form,
            'turists_places_form': turists_places_form,
            'activity_form': activity_form,
            'destination': destination,
        })

class ActivityListView(View):
    template_name = 'activity_list.html'

    def get(self, request):
        activities = Activity.objects.all()
        context = {'activities': activities}
        return render(request, self.template_name, context)

    def post(self, request):
        activity_id = request.POST.get('activity_id')
        if activity_id:
            activity = Activity.objects.get(id=activity_id)
            activity.delete()
        return redirect('activity_list')

