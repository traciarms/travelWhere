from functools import reduce
from django.db.models import Q, Count
import operator
from travel.models import City, CityClick

filter_dict = {'None': 0,
               'Hotel Price': 3,
               'Restaurant Rating': 2,
               'Outdoor Recreation': 0,
               'Events/Concerts': 1,
               'Night Life': 4}


def reduce_location_list(distance, location_list):
    """
        This method takes the list of locations and reduces it to the
        outer 25% of the radius and returns the reduced list
        :param distance:
        :param location_list:
        :return:
    """
    city_list = []

    if distance > 30:
        min_dist = distance * .75
    else:
        min_dist = 0

    for each in location_list:
        if each['distance'] > min_dist:
            city_state = [(x[0], x[1]) for x in city_list]
            if (each['city'], each['state']) not in city_state:
                city_list.append((each['city'], each['state'],
                                  each['distance']))

    return city_list


def find_user_clicked(selected_filter):
    """
        This method will return a list of top cities that users with
        the same stored filter have clicked on, this list will be used
        to suggest other cities to the current user.
    :param selected_filter:
    :return:
    """
    if selected_filter == 'None':
        selected_filter = 'Outdoor Recreation'
    city_click_list = CityClick.objects.\
        filter(customer__user_filter=selected_filter).\
        order_by('-num_clicks')[:10]

    return city_click_list


def apply_user_filter(user_filter, city_list):
    """
        This method applies the filter selected by the user to the list
        passed in.  It returns the filtered list.
        :param user_filter:
        :param city_list:
        :return:
    """
    city_tuple_list = []
    if len(city_list) > 0:
        query = reduce(operator.or_,
                       (Q(city=city, state=state)
                        for city, state, dist in city_list))

        city_list_num_hotels = City.objects.filter(query).annotate(
            num_hotels=Count('hotel__hotel_id'))
        city_list_num_events = City.objects.filter(query).annotate(
            num_events=Count('event__eventful_id'))
        city_list_num_trails = City.objects.filter(query).annotate(
            num_trails=Count('outdoorrecreation__id'))
        city_list_num_clubs = City.objects.filter(query).annotate(
            num_clubs=Count('nightlife__yelp_id'))
        city_list_num_rests = City.objects.filter(query).annotate(
            num_rests=Count('restaurant__yelp_id'))

        for num_hotels, num_events, num_trails, num_clubs, num_rests in \
                zip(city_list_num_hotels,
                    city_list_num_events,
                    city_list_num_trails,
                    city_list_num_clubs,
                    city_list_num_rests):

            if user_filter == 'Hotel Price' and num_hotels.num_hotels == 0:
                continue
            elif user_filter == 'Restaurant Rating' and \
                 num_rests.num_rests == 0:
                continue
            elif user_filter == 'Events/Concerts' and \
                 num_events.num_events == 0:
                continue
            elif user_filter == 'Night Life' and num_clubs.num_clubs == 0:
                continue
            elif ((user_filter == 'Outdoor Recreation' or
                   user_filter == 'None') and num_trails.num_trails == 0):
                continue
            else:
                city_tuple_list.append((num_trails.num_trails,
                                        num_events.num_events,
                                        num_rests.num_rests,
                                        num_hotels.num_hotels,
                                        num_clubs.num_clubs,
                                        num_events.city,
                                        num_events.state))

    sort_index = filter_dict[user_filter]
    city_tuple_list.sort(key=lambda x: x[sort_index], reverse=True)
    city_list = city_tuple_list[:5]

    return city_list


def build_template_dict(city_event_list, user):
    """
        This method builds the dictionary to pass to the template for
        rendering.  It takes a city event list and returns the dictionary
        that the template will display.

        :param city_event_list:
        :param user:
        :return:
    """
    city_dict_list = []
    for trail, event, rest, hotel, club, city, state in city_event_list:
        city = City.objects.get(city=city, state=state)
        rating = city.get_avg_rating().get('rating')
        if rating is not None:
            rating_range = range(int(rating))
        else:
            rating_range = 0
        has_rated = (user.is_authenticated and
                     user.customer.has_rated_city(city.id))

        city_dict = {'city': city,
                     'rating': rating,
                     'range': rating_range,
                     'has_rated': has_rated,
                     'Stats':
                         [{'Label': 'Number of Outdoor Recreation '
                           'activities',
                           'number': trail},
                          {'Label': 'Number of Events such as '
                           'concerts or festivals',
                           'number': event},
                          {'Label': 'Number of Top rated '
                           'restaurants (rated 4.0 or '
                           'higher)',
                           'number': rest},
                          {'Label': 'Number low priced hotels (under $125)',
                           'number': hotel},
                          {'Label': 'Number of Night clubs',
                           'number': club}]}
        city_dict_list.append(city_dict)

    return city_dict_list


