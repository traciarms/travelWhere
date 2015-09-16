import time
import hashlib
import requests
from travel.models import City, Hotel
from travelWhere.settings import EXPEDIA_API_KEY, EXPEDIA_SECRET, EXPEDIA_CID


def call_hotel_api(city, state):
    signature = hashlib.md5((EXPEDIA_API_KEY + EXPEDIA_SECRET +
                             str(int(time.time()))).encode("utf")).hexdigest()
    headers = {'cid': EXPEDIA_CID,
               'apiKey': EXPEDIA_API_KEY,
               'sig': signature,
               'city': city,
               'stateProvinceCode': state,
               'countryCode': 'US',
               'sort': 'PRICE'}
    response = requests.get('http://api.ean.com/ean-services/'
                            'rs/hotel/v3/list?',
                            headers)

    hotels = response.json()
    return hotels


def get_total_num(hotels):
    num_hotels = 0
    if 'error' not in hotels.keys():
        if 'HotelList' in hotels['HotelListResponse'].keys():
            num_hotels = int(hotels['HotelListResponse']['HotelList']
                             ['@activePropertyCount'])
    return num_hotels


def parse_api_response(city, hotels):

    if 'error' not in hotels.keys():
        if 'HotelList' in hotels['HotelListResponse'].keys():
            num_hotels = int(hotels['HotelListResponse']['HotelList']
                             ['@activePropertyCount'])
            hotel_list = \
                hotels['HotelListResponse']['HotelList']['HotelSummary']

            if num_hotels > 1:
                for hotel in hotel_list:
                    loc_city = hotel['city']
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

                    create_object(city, hotel_id, name, address, loc_city,
                                  state, high_rate, low_rate, rating, url)

            else:
                loc_city = hotel_list['city']
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

                create_object(city, hotel_id, name, address, loc_city, state,
                              high_rate, low_rate, rating, url)


def create_object(city, hotel_id, name, address, loc_city, state,
                  high_rate, low_rate, rating, url):

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
