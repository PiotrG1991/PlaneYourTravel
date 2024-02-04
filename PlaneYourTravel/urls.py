"""
URL configuration for PlaneYourTravel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from travel_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('main/', views.MainView.as_view(), name='main'),
    path('add_travel/', views.AddTravelView.as_view(), name='add_travel'),
    path('add_activity/', views.AddActivityView.as_view(), name='add_activity'),
    path('add_travel/transport/<int:travel_id>/', views.AddTransportView.as_view(), name='add_transport'),
    path('add_travel/destination/<int:travel_id>/', views.AddDestinationView.as_view(), name='add_destination'),


    path('accounts/', include('accounts.urls')),
]
