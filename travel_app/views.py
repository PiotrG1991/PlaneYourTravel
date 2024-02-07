from django.db.models import Q
from django.urls import reverse_lazy
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

            destination = Destination.objects.create()
            travel.destination = destination

            travel.title = form.cleaned_data['title']
            travel.start_date = form.cleaned_data['start_date']
            travel.end_date = form.cleaned_data['end_date']
            travel.participants = form.cleaned_data['participants']

            travel.save()

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

            destination, created = Destination.objects.get_or_create(travel=travel)
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
            destination, created = Destination.objects.get_or_create(travel=travel)

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

            destination, created = Destination.objects.get_or_create(travel=travel)

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

            destination, created = Destination.objects.get_or_create(travel=travel)

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

        if form.is_valid():
            destination, created = Destination.objects.get_or_create(travel=travel)

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
        transport_form = TransportForm(instance=travel.destination.transport)
        destination_form = DestinationForm(instance=travel.destination)
        edit_activity_form = EditActivityForm()
        accommodation_form = AccommodationForm(instance=travel.destination.accommodation)
        turists_places_form = TuristsPlacesForm(instance=travel.destination.turists_places)



        context = {
            'travel_form': travel_form,
            'transport_form': transport_form,
            'destination_form': destination_form,
            'edit_activity_form': edit_activity_form,
            'accommodation_form': accommodation_form,
            'turists_places_form': turists_places_form,
            'travel': travel,
            'activities': Activity.objects.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):

        travel = Travel.objects.get(pk=pk)
        travel_form = TravelForm(request.POST, instance=travel)
        transport_form = TransportForm(request.POST, instance=travel.destination.transport)
        destination_form = DestinationForm(request.POST, instance=travel.destination)
        accommodation_form = AccommodationForm(request.POST, instance=travel.destination.accommodation)
        turists_places_form = TuristsPlacesForm(request.POST, instance=travel.destination.turists_places)
        edit_activity_form = EditActivityForm(request.POST)

        if (
                travel_form.is_valid() and
                transport_form.is_valid() and
                destination_form.is_valid() and
                accommodation_form.is_valid() and
                turists_places_form.is_valid() and
                edit_activity_form.is_valid()
        ):
            travel_form.save()

            destination_instance = destination_form.save()
            destination_instance.save()

            transport_instance = transport_form.save(commit=False)
            transport_instance.save()

            accommodation_instance = accommodation_form.save(commit=False)
            accommodation_instance.save()

            turists_places_instance = turists_places_form.save(commit=False)
            turists_places_instance.save()

            selected_activities = edit_activity_form.cleaned_data.get('activities')
            destination_instance.activity.clear()
            destination_instance.activity.set(selected_activities)
            destination_instance.save()

            travel_form.save()

            return redirect('main')

        context = {
            'travel_form': travel_form,
            'transport_form': transport_form,
            'destination_form': destination_form,
            'accommodation_form': accommodation_form,
            'turists_places_form': turists_places_form,
            'activity2_form': edit_activity_form,
            'travel': travel,
            'activities': Activity.objects.all(),
        }
        return render(request, self.template_name, context)


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


