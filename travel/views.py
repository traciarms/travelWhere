from django.contrib.auth import authenticate
from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView
from travel.api import call_zipcode_api
from travel.forms import InitSearchForm, CustomerCreationForm, \
    LoggedInSearchForm
from travel.models import Customer, City, Restaurant, OutdoorRecreation, Hotel, \
    Event, NightLife

# Create your views here.
from travel.utils import apply_default_filters, apply_user_filter, \
    build_filter_dict, reduce_location_list


def create_user(request):
    if request.method == "POST":
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = form.save()
            customer = Customer()
            customer.user = user
            customer.address = data['address']
            customer.city = data['city']
            customer.state = data['state']
            customer.zip_code = data['zip_code']
            customer.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            login(request, user)

            return HttpResponseRedirect(reverse('index'))
    else:
        form = CustomerCreationForm()

    return render(request, 'registration/registration.html', {'form': form})


class CityDetail(DetailView):
    model = City
    pk_url_kwarg = 'city_id'
    template_name = 'city_detail.html'

    def get_context_data(self, **kwargs):
        city = self.object
        context = super(CityDetail, self).get_context_data(**kwargs)
        city = City.objects.get(pk=city.id)
        context['restaurants'] = city.restaurant_set.all()
        context['outdoors'] = city.outdoorrecreation_set.all()
        context['hotels'] = city.hotel_set.all()
        context['events'] = city.event_set.all()
        context['nights'] = city.nightlife_set.all()
        return context


def location_search(request):

    if request.method == 'GET':
        if request.user.is_authenticated():
            form = LoggedInSearchForm()
        else:
            form = InitSearchForm()
        context = {'form': form}

        return render(request, 'index.html', context)

    if request.method == 'POST':
        city_event_list = []
        if request.user.is_authenticated():
            form = LoggedInSearchForm(request.POST)
        else:
            form = InitSearchForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            distance = data['distance']
            zipcode = data['zip_code']

            if request.user.is_authenticated():
                user_filter = data['user_filter']

                filter = True
            else:
                filter = False

            location_list = call_zipcode_api(zipcode, distance)

            city_list = reduce_location_list(distance, location_list)
            city_dict_list = []

            for city, state, dist in city_list:
                if filter:
                    ret_tuple = apply_user_filter(user_filter,city,
                                                    state, dist)
                    if len(ret_tuple) > 0:
                        city_event_list.append(ret_tuple)
                else:
                    ret_tuple = apply_default_filters(city, state, dist)
                    if len(ret_tuple) > 0:
                        city_event_list.append(ret_tuple)

            city_event_list.sort(key=lambda x: x[3], reverse=True)
            city_event_list = city_event_list[:5]

            if not filter:

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
            else:
                city_dict_list = build_filter_dict(user_filter,
                                                   city_event_list)

            context = {'city_dict': city_dict_list,
                       'filter': filter}
            return render(request, 'city_list.html', context)

        else:
            context = {'form': form}

            return render(request, 'index.html', context)
