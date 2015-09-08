from django.core.management import BaseCommand
import requests
from travel.models import City, OutdoorRecreation
from travelWhere.settings import TRAIL_API_KEY
import us


class Command(BaseCommand):
    def handle(self, *args, **options):

        api_call = 0
        all_cities = City.objects.all()
        for city in all_cities:

            response = requests.get('https://outdoor-data-api.herokuapp.com/api.json?'\
                            'api_key={}&q[city_eq]={}&q[state_cont]={}'\
                            '&radius=25'.\
                           format(TRAIL_API_KEY, city.city, city.state))

            num_trails = []
            trails = response.json()

            if 'places' in trails.keys():
                num_trails = len(trails['places'])

                for place in trails['places']:
                    loc_city = place['city']
                    state = place['state']
                    if len(state) > 2:
                        states_dict = us.states.mapping('name', 'abbr')
                        if state in states_dict:
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