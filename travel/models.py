from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from travel.validators import validate_zip_code


class TruncatingCharField(models.CharField):
    """
        This method is used to truncate fields coming from the api in
        case we are getting data larger than expected.
    """
    def get_prep_value(self, value):
        value = super(TruncatingCharField, self).get_prep_value(value)
        if value:
            return value[:self.max_length]
        return value


class Customer(models.Model):
    """
        This is the customer model for storing the customer profile info
    """
    NONE = 'None'
    HOTEL_PRICE = 'Hotel Price'
    REST_RATING = 'Restaurant Rating'
    OUT_DOOR_RECREATION = 'Outdoor Recreation'
    EVENT = 'Events/Concerts'
    NIGHT_LIFE = 'Night Life'
    FILTER_CATEGORY_CHOICES = (
        (NONE, 'None'),
        (HOTEL_PRICE, 'Hotel Price'),
        (REST_RATING, 'Restaurant Rating'),
        (OUT_DOOR_RECREATION, 'Outdoor Recreation'),
        (EVENT, 'Events/Concerts'),
        (NIGHT_LIFE, 'Night Life')
    )
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10, null=True,
                                validators=[validate_zip_code])
    user_filter = models.CharField(max_length=50,
                                   choices=FILTER_CATEGORY_CHOICES,
                                   default=OUT_DOOR_RECREATION,
                                   verbose_name='Primary Search Filter')

    def has_rated_city(self, city_id):
        city = City.objects.get(pk=city_id)
        ratings = city.rating_set
        rated = len(ratings.filter(customer_id=self.user.customer.id)) > 0
        return rated

    def __str__(self):
        return ("User: {}, Address: {}, City: {}, State: {}, Zipcode: {},"
                .format(self.user, self.address, self.city,
                        self.state, self.zip_code))


class City(models.Model):
    """
        This is the model for storing city info
    """
    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=5, db_index=True)
    img_url = models.TextField(null=True)

    def get_avg_rating(self):
        return self.rating_set.aggregate(rating=Avg('rating'))


class Hotel(models.Model):
    """
        This is the model for storing hotel info
    """
    city = models.ForeignKey(City, null=True)
    hotel_id = TruncatingCharField(max_length=150, null=True, unique=True)
    name = TruncatingCharField(max_length=250)
    address = TruncatingCharField(max_length=250, null=True)
    loc_city = TruncatingCharField(max_length=50)
    state = TruncatingCharField(max_length=5)
    low_rate = models.FloatField()
    high_rate = models.FloatField()
    rating = models.IntegerField()
    url = TruncatingCharField(max_length=250, null=True)


class Restaurant(models.Model):
    city = models.ForeignKey(City, null=True)
    yelp_id = TruncatingCharField(max_length=50, null=True, unique=True)
    name = TruncatingCharField(max_length=250)
    address = TruncatingCharField(max_length=250, null=True)
    loc_city = TruncatingCharField(max_length=50)
    state = TruncatingCharField(max_length=5)
    category = TruncatingCharField(max_length=50, null=True)
    phone = TruncatingCharField(max_length=25, null=True)
    rating = models.FloatField()
    url = TruncatingCharField(max_length=250, null=True)


class NightLife(models.Model):
    city = models.ForeignKey(City, null=True)
    yelp_id = TruncatingCharField(max_length=50, null=True, unique=True)
    name = TruncatingCharField(max_length=250)
    address = TruncatingCharField(max_length=250, null=True)
    loc_city = TruncatingCharField(max_length=50)
    state = TruncatingCharField(max_length=5)
    category = TruncatingCharField(max_length=50, null=True)
    phone = TruncatingCharField(max_length=25, null=True)
    url = TruncatingCharField(max_length=250, null=True)


class Event(models.Model):
    city = models.ForeignKey(City, null=True)
    eventful_id = TruncatingCharField(unique=True,
                                      max_length=100, null=True)
    title = TruncatingCharField(max_length=100, null=True)
    address = TruncatingCharField(max_length=250, null=True)
    loc_city = TruncatingCharField(max_length=250)
    state = TruncatingCharField(max_length=5)
    date = models.DateTimeField(null=True)
    venue_name = TruncatingCharField(max_length=100, null=True)
    description = models.TextField(null=True)
    url = TruncatingCharField(max_length=250, null=True)


class OutdoorRecreation(models.Model):
    city = models.ForeignKey(City, null=True)
    name = TruncatingCharField(max_length=250)
    loc_city = TruncatingCharField(max_length=50)
    state = TruncatingCharField(max_length=5)
    category = TruncatingCharField(max_length=100, null=True)
    description = models.TextField(null=True)

    def natural_key(self):
        return self.name, self.loc_city, self.state

    class Meta:
        unique_together = (('name', 'loc_city', 'state'),)


class OutdoorRecreationManager(models.Manager):
    def get_by_natural_key(self, name, city, state):
        return self.get(name=name, city=city, state=state)


class CityClick(models.Model):
    customer = models.ForeignKey(Customer)
    city = models.ForeignKey(City)
    num_clicks = models.IntegerField(default=0)


class Rating(models.Model):
    customer = models.ForeignKey(Customer)
    city = models.ForeignKey(City)
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(5)])


class HotelClick(models.Model):
    hotel = models.ForeignKey(Hotel)
    customer = models.ForeignKey(Customer)
    num_clicks = models.IntegerField(default=0)


class EventClick(models.Model):
    event = models.ForeignKey(Event)
    customer = models.ForeignKey(Customer)
    num_clicks = models.IntegerField(default=0)


class RestaurantClick(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    customer = models.ForeignKey(Customer)
    num_clicks = models.IntegerField(default=0)


class NightLifeClick(models.Model):
    nightlife = models.ForeignKey(NightLife)
    customer = models.ForeignKey(Customer)
    num_clicks = models.IntegerField(default=0)


class OutdoorRecreationClick(models.Model):
    outdoorrecreation = models.ForeignKey(OutdoorRecreation)
    customer = models.ForeignKey(Customer)
    num_clicks = models.IntegerField(default=0)
