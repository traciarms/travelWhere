import urllib
import json
import requests
from travel.models import City
from travelWhere.settings import ZIPCODES_API_KEY


def call_zipcode_api(zipcode, distance):
    """
        This method is called from the search view - it calls the zipcode
        api and finds all the cities within the given distance

        :param zipcode:
        :param distance:
        :return: location list from the api
    """
    response = requests.get('https://www.zipcodeapi.com/rest/{}/radius.json/'\
                            '{}/{}/mile'.\
                format(ZIPCODES_API_KEY, zipcode, distance))

    location_list = []
    locations = response.json()

    if 'zip_codes' in locations.keys():
        location_list = locations['zip_codes']


    # response = requests.get('https://en.wikipedia.org/w/api.php?format'
    #                         '=json&action=query&generator=search&'
    #                         'gsrnamespace=0&gsrsearch=Broadbent%2COR&'
    #                         'gsrlimit=10&prop=pageimages|extracts&'
    #                         'pilimit=max&exintro&explaintext&exsentences=1&'
    #                         'exlimit=max&pithumbsize=300')
    #
    # wiki = response.json()
    # query = wiki.get('query').get('pages')
    #
    # for key in query.keys():
    #     if query.get(key).get('index') == 1:
    #         print('we got the first index {}'.format(query.get(key).get('thumbnail').get('source')))
    # foo = 'bar'

    return location_list
