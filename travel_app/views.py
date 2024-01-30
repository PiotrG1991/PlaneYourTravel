from django.views import View
from django.shortcuts import render

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


class MainView(View):
    def get(self, request):
        return render(request, 'main.html')


