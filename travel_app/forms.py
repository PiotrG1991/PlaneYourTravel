from travel_app.models import Travel, Activity, Transport, Destination
from django import forms

class TravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ['title', 'start_date', 'end_date', 'participants']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name']


class TransportForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}))
    class Meta:
        model = Transport
        fields = ['name', 'description', 'transport_cost']


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'description', 'start_date', 'end_date']

    widgets = {
        'start_date': forms.DateInput(attrs={'type': 'date'}),
        'end_date': forms.DateInput(attrs={'type': 'date'}),
    }
