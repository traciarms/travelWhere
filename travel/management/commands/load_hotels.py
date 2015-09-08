import time
import hashlib
from django.core.management import BaseCommand, CommandError
import requests
from travel.models import City, Event, Hotel
from travelWhere.settings import EVENTFUL_API_KEY, EXPEDIA_API_KEY, \
    EXPEDIA_SECRET, EXPEDIA_CID, ZIPCODES_API_KEY


class Command(BaseCommand):
    def handle(self, zipcode=None, *args, **options):

        api_call = 0
        response = requests.get('https://www.zipcodeapi.com/rest/{}/radius.json/'\
                            '{}/{}/mile'.format(ZIPCODES_API_KEY, '89104', 300))

        location_list = []
        locations = response.json()

        if 'zip_codes' in locations.keys():
            location_list = locations['zip_codes']
            for location in location_list:
                city = location['city']
                state = location['state']

                self.stdout.write('the city state is {}, {}'.format(city,
                                                                    state))

                signature = hashlib.md5((EXPEDIA_API_KEY+EXPEDIA_SECRET+
                                 str(int(time.time()))).encode("utf")).hexdigest()
                headers = { 'cid' : EXPEDIA_CID,
                            'apiKey': EXPEDIA_API_KEY,
                            'sig': signature,
                            'city': city,
                            'stateProvinceCode': state,
                            'countryCode': 'US',
                            'sort': 'PRICE'}
                response = requests.get('http://api.ean.com/ean-services/rs/hotel/v3/list?',
                                        headers)

                hotels = response.json()
                api_call += 1

                if 'error' not in hotels.keys():
                    if 'HotelList' in hotels['HotelListResponse'].keys():
                        num_hotels = int(hotels['HotelListResponse']['HotelList']\
                                             ['@activePropertyCount'])
                        hotel_list = hotels['HotelListResponse']['HotelList']\
                            ['HotelSummary']

                        if num_hotels > 1:
                           for hotel in hotel_list:
                                if 'city' in hotel.keys():
                                    loc_city = hotel['city']
                                if 'stateProvinceCode' in hotel.keys():
                                    state = hotel['stateProvinceCode']
                                if loc_city and state:
                                    try:
                                        city = City.objects.get(city=loc_city,
                                                                state=state)
                                    except City.DoesNotExist:
                                        city = None

                                    name = hotel['name']
                                    hotel_id = hotel['hotelId']
                                    address = hotel['address1']
                                    low_rate = hotel['lowRate']
                                    high_rate = hotel['highRate']
                                    rating = hotel['hotelRating']
                                    url = hotel['thumbNailUrl']

                                    if city:
                                        try:
                                            Hotel.objects.get(hotel_id=hotel_id)
                                        except Hotel.DoesNotExist:
                                            obj = Hotel.objects.create(city=city,
                                                                        hotel_id=hotel_id,
                                                                        name=name,
                                                                        address=address,
                                                                        loc_city=loc_city,
                                                                        state=state,
                                                                        high_rate=high_rate,
                                                                        low_rate=low_rate,
                                                                        rating=rating,
                                                                        url=url)
                                            obj.save()

                        else:
                            if 'city' in hotel_list.keys():
                                loc_city = hotel_list['city']
                            if 'stateProvinceCode' in hotel_list.keys():
                                state = hotel_list['stateProvinceCode']
                            if loc_city and state:
                                try:
                                    city = City.objects.get(city=loc_city,
                                                            state=state)
                                except City.DoesNotExist:
                                    city = None
                                name = hotel_list['name']
                                hotel_id = hotel_list['hotelId']
                                address = hotel_list['address1']
                                low_rate = hotel_list['lowRate']
                                high_rate = hotel_list['highRate']
                                rating = hotel_list['hotelRating']
                                url = hotel_list['thumbNailUrl']

                                if city:
                                    try:
                                        Hotel.objects.get(hotel_id=hotel_id)
                                    except Hotel.DoesNotExist:
                                        obj = Hotel.objects.create(city=city,
                                                                    hotel_id=hotel_id,
                                                                    name=name,
                                                                    address=address,
                                                                    loc_city=loc_city,
                                                                    state=state,
                                                                    high_rate=high_rate,
                                                                    low_rate=low_rate,
                                                                    rating=rating,
                                                                    url=url)
                                        obj.save()
                # else:
                #     raise CommandError('Too many api call for today {}'
                #                        ' left off at city {}'.
                #                        format(api_call, city.city))

