from travel_app.models import Travel, Activity, Transport, Destination, Accommodation, TuristsPlaces
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
        fields = '__all__'


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


class AccommodationForm(forms.ModelForm):

    class Meta:
        model = Accommodation
        fields = ['name', 'description', 'address', 'price_per_night']


class TuristsPlacesForm(forms.ModelForm):

    class Meta:
        model = TuristsPlaces
        fields = ['description']


class Activity2Form(forms.ModelForm):
    name = forms.ModelMultipleChoiceField(queryset=Activity.objects.all(), widget=forms.CheckboxSelectMultiple,)

    class Meta:
        model = Activity
        fields = ['name']

    widgets = {
        'name': forms.CheckboxSelectMultiple(),
    }


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, label='Search')
