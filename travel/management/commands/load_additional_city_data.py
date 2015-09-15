import time
from django.core.management import BaseCommand
import requests
from travel.models import City


class Command(BaseCommand):
    def handle(self, *args, **options):

        all_cities = City.objects.all()

        # headers = {'api-key' : 'vedaf2gfvgknc38cbkk4z7az'}
        # count = 0
        for city in all_cities:

            response = requests.get('https://en.wikipedia.org/w/api.php?format'
                            '=json&action=query&generator=search&'
                            'gsrnamespace=0&gsrsearch={}%2C{}&'
                            'gsrlimit=10&prop=pageimages|extracts&'
                            'pilimit=max&exintro&explaintext&exsentences=1&'
                            'exlimit=max&pithumbsize=300'.format(city.city,
                                                                 city.state))

            wiki = response.json()
            if 'query' in wiki.keys():
                if 'pages' in wiki.get('query').keys():
                    query = wiki.get('query').get('pages')

                    for key in query.keys():
                        if query.get(key).get('index') == 1:

                            if key in query.keys():
                                if 'thumbnail' in query.get(key).keys():
                                    if 'source' in query.get(key).get('thumbnail').keys():
                                        url = query.get(key).get('thumbnail').get('source')

                                        print('getting image for {}, {}'.format(city.city,
                                                                                city.state))
                                        print('we got the first index {}'.format(url))


                                        city_obj = City.objects.get(city=city.city,
                                                                    state=city.state)
                                        city_obj.img_url = url
                                        city_obj.save(update_fields=['img_url'])

