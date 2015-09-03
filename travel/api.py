import hashlib
import rauth
import requests
import time
from travel.models import City, Event
from travelWhere.settings import ZIPCODES_API_KEY, EVENTFUL_API_KEY, \
    TRAIL_API_KEY, consumer_key, token, consumer_secret, token_secret, \
    EXPEDIA_API_KEY, EXPEDIA_SECRET, EXPEDIA_CID


def call_zipcode_api(zipcode, distance):
    response = requests.get('https://www.zipcodeapi.com/rest/{}/radius.json/'\
                            '{}/{}/mile'.\
                format(ZIPCODES_API_KEY, zipcode, distance))

    location_list = []
    locations = response.json()

    if 'zip_codes' in locations.keys():
        location_list = locations['zip_codes']
        for location in location_list:
            city = location['city']
            state = location['state']

            if city and state:
                city = City.objects.get_or_create(city=city, state=state)

    return location_list


def call_eventful_api(search_city):
    response = requests.get('http://api.eventful.com/json/events/search?'\
                            'app_key={}&l={}&c={},{}'.\
                            format(EVENTFUL_API_KEY, search_city,
                            'festivals_parades', 'music'))
    num_events = []
    events = response.json()

    if 'total_items' in events.keys():
        num_events = int(events['total_items'])

        if num_events > 1:
            for event in events['events']['event']:
                title = event['title']
                eventful_id = event['id']
                address = event['venue_address']
                loc_city = event['city_name']
                state = event['region_abbr']
                city = City.objects.get(city=loc_city, state=state)
                date = event['start_time']
                description = event['description']
                venue_name = event['venue_name']
                url = event['venue_url']
                Event.objects.get_or_create(city=city,
                                            eventful_id=eventful_id,
                                            title=title,
                                            address=address,
                                            loc_city=loc_city,
                                            state=state,
                                            date=date,
                                            description=description,
                                            venue_name=venue_name,
                                            url=url)
        elif num_events == 1:
            title = events['events']['event']['title']
            eventful_id = events['events']['event']['id']
            address = events['events']['event']['venue_address']
            loc_city = events['events']['event']['city_name']
            state = events['events']['event']['region_abbr']
            city = City.objects.get(city=loc_city, state=state)
            date = events['events']['event']['start_time']
            description = events['events']['event']['description']
            venue_name = events['events']['event']['venue_name']
            url = events['events']['event']['venue_url']
            Event.objects.get_or_create(city=city,
                                        eventful_id=eventful_id,
                                        title=title,
                                        address=address,
                                        loc_city=loc_city,
                                        state=state,
                                        date=date,
                                        description=description,
                                        venue_name=venue_name,
                                        url=url)

    return num_events


def call_trails_api(search_city):
    response = requests.get('https://outdoor-data-api.herokuapp.com/api.json?'\
                            'api_key={}&q[city_eq]={}&radius=25'.\
                           format(TRAIL_API_KEY, search_city))

    num_trails = []
    trails = response.json()

    if 'places' in trails.keys():
        num_trails = len(trails['places'])

        for place in trails['places']:
            name = place['name']
            loc_city = place['city']
            state = place['state']
            description = place['description']
            category = ''
            for activity in place['activities']:
                category = category+', '+activity['activity_type']['name']

    return num_trails


def call_food_api(search_city):

    session = rauth.OAuth1Session(
        consumer_key = consumer_key, consumer_secret = consumer_secret,
        access_token = token, access_token_secret = token_secret)

    response = session.get('http://api.yelp.com/v2/search',
                           params={'term': 'food', 'location': search_city})

    yelp = response.json()
    high_rating_count = 0

    if 'error' not in yelp.keys():
        for business in yelp['businesses']:
            rating = business['rating']

            if rating >= 4:
                high_rating_count += 1

                name = business['name']
                address = business['location']['address']
                loc_city = business['location']['city']
                state = business['location']['state_code']
                if 'phone' in business.keys():
                    phone = business['phone']
                rating = rating
                url = business['url']
                category = ''
                for cat in business['categories']:
                    if len(cat) > 1:
                        for each in cat:
                            category = category+', '+each
                    else:
                        category = category+', '+cat
    return high_rating_count


def call_nightlife_api(search_city):

    session = rauth.OAuth1Session(
        consumer_key = consumer_key, consumer_secret = consumer_secret,
        access_token = token, access_token_secret = token_secret)

    response = session.get('http://api.yelp.com/v2/search',
                           params={'category_filter': 'nightlife',
                                   'location': search_city})

    yelp = response.json()
    num_night_life = 0

    if 'error' not in yelp.keys():
        num_night_life = yelp['total']

        if num_night_life > 0:
            for business in yelp['businesses']:
                name = business['name']
                address = business['location']['address']
                loc_city = business['location']['city']
                state = business['location']['state_code']
                if 'phone' in business.keys():
                    phone = business['phone']
                rating = business['rating']
                url = business['url']
                category = ''
                for cat in business['categories']:
                    if len(cat) > 1:
                        for each in cat:
                            category = category+', '+each
                    else:
                        category = category+', '+cat
        else:
            name = yelp['name']
            address = yelp['location']['address']
            loc_city = yelp['location']['city']
            state = yelp['location']['state_code']
            if 'phone' in yelp.keys():
                phone = yelp['phone']
            rating = yelp['rating']
            url = yelp['url']
            category = ''
            for cat in yelp['categories']:
                if len(cat) > 1:
                    for each in cat:
                        category = category+', '+each
                else:
                    category = category+', '+cat

    return num_night_life


def call_expedia_api(city):
    signature = hashlib.md5((EXPEDIA_API_KEY+EXPEDIA_SECRET+
                             str(int(time.time()))).encode("utf")).hexdigest()
    headers = { 'cid' : EXPEDIA_CID,
                'apiKey': EXPEDIA_API_KEY,
                'sig': signature,
                'city': city,
                'sort': 'PRICE'}
    response = requests.get('http://api.ean.com/ean-services/rs/hotel/v3/list?',
                            headers)

    hotels = response.json()
    num_hotels = 0

    if 'error' not in hotels.keys():
        if 'HotelList' in hotels['HotelListResponse'].keys():
            num_hotels = int(hotels['HotelListResponse']['HotelList']\
                                 ['@activePropertyCount'])
            hotel_list = hotels['HotelListResponse']['HotelList']\
                ['HotelSummary']

            if num_hotels > 1:
               for hotel in hotel_list:
                    name = hotel['name']
            else:
                name = hotel_list['name']


            # address = hotels['HotelListResponse']['HotelList']\
            #     ['HotelSummary']['address1']
            # loc_city = hotels['HotelListResponse']['HotelList']\
            #     ['HotelSummary']['city']
            # state = hotels['HotelListResponse']['HotelList']\
            #     ['HotelSummary']['stateProvinceCod']
            # low_rate = hotels['HotelListResponse']['HotelList']\
            #     ['HotelSummary']['lowRate']
            # high_rate = hotels['HotelListResponse']['HotelList']\
            #     ['HotelSummary']['highRate']
            # rating = hotels['HotelListResponse']['HotelList']\
            #     ['HotelSummary']['hotelRating']
            # url = 'http://images.travelnow.com'+hotels['HotelListResponse']\
            #     ['HotelList']['HotelSummary']['thumbNailUrl']

    return num_hotels

