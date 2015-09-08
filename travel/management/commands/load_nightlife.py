from django.core.management import BaseCommand, CommandError
import rauth
from travel.models import City, Restaurant, NightLife
from travelWhere.settings import consumer_key, \
    consumer_secret, token, token_secret


class Command(BaseCommand):
    def handle(self, *args, **options):

        api_call = 0
        all_cities = City.objects.filter(id__gt=26346)
        for city in all_cities:
            session = rauth.OAuth1Session(
                consumer_key = consumer_key, consumer_secret = consumer_secret,
                access_token = token, access_token_secret = token_secret)

            self.stdout.write('the city state is {}, {} {}'.
                                                  format(city.city, city.state,
                                                     city.id))

            response = session.get('http://api.yelp.com/v2/search',
                                   params={'category_filter': 'nightlife',
                                           'location': city.city+', '\
                                                       +city.state})
            api_call += 1
            print(api_call)
            yelp = response.json()
            num_night_life = 0

            if 'error' not in yelp.keys():
                num_night_life = yelp['total']

                if num_night_life > 0:
                    for business in yelp['businesses']:
                        if 'location' in business.keys():
                            if 'city' in business['location'].keys():
                                loc_city = business['location']['city']
                        if 'location' in business.keys():
                            if 'state_code' in business['location'].keys():
                                state = business['location']['state_code']
                        if loc_city and state:
                            try:
                                city = City.objects.get(city=loc_city, state=state)
                            except City.DoesNotExist:
                                city = None
                        if 'name' in business.keys():
                            name = business['name']
                        if 'id' in business.keys():
                            yelp_id = business['id']
                        if 'location' in business.keys():
                            if 'address' in business['location'].keys():
                                address = business['location']['address']

                        if 'phone' in business.keys():
                            phone = business['phone']
                        else:
                            phone = ''
                        if 'url' in business.keys():
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
                                NightLife.objects.get(yelp_id=yelp_id)
                            except NightLife.DoesNotExist:
                                print('creating')
                                obj = NightLife.objects.create(city=city,
                                                            yelp_id=yelp_id,
                                                            name=name,
                                                            address=address,
                                                            loc_city=loc_city,
                                                            state=state,
                                                            category=category,
                                                            phone=phone,
                                                            url=url)
                                obj.save()
                else:
                    if 'location' in yelp.keys():
                        loc_city = yelp['location']['city']
                        state = yelp['location']['state_code']
                    if loc_city and state:
                        try:
                            city = City.objects.get(city=loc_city,
                                                        state=state)
                        except City.DoesNotExist:
                            city = None
                    if 'name' in yelp.keys():
                        name = yelp['name']
                    if 'id' in yelp.keys():
                        yelp_id = yelp['id']
                    if 'location' in yelp.keys():
                        address = yelp['location']['address']

                    if 'phone' in yelp.keys():
                        phone = yelp['phone']
                    else:
                        phone = ''
                    if 'url' in yelp.keys():
                        url = yelp['url']
                    category = ''
                    if 'categories' in yelp.keys():
                        for cat in yelp['categories']:
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
                            NightLife.objects.get(yelp_id=yelp_id)
                        except NightLife.DoesNotExist:
                            print('creating')
                            obj = NightLife.objects.create(city=city,
                                                            yelp_id=yelp_id,
                                                            name=name,
                                                            address=address,
                                                            loc_city=loc_city,
                                                            state=state,
                                                            category=category,
                                                            phone=phone,
                                                            url=url)
                            obj.save()

            if api_call > 17000:
                raise CommandError('too many api calls {} on city {}'
                                   .format(api_call, city.city))