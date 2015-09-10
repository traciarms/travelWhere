import rauth
import requests
from travel.models import City, Event, OutdoorRecreation, \
    Restaurant, NightLife
from travelWhere.settings import ZIPCODES_API_KEY, EVENTFUL_API_KEY, \
    TRAIL_API_KEY, consumer_key, token, consumer_secret, token_secret
import us


def call_zipcode_api(zipcode, distance):
    response = requests.get('https://www.zipcodeapi.com/rest/{}/radius.json/'\
                            '{}/{}/mile'.\
                format(ZIPCODES_API_KEY, zipcode, distance))

    location_list = []
    locations = response.json()

    if 'zip_codes' in locations.keys():
        location_list = locations['zip_codes']

        # for location in location_list:
        #     city = location['city']
        #     state = location['state']

            # if city and state:
            #     city = City.objects.get_or_create(city=city, state=state)

    return location_list


def call_eventful_api(search_city, search_state):

    all_cities = City.objects.filter(id__gt=400)
    print(len(all_cities))

    for city in all_cities:
        response = requests.get('http://api.eventful.com/json/events/search?'\
                            'app_key={}&l={},{}&within={}&c={},{}'.\
                            format(EVENTFUL_API_KEY, city.city, city.state,
                            '30', 'festivals_parades', 'music'))

        events = response.json()

        if 'total_items' in events.keys():
            num_events = int(events['total_items'])

            if num_events > 1:
                if 'events' in events.keys():
                    if events['events'] != None:
                        for event in events['events']['event']:

                            if type(event) is dict:
                                if 'city_name' in event.keys():
                                    loc_city = event['city_name']
                                if 'region_abbr' in event.keys():
                                    state = event['region_abbr']
                                if loc_city and state:
                                    try:
                                        city = City.objects.get(city=loc_city, state=state)
                                    except City.DoesNotExist:
                                        city = None
                                    title = event['title']
                                    eventful_id = event['id']
                                    address = event['venue_address']
                                    date = event['start_time']
                                    description = event['description']
                                    venue_name = event['venue_name']
                                    url = event['venue_url']

                                    if city and loc_city and state:
                                        try:
                                            Event.objects.get(eventful_id=eventful_id)
                                        except Event.DoesNotExist:
                                            obj = Event.objects.create(city=city,
                                                                    eventful_id=eventful_id,
                                                                    title=title,
                                                                    address=address,
                                                                    loc_city=loc_city,
                                                                    state=state,
                                                                    date=date,
                                                                    description=description,
                                                                    venue_name=venue_name,
                                                                    url=url)
                                            obj.save()
            elif num_events == 1:
                loc_city = events['events']['event']['city_name']
                state = events['events']['event']['region_abbr']
                try:
                    city = City.objects.get(city=loc_city, state=state)
                except City.DoesNotExist:
                    city = None
                title = events['events']['event']['title']
                eventful_id = events['events']['event']['id']
                address = events['events']['event']['venue_address']
                date = events['events']['event']['start_time']
                description = events['events']['event']['description']
                venue_name = events['events']['event']['venue_name']
                url = events['events']['event']['venue_url']

                if city and loc_city and state:
                    try:
                        Event.objects.get(eventful_id=eventful_id)
                    except Event.DoesNotExist:
                        obj = Event.objects.create(city=city,
                                                eventful_id=eventful_id,
                                                title=title,
                                                address=address,
                                                loc_city=loc_city,
                                                state=state,
                                                date=date,
                                                description=description,
                                                venue_name=venue_name,
                                                url=url)
                        obj.save()
    return num_events


def call_trails_api(search_city, search_state):
    response = requests.get('https://outdoor-data-api.herokuapp.com/api.json?'\
                            'api_key={}&q[city_eq]={}&q[state_cont]={}'\
                            '&radius=25'.\
                           format(TRAIL_API_KEY, search_city, search_state))

    num_trails = []
    trails = response.json()

    if 'places' in trails.keys():
        num_trails = len(trails['places'])

        for place in trails['places']:
            loc_city = place['city']
            state = place['state']
            if len(state) > 2:
                states_dict = us.states.mapping('name', 'abbr')
                state = states_dict[state]
                print(state)
            try:
                city = City.objects.get(city=loc_city, state=state)
            except City.DoesNotExist:
                city = None

            name = place['name']
            description = place['description']
            category = ''
            for activity in place['activities']:
                if category == '':
                    category = activity['activity_type']['name']
                else:
                    category = category+', '+activity['activity_type']['name']

            if city and loc_city and state:
                try:
                    OutdoorRecreation.objects.get(name=name,
                                                  loc_city=loc_city,
                                                  state=state)
                except OutdoorRecreation.DoesNotExist:
                    obj = OutdoorRecreation.objects.create(city=city,
                                                    name=name,
                                                    loc_city=loc_city,
                                                    state=state,
                                                    category=category,
                                                    description=description)
                    obj.save()

    return num_trails


def call_food_api(search_city, search_state):

    session = rauth.OAuth1Session(
        consumer_key = consumer_key, consumer_secret = consumer_secret,
        access_token = token, access_token_secret = token_secret)

    response = session.get('http://api.yelp.com/v2/search',
                           params={'term': 'food',
                                'location': search_city+', '+search_state})

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
                        Restaurant.objects.get_or_create(city=city,
                                                    yelp_id=yelp_id,
                                                    name=name,
                                                    address=address,
                                                    loc_city=loc_city,
                                                    state=state,
                                                    category=category,
                                                    phone=phone,
                                                    rating=rating,
                                                    url=url)

    return high_rating_count


