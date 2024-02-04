from travel_app.models import Travel
from django import forms

class TravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ['title', 'start_date', 'end_date', 'participants']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }