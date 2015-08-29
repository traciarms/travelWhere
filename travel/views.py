import null as null
from django.http import request
from django.shortcuts import render
from django.template import context
import rauth
import requests
from travel.forms import InitSearchForm
from travelWhere.settings import ZIPCODES_API_KEY, EVENTFUL_API_KEY, \
    TRAIL_API_KEY, YELP_API_KEY
# Create your views here.

# def avg_rating(request, select_category=None):
# -    category_list = Category.objects.all()
# -    movie_list = Movie.objects.exclude(rating=None)
# -    if select_category != 'None':
# -        movie_list = movie_list.filter(category__category__icontains=select_category)
# -    avg_rating = movie_list.annotate(
# -        average=Avg('rating__ratings')).order_by('-average')[:20]
# -
# -    return render(request, 'app1/avg_rating.html',
# -                  {'avg_rating': avg_rating,
# -                   'category_list': category_list,
# -                   'select_category': select_category})


# class SearchTwitterView(TemplateView):
    # template_name = "index.html"



def call_zipcode_api(zipcode, distance):
    response = requests.get('https://www.zipcodeapi.com/rest/{}/radius.json/{}/{}/mile'.\
                format(ZIPCODES_API_KEY, zipcode, distance))

    locations = response.json()
    location_list = locations['zip_codes']
    return location_list


def call_eventful_api(search_city):
    response = requests.get('http://api.eventful.com/json/events/search?app_key={}&l={}&c={},{}'.\
                            format(EVENTFUL_API_KEY, search_city,
                            'festivals_parades', 'music'))

    events = response.json()
    num_events = events['total_items']


    return num_events


def call_trails_api(search_city):
    response = requests.get('https://outdoor-data-api.herokuapp.com/api.json?api_key={}&q[city_eq]={}&radius=25'.\
                           format(TRAIL_API_KEY, search_city))

    trails = response.json()
    num_trails = len(trails['places'])

    return num_trails


def call_yelp_api(search_city):

    #Obtain these from Yelp's manage access page
    consumer_key = "xCvm07_lr5NIW-I4uVukzQ"
    consumer_secret = "6tSvvoI5wYmV_vH3Ws3JIFvXAr4"
    token = "5bfzpwor6paKASUGChfDSD9hAfHi99TZ"
    token_secret = "JcB8IUkCPkwEa3hX8BYl9AfLHYs"

    session = rauth.OAuth1Session(
        consumer_key = consumer_key, consumer_secret = consumer_secret,
        access_token = token, access_token_secret = token_secret)

    # request = session.get("http://api.yelp.com/v2/search",params=params)
    response = session.get('http://api.yelp.com/v2/search',
                           params={'term': 'food', 'location': search_city})

    yelp = response.json()
    high_rating_count = 0

    if 'error' not in yelp.keys():
        for business in yelp['businesses']:
            rating = business['rating']

            if rating >= 4:
                high_rating_count += 1

    return high_rating_count


def get_zipcode_dict(request, user_zipcode=null):
    # def get_context_data(self, **kwargs):
    #     context = super(SearchTwitterView, self).get_context_data(**kwargs)

    if request.method == 'GET':
        form = InitSearchForm()
        context = {'form': form}

        return render(request, 'index.html', context)

    if request.method == 'POST':
        location_list  = []
        city_list = []
        city_event_list = []
        form = InitSearchForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            distance = data['distance']
            zipcode = data['zip_code']
            location_list = call_zipcode_api(zipcode, distance)

            min_dist = distance * .75
            for each in location_list:
                if each['distance'] > min_dist:
                    city_list.append(each['city'])
            # location_list = location_dict['city']
            city_set = set(city_list)

            for city in city_set:

                num_trails = call_trails_api(city)
                if num_trails != 0:
                    num_events = call_eventful_api(city)

                    if num_events != '0':
                        num_rests = call_yelp_api(city)

                        if num_rests != 0:
                            city_event_list.append((city, num_trails, num_events, num_rests))

        context = {'city_list': city_event_list}

        # return HttpResponseRedirect(reverse('restaurant_profile',
        #                                         args=[user.restaurant.id]))

        return render(request, 'city_list.html', context)



# def playgame(request):
#
#     winner = ''
#     try:
#         game = Game.objects.get(completed=False)
#     except:
#         game = Game.objects.create(player1=User.objects.get(username='player1'),
#                                    player2=User.objects.get(username='player2'),
#                                    give_player=User.objects.get(username='player1'),
#                                    form_player=User.objects.get(username='player1'))
#     if request.method == 'GET':
#         form = WordForm()
#         context = {'game': game, 'form': form}
#         return render(request, 'index.html', context)
#
#     if request.method == 'POST':
#         form = WordForm(request.POST)
#         if request.user == game.give_player: