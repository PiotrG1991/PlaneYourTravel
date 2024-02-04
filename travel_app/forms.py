from travel_app.models import Travel, Activity
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