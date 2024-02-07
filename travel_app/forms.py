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

    class Meta:
        model = Transport
        fields = ['transport_name', 'transport_description', 'transport_cost']


class DestinationForm(forms.ModelForm):

    class Meta:
        model = Destination
        fields = ['destination_name', 'destination_description', 'start_date', 'end_date']

    widgets = {
        'start_date': forms.DateInput(attrs={'type': 'date'}),
        'end_date': forms.DateInput(attrs={'type': 'date'}),
    }


class AccommodationForm(forms.ModelForm):

    class Meta:
        model = Accommodation
        fields = ['accommodation_name', 'accommodation_description', 'accommodation_address', 'price_per_night']


class TuristsPlacesForm(forms.ModelForm):


    class Meta:
        model = TuristsPlaces
        fields = ['turists_places_description']

class Activity2Form(forms.ModelForm):
    name = forms.ModelMultipleChoiceField(queryset=Activity.objects.all(), widget=forms.CheckboxSelectMultiple, )

    class Meta:
        model = Activity
        fields = ['name']

    widgets = {
        'name': forms.CheckboxSelectMultiple(),
    }

    def save(self, destination):
        activity_id = self.cleaned_data['name'].id
        destination.activity.add(activity_id)



class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, label='Search')


class EditActivityForm(forms.Form):
    activities = forms.ModelMultipleChoiceField(queryset=Activity.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Activity
        fields = ['name']

    widgets = {
        'name': forms.CheckboxSelectMultiple(),
    }

    def save(self, destination):
        activity_id = self.cleaned_data['name'].id
        destination.activity.add(activity_id)