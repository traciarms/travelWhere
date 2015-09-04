from travel.api import call_trails_api, call_eventful_api, call_food_api, \
    call_expedia_api, call_nightlife_api
from travel.models import City


def reduce_location_list(distance, location_list):
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


def apply_default_filters(city, state, dist):
    city_tuple = ()

    num_trails = call_trails_api(city, state)
    if num_trails != 0:
        num_events = call_eventful_api(city, state)

        # if num_events != 0:
        num_rests = call_food_api(city, state)

            # if num_rests != 0:
        city_tuple = (city, state, dist, num_trails, num_events,
                        num_rests)

    return city_tuple


def apply_user_filter(filter, city, state, dist):

    if filter == 'Hotel Price':
        num_hotels = call_expedia_api(city, state)
        if num_hotels > 0:
            num_trails = call_trails_api(city, state)
            num_events = call_eventful_api(city, state)
            return (city, state, dist, num_hotels, num_trails, num_events)
        else:
            return ()
    elif filter == 'Restaurant Rating':
        num_rests = call_food_api(city, state)
        if num_rests > 0:
            num_trails = call_trails_api(city, state)
            num_events = call_eventful_api(city, state)
            return (city, state, dist, num_rests, num_trails, num_events)
        else:
            return ()
    elif filter == 'Events/Concerts':
        num_events = call_eventful_api(city, state)
        if num_events > 0:
            num_trails = call_trails_api(city, state)
            num_rests = call_food_api(city, state)
            return (city, state, dist, num_events, num_trails, num_rests)
        else:
            return ()
    elif filter == 'Night Life':
        num_clubs = call_nightlife_api(city, state)
        if num_clubs > 0:
            num_trails = call_trails_api(city, state)
            num_events = call_eventful_api(city, state)
            return (city, state, dist, num_clubs, num_trails, num_events)
        else:
            return ()
    else:
        num_trails = call_trails_api(city, state)
        if num_trails > 0:
            num_events = call_eventful_api(city, state)
            num_rests = call_food_api(city, state)
            return (city, state, dist, num_trails, num_events, num_rests)
        else:
            return ()


def build_filter_dict(filter, city_event_list):
    city_dict_list = []
    if filter == 'Hotel Price':
        for city, state, dist, hotel, trail, event in city_event_list:
            city = City.objects.get(city=city, state=state)
            city_dict = {'city': city,
                         'dist': dist,
                         'Stats':
                             [{'Label': 'Number low priced hotels (under '
                                        '$125)',
                                'number': hotel},
                              {'Label': 'Number of Outdoor Recreation '
                                        'activities',
                                'number': trail},
                              {'Label': 'Number of Events such as '
                                'concerts or festivals',
                                'number': event}]
                        }
            city_dict_list.append(city_dict)
    elif filter == 'Restaurant Rating':
        for city, state, dist, rest, trail, event in city_event_list:
            city = City.objects.get(city=city, state=state)
            city_dict = {'city': city,
                         'dist': dist,
                         'Stats':
                             [{'Label': 'Number of Top rated '
                                'restaurants (rated 4.0 or '
                                'higher)',
                                'number': rest},
                              {'Label': 'Number of Outdoor Recreation '
                                'activities',
                                'number': trail},
                              {'Label': 'Number of Events such as '
                                'concerts or festivals',
                                'number': event}]
                        }
            city_dict_list.append(city_dict)
    elif filter == 'Events/Concerts':
        for city, state, dist, event, trail, rest in city_event_list:
            city = City.objects.get(city=city, state=state)
            city_dict = {'city': city,
                         'dist': dist,
                         'Stats':
                             [{'Label': 'Number of Events such as '
                                'concerts or festivals',
                                'number': event},
                              {'Label': 'Number of Outdoor Recreation '
                                'activities',
                                'number': trail},
                              {'Label': 'Number of Top rated '
                                'restaurants (rated 4.0 or '
                                'higher)',
                                'number': rest}]
                        }
            city_dict_list.append(city_dict)
    elif filter == 'Night Life':
        for city, state, dist, club, trail, event in city_event_list:
            city = City.objects.get(city=city, state=state)
            city_dict = {'city': city,
                         'dist': dist,
                         'Stats':
                             [{'Label': 'Number of Night clubs',
                                'number': club},
                              {'Label': 'Number of Outdoor Recreation '
                                'activities',
                                'number': trail},
                              {'Label': 'Number of Events such as '
                                'concerts or festivals',
                                'number': event}]
                        }
            city_dict_list.append(city_dict)
    else:
        for city, state, dist, trail, event, rest in city_event_list:
            city = City.objects.get(city=city, state=state)
            city_dict = {'city': city,
                         'dist': dist,
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
                                'number': rest}]
                        }
            city_dict_list.append(city_dict)

    return city_dict_list