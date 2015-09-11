from functools import reduce
from django.db.models import Q, Count

import operator
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


def apply_user_filter(filter, city_list):
    print(city_list)

    if len(city_list) > 0:
        print('in here len is greater than 0')
        query = reduce(
                operator.or_,
                (Q(city=city, state=state)
                        for city, state, dist in city_list))

        print(query)
        print(City.objects.filter(query))
        city_list_num_hotels = City.objects.filter(query).annotate(
            num_hotels=Count('hotel__hotel_id'))
        print(city_list_num_hotels)
        city_list_num_events = City.objects.filter(query).annotate(
            num_events=Count('event__eventful_id'))
        city_list_num_trails = City.objects.filter(query).annotate(
            num_trails=Count('outdoorrecreation__id'))
        city_list_num_clubs = City.objects.filter(query).annotate(
            num_clubs=Count('nightlife__yelp_id'))
        city_list_num_rests = City.objects.filter(query).annotate(
            num_rests=Count('restaurant__yelp_id'))

        city_tuple_list = []

        if filter == 'Hotel Price':
            print('in here filter is hotel the city_hotel list {}'
                  .format(city_list_num_hotels))
            for num_hotels, num_trails, num_events in zip(city_list_num_hotels,
                                                         city_list_num_trails,
                                                         city_list_num_events):
                if num_hotels.num_hotels > 0:
                    city_tuple_list.append(
                            (num_hotels.num_hotels,
                              num_trails.num_trails,
                              num_events.num_events,
                              num_events.city,
                              num_events.state)
                        )
        elif filter == 'Restaurant Rating':
            for num_rests, num_trails, num_events in zip(city_list_num_rests,
                                                         city_list_num_trails,
                                                         city_list_num_events):
                if num_rests.num_rests > 0:
                    city_tuple_list.append(
                            (num_rests.num_rests,
                              num_trails.num_trails,
                              num_events.num_events,
                              num_events.city,
                              num_events.state)
                        )
        elif filter == 'Events/Concerts':
            for num_events, num_trails, num_rests in zip(city_list_num_events,
                                                         city_list_num_trails,
                                                         city_list_num_rests):

                if num_events.num_events > 0:
                    city_tuple_list.append(
                            (num_events.num_events,
                              num_trails.num_trails,
                              num_rests.num_rests,
                              num_events.city,
                              num_events.state)
                        )
        elif filter == 'Night Life':
            for num_clubs, num_trails, num_events in zip(city_list_num_clubs,
                                                         city_list_num_trails,
                                                         city_list_num_events):
                if num_clubs.num_clubs > 0:
                    city_tuple_list.append(
                            (num_clubs.num_clubs,
                              num_trails.num_trails,
                              num_events.num_events,
                              num_events.city,
                              num_events.state)
                        )
        else:
            for num_trails, num_events, num_rests in zip(city_list_num_trails,
                                                         city_list_num_events,
                                                         city_list_num_rests):
                if num_trails.num_trails > 0:
                    city_tuple_list.append(
                            (num_trails.num_trails,
                              num_events.num_events,
                              num_rests.num_rests,
                              num_events.city,
                              num_events.state)
                        )

        city_tuple_list.sort(key=lambda x: x[0], reverse=True)
        city_list = city_tuple_list[:5]

    return city_list


def build_filter_dict(filter, city_event_list):
    city_dict_list = []
    if filter == 'Hotel Price':
        for hotel, trail, event, city, state in city_event_list:
            city = City.objects.get(city=city, state=state)
            city_dict = {'city': city,
                         # 'dist': dist,
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
        for rest, trail, event,city, state in city_event_list:
            city = City.objects.get(city=city, state=state)
            city_dict = {'city': city,
                         # 'dist': dist,
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
        for event, trail, rest, city, state in city_event_list:
            city = City.objects.get(city=city, state=state)
            city_dict = {'city': city,
                         # 'dist': dist,
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
        for club, trail, event, city, state in city_event_list:
            city = City.objects.get(city=city, state=state)
            city_dict = {'city': city,
                         # 'dist': dist,
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
        for trail, event, rest, city, state in city_event_list:
            city = City.objects.get(city=city, state=state)
            city_dict = {'city': city,
                         # 'dist': dist,
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