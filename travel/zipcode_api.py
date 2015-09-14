import urllib
import json
import requests
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

        # print(location_list)
        #
        # # headers = {'api-key' : 'vedaf2gfvgknc38cbkk4z7az'}
        # client_secret = 'UgzJEgNWrD4zUUvNPSJQpKuFqSyfbb9ajG3EqYj2E7J3D'
        # client_id = 'vedaf2gfvgknc38cbkk4z7az'
        #
        # headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        # data = {'client_secret': client_secret,
        #         'grant_type': 'client_credentials',
        #         'client_id': client_id}
        # auth_url = 'https://connect.gettyimages.com/oauth2/token'
        # response = requests.post(auth_url,headers=headers,data=urllib.parse.urlencode(data))
        # result = json.loads(response.text)
        # access_token = result['access_token']
        #
        # print('the access token is {}'.format(access_token))
        #
        # for each in location_list:
        #     response = requests.get('https://connect.gettyimages.com/v3/'
        #                             'search/images?phrase=iconic images of'\
        #                             ' {}, {}'.\
        #                             format(each.get('city'),
        #                                     each.get('state')), headers)
        #
        #     city_data = response.json()
        #     print(city_data)

        # for each in location_list:
        #     print(each.get('city'))
        #     response = requests.get('https://connect.gettyimages.com/v3/'
        #                             'search/images?phrase=iconic images of'\
        #                             ' {}, {}'.\
        #                             format(each.get('city'),
        #                                    each.get('state')),
        #                             headers)
        #
        #     city_data = response.json()
        #     print(city_data)

        #     if 'result_count' in city_data.keys():
        #         if city_data.get('result_count') > 0:
        #             url = city_data.get('images').get('display_sizes').get('uri')
        #
        #             print('the image url for {} is {}'.format(city.city, url))

    return location_list