def call_nightlife_api(search_city, search_state):

    session = rauth.OAuth1Session(
        consumer_key = consumer_key, consumer_secret = consumer_secret,
        access_token = token, access_token_secret = token_secret)

    response = session.get('http://api.yelp.com/v2/search',
                           params={'category_filter': 'nightlife',
                                   'location': search_city+', '\
                                               +'search_state'})

    yelp = response.json()
    num_night_life = 0

    if 'error' not in yelp.keys():
        num_night_life = yelp['total']

        if num_night_life > 0:
            for business in yelp['businesses']:

                loc_city = business['location']['city']
                state = business['location']['state_code']
                if loc_city and state:
                    try:
                        city = City.objects.get(city=loc_city, state=state)
                    except City.DoesNotExist:
                        city = None

                name = business['name']
                yelp_id = business['id']
                address = business['location']['address']

                if 'phone' in business.keys():
                    phone = business['phone']
                else:
                    phone = ''
                url = business['url']
                category = ''
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
                    NightLife.objects.get_or_create(city=city,
                                                    yelp_id=yelp_id,
                                                    name=name,
                                                    address=address,
                                                    loc_city=loc_city,
                                                    state=state,
                                                    category=category,
                                                    phone=phone,
                                                    url=url)
        else:
            loc_city = yelp['location']['city']
            state = yelp['location']['state_code']
            if loc_city and state:
                try:
                    if len(state) == 2:
                        city, created = \
                            City.objects.get_or_create(city=loc_city,
                                                       state=state)
                    else:
                        city = City.objects.get(city=loc_city,
                                                state=state)
                except City.DoesNotExist:
                    city = None
            name = yelp['name']
            yelp_id = yelp['id']
            address = yelp['location']['address']

            if 'phone' in yelp.keys():
                phone = yelp['phone']
            else:
                phone = ''
            url = yelp['url']
            category = ''
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
                    NightLife.objects.get_or_create(city=city,
                                                    yelp_id=yelp_id,
                                                    name=name,
                                                    address=address,
                                                    loc_city=loc_city,
                                                    state=state,
                                                    category=category,
                                                    phone=phone,
                                                    url=url)

    return num_night_life


# def call_expedia_api(city, state):
#     signature = hashlib.md5((EXPEDIA_API_KEY+EXPEDIA_SECRET+
#                              str(int(time.time()))).encode("utf")).hexdigest()
#     headers = { 'cid' : EXPEDIA_CID,
#                 'apiKey': EXPEDIA_API_KEY,
#                 'sig': signature,
#                 'city': city,
#                 'stateProvinceCode': state,
#                 'countryCode': 'US',
#                 'sort': 'PRICE'}
#     response = requests.get('http://api.ean.com/ean-services/rs/hotel/v3/list?',
#                             headers)
#
#     hotels = response.json()
#     num_hotels = 0
#
#     if 'error' not in hotels.keys():
#         if 'HotelList' in hotels['HotelListResponse'].keys():
#             num_hotels = int(hotels['HotelListResponse']['HotelList']\
#                                  ['@activePropertyCount'])
#             hotel_list = hotels['HotelListResponse']['HotelList']\
#                 ['HotelSummary']
#
#             if num_hotels > 1:
#                for hotel in hotel_list:
#                     loc_city = hotel['city']
#                     state = hotel['stateProvinceCode']
#                     if loc_city and state:
#                         try:
#                             if len(state) == 2:
#                                 city, created = \
#                                     City.objects.get_or_create(city=loc_city,
#                                                                state=state)
#                             else:
#                                 city = City.objects.get(city=loc_city,
#                                                         state=state)
#                         except City.DoesNotExist:
#                             city = None
#
#                     name = hotel['name']
#                     hotel_id = hotel['hotelId']
#                     address = hotel['address1']
#                     low_rate = hotel['lowRate']
#                     high_rate = hotel['highRate']
#                     rating = hotel['hotelRating']
#                     url = hotel['thumbNailUrl']
#
#                     if city:
#                         try:
#                             Hotel.objects.get_or_create(hotel_id=hotel_id)
#                         except Hotel.DoesNotExist:
#                             obj = Hotel.objects.get_or_create(city=city,
#                                                         hotel_id=hotel_id,
#                                                         name=name,
#                                                         address=address,
#                                                         loc_city=loc_city,
#                                                         state=state,
#                                                         high_rate=high_rate,
#                                                         low_rate=low_rate,
#                                                         rating=rating,
#                                                         url=url)
#                             obj.save()
#             else:
#                 name = hotel_list['name']
#                 hotel_id = hotel_list['hotelId']
#                 address = hotel_list['address1']
#                 loc_city = hotel_list['city']
#                 state = hotel_list['stateProvinceCode']
#                 low_rate = hotel_list['lowRate']
#                 high_rate = hotel_list['highRate']
#                 rating = hotel_list['hotelRating']
#                 url = hotel_list['thumbNailUrl']
#
#                 if city:
#                     try:
#                         Hotel.objects.get_or_create(hotel_id=hotel_id)
#                     except Hotel.DoesNotExist:
#                         obj = Hotel.objects.get_or_create(city=city,
#                                                     hotel_id=hotel_id,
#                                                     name=name,
#                                                     address=address,
#                                                     loc_city=loc_city,
#                                                     state=state,
#                                                     high_rate=high_rate,
#                                                     low_rate=low_rate,
#                                                     rating=rating,
#                                                     url=url)
#                         obj.save()
#
#     return num_hotels

