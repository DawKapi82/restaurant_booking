from django import forms
from django.contrib.auth.forms import UserCreationForm

from booking.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['id', 'name', 'surname', 'phone', 'reservation_date', 'table_count']

    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label='Surname', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'class': 'form-control'}))
    reservation_date = forms.DateTimeField(label='Date and time',widget=forms.TextInput(attrs={'type':'datetime-local','class': 'form-control'}))
    table_count = forms.IntegerField(label='Number of tables', widget=forms.TextInput(attrs={'class': 'form-control'}))


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})