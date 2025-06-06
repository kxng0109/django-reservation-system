from django.forms import ModelForm, DateInput, Textarea
from .models import Reservation

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'date', 'party_size', 'notes']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'notes': Textarea(attrs={'rows': 3})
        }