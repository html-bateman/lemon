from django.forms import ModelForm
from .models import Booking, Reservation


# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
