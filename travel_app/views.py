from django.views import View
from django.shortcuts import render, redirect

from travel_app.forms import TravelForm, ActivityForm
from travel_app.models import Travel


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
            form.save()
            return redirect('main')
        return render(request, self.template_name, {'form': form})
