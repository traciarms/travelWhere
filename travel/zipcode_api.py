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
    response = requests.get('https://www.zipcodeapi.com/rest/{}/radius.json/'
                            '{}/{}/mile'.
                            format(ZIPCODES_API_KEY, zipcode, distance))

    location_list = []
    locations = response.json()

    if 'zip_codes' in locations.keys():
        location_list = locations['zip_codes']

    return location_list
