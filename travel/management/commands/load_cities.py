from django.core.management import BaseCommand
import requests
from travel.models import City
from travelWhere.settings import ZIPCODES_API_KEY


class Command(BaseCommand):
    def handle(self, *args, **options):

        response = requests.get('https://www.zipcodeapi.com/rest/{}/'\
                                'radius.json/{}/{}/mile'.\
                format(ZIPCODES_API_KEY, '32169', '4000'))

        location_list = []
        locations = response.json()

        if 'zip_codes' in locations.keys():
            location_list = locations['zip_codes']

            for location in location_list:
                city = location['city']
                state = location['state']

                if city and state:
                    self.stdout.write('Get or create for {}, {}'.
                                      format(city, state))
                    city, created = City.objects.get_or_create(city=city, state=state)
                    self.stdout.write('Create: {}'.format(created))