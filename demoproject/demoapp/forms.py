from django import forms
from .models import Booking, UserComments

SHIFTS = (
    ("1", "Morning"),
    ("2", "Afternoon"),
    ("3", "Evening"),
)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"


class InputForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200, required=False)
    shift = forms.ChoiceField(choices=SHIFTS)
    time_log = forms.TimeField(help_text="enter time here")


class UserCommentsForm(forms.ModelForm):
    class Meta:
        model = UserComments
        fields = '__all__'
