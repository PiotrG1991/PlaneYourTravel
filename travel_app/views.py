from django.views import View
from django.shortcuts import render

from travel_app.models import Travel


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


class MainView(View):
    model = Travel
    template_name = 'latest_travels_list.html'
    context_object_name = 'latest_travels'
    ordering = ['-created']
    def get(self, request):
        return render(request, 'main.html')

    def get_queryset(self):
        return Travel.objects.all()[:5]

