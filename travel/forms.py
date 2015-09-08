from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django import forms
from django.forms import ModelForm
from travel import models
from travel.models import Customer
from travel.validators import validate_zip_code


class CustomerCreationForm(UserCreationForm):
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=10, validators=[validate_zip_code])
    user_filter = forms.ChoiceField(
        choices=(models.Customer.FILTER_CATEGORY_CHOICES))

    class Meta:
        model = User
        fields = ('username', 'address', 'city', 'state', 'zip_code',
                  'user_filter')


class CustomerProfile(ModelForm):

    class Meta:
        model = Customer
        fields = ('address', 'city', 'state', 'zip_code', 'user_filter')


class InitSearchForm(forms.Form):
    zip_code = forms.CharField(label='Your starting zip code', max_length=10,
                               validators=[validate_zip_code])
    distance = forms.IntegerField(label='How far would you like to travel on '
                                        'this adventure?',
                                  validators=[MinValueValidator(0)])


class LoggedInSearchForm(forms.Form):
    zip_code = forms.CharField(label='Your starting zip code', max_length=10,
                               validators=[validate_zip_code])
    distance = forms.IntegerField(label='How far would you like to travel on '
                                        'this adventure?',
                                  validators=[MinValueValidator(0)])
    user_filter = forms.ChoiceField(
        choices=(models.Customer.FILTER_CATEGORY_CHOICES))
    # second_filter = forms.ChoiceField(
    #     choices=(models.Customer.FILTER_CATEGORY_CHOICES))
    # third_filter = forms.ChoiceField(
    #     choices=(models.Customer.FILTER_CATEGORY_CHOICES))
