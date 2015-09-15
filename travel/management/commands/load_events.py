from django.core.management import BaseCommand, CommandError
import requests
from travel.models import City, Event
from travelWhere.settings import EVENTFUL_API_KEY


class Command(BaseCommand):
    def handle(self, *args, **options):

        api_call = 0
        all_cities = City.objects.filter(id__gt=21969)
        print(len(all_cities))
        prev_city_id = 0

        for city in all_cities:
            print('the city_id is {} and the prev_city_id is {}'.
                  format(city.id, prev_city_id))
            if city.id != prev_city_id:
                response = requests.get('http://api.eventful.com/json/events/'\
                                        'search?'\
                                        'app_key={}&l={},{}&within={}&c='\
                                        '{},{}'.\
                                        format(EVENTFUL_API_KEY,
                                               city.city,
                                               city.state,
                                        '10', 'festivals_parades', 'music'))
                api_call += 1
                prev_city_id = city.id
                events = response.json()

                if 'total_items' in events.keys():
                    page_total = int(events['page_count'])
                    page_count = 0
                    if page_total >= 1:
                        while page_count <= page_total:

                            if api_call < 24990:
                                num_events = 0
                                if city:
                                    self.stdout.write('the city state is {}, {} {}'.
                                                      format(city.city, city.state,
                                                         city.id))
                                    response = requests.get('http://api.eventful.com/json/events/search?'\
                                                'app_key={}&page_size=100&page_number={}&l={},'
                                                            '{}&within={}&c={},{}'.\
                                                format(EVENTFUL_API_KEY, page_count,
                                                       city.city, city.state,
                                                       '30', 'festivals_parades', 'music'))
                                    api_call += 1
                                    print(api_call)
                                    events = response.json()
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
                                                                print('getting')
                                                                Event.objects.get(eventful_id=eventful_id)
                                                            except Event.DoesNotExist:
                                                                print('creating')
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

                                page_count += 1
                            else:
                                raise CommandError('Too many api call for today {}'
                                                   ' left off at city {}'.
                                                   format(api_call, city.city))
