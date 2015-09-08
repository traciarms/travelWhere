from django.core.management import BaseCommand, CommandError
import rauth
from travel.models import City, Restaurant
from travelWhere.settings import consumer_key, \
    consumer_secret, token, token_secret


class Command(BaseCommand):
    def handle(self, *args, **options):

        api_call = 0
        all_cities = City.objects.filter(id__gt=24002)
        for city in all_cities:
            session = rauth.OAuth1Session(
            consumer_key = consumer_key, consumer_secret = consumer_secret,
            access_token = token, access_token_secret = token_secret)

            self.stdout.write('the city state is {}, {} {}'.
                                                  format(city.city, city.state,
                                                     city.id))
            response = session.get('http://api.yelp.com/v2/search',
                                   params={'term': 'food',
                                        'location': city.city+', '+city.state})
            api_call += 1
            print(api_call)
            yelp = response.json()
            high_rating_count = 0

            if 'error' not in yelp.keys():
                for business in yelp['businesses']:
                    rating = business['rating']

                    if rating >= 4:
                        high_rating_count += 1
                        if 'city' in business['location'].keys():
                            loc_city = business['location']['city']
                        else:
                            loc_city = ''
                        if 'state_code' in business['location'].keys():
                            state = business['location']['state_code']
                        else:
                            state = ''

                        if loc_city and state:
                            try:
                                city = City.objects.get(city=loc_city, state=state)
                            except City.DoesNotExist:
                                city = None

                            yelp_id = business['id']
                            name = business['name']
                            address = business['location']['address']
                            if 'phone' in business.keys():
                                phone = business['phone']
                            else:
                                phone = ''
                            rating = rating
                            url = business['url']
                            category = ''
                            if 'categories' in business.keys():
                                for cat in business['categories']:
                                    if len(cat) > 1:
                                        for each in cat:
                                            if category == '':
                                                category = each
                                            else:
                                                category = category+', '+each
                                    else:
                                        if category == '':
                                            category = cat
                                        else:
                                            category = category+', '+cat

                            if city:
                                try:
                                    print('getting')
                                    Restaurant.objects.get(yelp_id=yelp_id)
                                except Restaurant.DoesNotExist:
                                    print('creating')
                                    obj = Restaurant.objects.create(city=city,
                                                                    yelp_id=yelp_id,
                                                                    name=name,
                                                                    address=address,
                                                                    loc_city=loc_city,
                                                                    state=state,
                                                                    category=category,
                                                                    phone=phone,
                                                                    rating=rating,
                                                                    url=url)
                                    obj.save()

            if api_call > 24990:
                raise CommandError('too many api calls {} on city {}'
                                   .format(api_call, city.city))