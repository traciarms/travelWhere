from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class Customer(models.Model):
    HOTEL_PRICE = 'Hotel Price'
    REST_RATING = 'Restaurant Rating'
    NATIONAL_PARK = 'National Park'
    EVENT = 'Events/Concerts'
    LANDMARK = 'Landmarks'
    FILTER_CATEGORY_CHOICES = (
        (HOTEL_PRICE, 'Hotel Price'),
        (REST_RATING, 'Restaurant Rating'),
        (NATIONAL_PARK, 'National Parks'),
        (EVENT, 'Events/Concerts'),
        (LANDMARK, 'Landmark')
    )
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    distance = models.IntegerField(validators=[MinValueValidator(0)])
    first_filter = models.CharField(max_length=50,
                                    choices=FILTER_CATEGORY_CHOICES,
                                    default=NATIONAL_PARK,
                                    verbose_name='Filter Categories')
    second_filter = models.CharField(max_length=50,
                                     choices=FILTER_CATEGORY_CHOICES,
                                     default=EVENT,
                                     verbose_name='Filter Categories')
    third_filter = models.CharField(max_length=50,
                                    choices=FILTER_CATEGORY_CHOICES,
                                    default=REST_RATING,
                                    verbose_name='Filter Categories')

    def __str__(self):
        return ("User: {}, Address: {}, City: {}, State: {}, Zipcode: {},"
                "Distance: {}".format(self.user, self.address, self.city,
                                   self.state, self.zip_code, self.distance))