def get_outdoor_context(city):
    """
    This method loads the outdoor data for a given city into context
    :param city:
    :return:
    """
    context = {}
    outdoors_trails = city.outdoorrecreation_set.\
        filter(name__icontains='trail')
    outdoors_mountain_resorts = city.outdoorrecreation_set.\
        filter(name__icontains='mountain resort')
    outdoors_campground = city.outdoorrecreation_set.\
        filter(name__icontains='campground')
    outdoors_state_park = city.outdoorrecreation_set.\
        filter(name__icontains='state park')
    outdoors_peak = city.outdoorrecreation_set.\
        filter(Q(name__icontains='peak') | Q(name__icontains='lookout'))
    outdoors_lake = city.outdoorrecreation_set.\
        filter(name__icontains='lake')
    outdoors_other = city.outdoorrecreation_set.\
        exclude(reduce(operator.or_, (Q(name__icontains='trail'),
                                      Q(name__icontains='mountain resort'),
                                      Q(name__icontains='campground'),
                                      Q(name__icontains='state park'),
                                      Q(name__icontains='peak'),
                                      Q(name__icontains='lookout'),
                                      Q(name__icontains='lake'))))
    context['outdoors_trails'] = outdoors_trails
    context['num_outdoors_trails'] = len(outdoors_trails)
    context['outdoors_mountain_resorts'] = outdoors_mountain_resorts
    context['num_outdoors_mountain_resorts'] = len(outdoors_mountain_resorts)
    context['outdoors_campground'] = outdoors_campground
    context['num_outdoors_campground'] = len(outdoors_campground)
    context['outdoors_state_park'] = outdoors_state_park
    context['num_outdoors_state_park'] = len(outdoors_state_park)
    context['outdoors_peak'] = outdoors_peak
    context['num_outdoors_peak'] = len(outdoors_peak)
    context['outdoors_lake'] = outdoors_lake
    context['num_outdoors_lake'] = len(outdoors_lake)
    context['outdoors_other'] = outdoors_other
    context['num_outdoors_other'] = len(outdoors_other)
    context['show_outdoor'] = ((len(outdoors_trails) > 0) or
                               (len(outdoors_mountain_resorts) > 0) or
                               (len(outdoors_campground) > 0) or
                               (len(outdoors_state_park) > 0) or
                               (len(outdoors_lake) > 0) or
                               (len(outdoors_other) > 0))
    return context


def get_hotel_context(city):
    """
    This method loads the hotel data for a given city into context
    :param city:
    :return:
    """
    context = {}
    hotels_lt50 = city.hotel_set.filter(high_rate__lt=50)
    hotels_50_100 = city.hotel_set.filter(low_rate__gt=50,
                                          high_rate__lt=100)
    hotels100_125 = city.hotel_set.filter(low_rate__gt=100,
                                          high_rate__lt=125)
    context['hotels_lt50'] = hotels_lt50
    context['num_hotels_lt50'] = len(hotels_lt50)
    context['hotels_50_100'] = hotels_50_100
    context['num_hotels_50_100'] = len(hotels_50_100)
    context['hotels100_125'] = hotels100_125
    context['num_hotels100_125'] = len(hotels100_125)
    context['show_hotels'] = ((len(hotels_lt50) > 0) or
                              (len(hotels_50_100) > 0) or
                              (len(hotels100_125) > 0))

    return context


def get_restaurant_context(city):
    """
    This method loads the restaurant data for a given city into context
    :param city:
    :return:
    """
    context = {}
    restaurants4 = city.restaurant_set.filter(rating=4.0)
    restaurants4_5 = city.restaurant_set.filter(rating=4.5)
    restaurants5 = city.restaurant_set.filter(rating=5.0)
    context['restaurants4'] = restaurants4
    context['num_restaurants4'] = len(restaurants4)
    context['restaurants4_5'] = restaurants4_5
    context['num_restaurants4_5'] = len(restaurants4_5)
    context['restaurants5'] = restaurants5
    context['num_restaurants5'] = len(restaurants5)
    context['show_restaurants'] = ((len(restaurants4) > 0) or
                                   (len(restaurants4_5) > 0) or
                                   (len(restaurants5) > 0))
    return context


def get_music_context(city):
    """
    This method loads the music/events data for a given city into context
    :param city:
    :return:
    """
    context = {}
    events_festivals = \
        city.event_set.filter(title__icontains='fest')
    events_music = \
        city.event_set.exclude(title__icontains='fest')
    context['events_festivals'] = events_festivals
    context['num_events_festivals'] = len(events_festivals)
    context['events_music'] = events_music
    context['num_events_music'] = len(events_music)
    context['show_music'] = ((len(events_festivals) > 0) or
                             (len(events_music) > 0))
    return context


def get_night_context(city):
    """
    This method loads the nightlife data for a given city into context
    :param city:
    :return:
    """
    context = {}
    nights_pub = city.nightlife_set.filter(category__icontains='pub')
    nights_bar = city.nightlife_set.filter(category__icontains='bar')
    nights_sports_bar = \
        city.nightlife_set.filter(category__icontains='sports bar')
    nights_music_venues = \
        city.nightlife_set.filter(category__icontains='music venue')
    nights_night_club = \
        city.nightlife_set.filter(category__icontains='night club')
    context['nights_pub'] = nights_pub
    context['num_nights_pub'] = len(nights_pub)
    context['nights_bar'] = nights_bar
    context['num_nights_bar'] = len(nights_bar)
    context['nights_sports_bar'] = nights_sports_bar
    context['num_nights_sports_bar'] = len(nights_sports_bar)
    context['nights_music_venues'] = nights_music_venues
    context['num_nights_music_venues'] = len(nights_music_venues)
    context['nights_night_club'] = nights_night_club
    context['num_nights_night_club'] = len(nights_night_club)
    context['show_nights'] = ((len(nights_pub) > 0) or
                              (len(nights_bar) > 0) or
                              (len(nights_sports_bar) > 0) or
                              (len(nights_music_venues) > 0) or
                              (len(nights_night_club) > 0))
    return context
