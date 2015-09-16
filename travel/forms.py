from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django import forms
from django.forms import ModelForm
from travel import models
from travel.models import Customer
from travel.validators import validate_zip_code


class CustomerCreationForm(UserCreationForm):
    """
        The customer registration form
    """
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=10, validators=[validate_zip_code])
    user_filter = forms.ChoiceField(
        choices=models.Customer.FILTER_CATEGORY_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'address', 'city',
                  'state', 'zip_code', 'user_filter')


class CustomerProfile(ModelForm):
    """
        The Customer profile form
    """
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'address', 'city', 'state',
                  'zip_code', 'user_filter')


class InitSearchForm(forms.Form):
    """
        The initial search form - empty
    """
    zip_code = forms.CharField(validators=[validate_zip_code],
                               widget=forms.TextInput(attrs={'class':
                                                             'field-input'}))
    distance = forms.IntegerField(validators=[MinValueValidator(0)],
                                  widget=forms.TextInput(attrs={'class':
                                                                'field-input'})
                                  )


class LoggedInSearchForm(forms.Form):
    """
        The search for if the user is logged in - this will load their
        selected filter.
    """
    zip_code = forms.CharField(max_length=10,
                               validators=[validate_zip_code],
                               widget=forms.TextInput(
                                   attrs={'class': 'field-input'}))

    distance = forms.IntegerField(validators=[MinValueValidator(0)],
                                  widget=forms.TextInput(attrs={'class':
                                                                'field-input'})
                                  )
    user_filter = \
        forms.ChoiceField(label='Your preferred search filter',
                          choices=models.Customer.FILTER_CATEGORY_CHOICES,
                          widget=forms.Select(attrs={'class': 'field-input'},
                          choices=(models.Customer.FILTER_CATEGORY_CHOICES)))
