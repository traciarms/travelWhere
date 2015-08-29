from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, ModelForm
from django import forms

from travel.models import Customer


class CustomerCreationForm(UserCreationForm):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'address', 'city', 'state',
                  'zip_code', 'distance', 'first_filter', 'second_filter',
                  'third_filter')

class InitSearchForm(ModelForm):
    zip_code = forms.CharField(label='Your starting zip code', max_length=10)
    distance = forms.IntegerField(label='How far would you like to travel on this adventure?  ')

    class Meta:
        model = Customer
        fields = ('distance', 'zip_code')