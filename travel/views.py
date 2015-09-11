from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView
from travel.api import call_zipcode_api
from travel.forms import InitSearchForm, CustomerCreationForm, \
    LoggedInSearchForm, CustomerProfile
from travel.models import Customer, City

# Create your views here.
from travel.utils import apply_user_filter, build_filter_dict, \
    reduce_location_list


def create_user(request):
    if request.method == "POST":
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = form.save()
            customer = Customer()
            customer.user = user
            customer.first_name = data['first_name']
            customer.last_name = data['last_name']
            customer.address = data['address']
            customer.city = data['city']
            customer.state = data['state']
            customer.zip_code = data['zip_code']
            customer.user_filter = data['user_filter']
            customer.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            if user is not None:
                if user.is_active:
                    login(request, user)

            if request.user.is_authenticated():
                return HttpResponseRedirect(reverse('profile',
                                                     args=[user.customer.id]))
            else:
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
        context['restaurants4'] = len(city.restaurant_set.filter(rating=4.0))
        context['restaurants4_5'] = len(city.restaurant_set.filter(rating=4.5))
        context['restaurants5'] = len(city.restaurant_set.filter(rating=5.0))

        context['outdoors_trails'] = \
            len(city.outdoorrecreation_set.filter(name__icontains='trail'))
        context['outdoors_mountain_resorts'] = \
            len(city.outdoorrecreation_set.filter(name__icontains='mountain resort'))
        context['outdoors_campground'] = \
            len(city.outdoorrecreation_set.filter(name__icontains='campground'))
        context['outdoors_state_park'] = \
            len(city.outdoorrecreation_set.filter(name__icontains='state park'))
        context['outdoors_peak'] = \
            len(city.outdoorrecreation_set.filter(Q(name__icontains='peak') |
                                                  Q(name__icontains='lookout')))
        context['outdoors_lake'] = \
            len(city.outdoorrecreation_set.filter(name__icontains='lake'))

        context['hotels_lt50'] = len(city.hotel_set.filter(high_rate__lt=50))
        context['hotels_50_100'] = len(city.hotel_set.filter(low_rate__gt=50,
                                                             high_rate__lt=100))
        context['hotels100_125'] = len(city.hotel_set.filter(low_rate__gt=100,
                                                             high_rate__lt=125))

        context['events_festivals'] = \
            len(city.event_set.filter(title__icontains='fest'))
        context['events_music'] = \
            len(city.event_set.exclude(title__icontains='fest'))

        context['nights_pub'] = \
            len(city.nightlife_set.filter(category__icontains='pub'))
        context['nights_bar'] = \
            len(city.nightlife_set.filter(category__icontains='bar'))
        context['nights_sports_bar'] = \
            len(city.nightlife_set.filter(category__icontains='sports bar'))
        context['nights_music_venues'] = \
            len(city.nightlife_set.filter(category__icontains='music venue'))
        context['nights_night_club'] = \
            len(city.nightlife_set.filter(category__icontains='night club'))
        return context


class UserProfile(UpdateView):
    model = Customer
    form_class = CustomerProfile
    pk_url_kwarg = 'customer_id'
    template_name = 'profile.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


def location_search(request):

    if request.method == 'GET':
        if request.user.is_authenticated():
            form = LoggedInSearchForm(
                initial={'user_filter': request.user.customer.user_filter})
            # form = LoggedInSearchForm()
        else:
            form = InitSearchForm()
        context = {'form': form}

        return render(request, 'index.html', context)

    if request.method == 'POST':
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
                user_filter = 'None'
                filter = False

            location_list = call_zipcode_api(zipcode, distance)

            city_list = reduce_location_list(distance, location_list)
            city_dict_list = []

            city_event_list = apply_user_filter(user_filter, city_list)

            # if not filter:
            #
            #     # for city, state, dist, trail, event, rest in city_event_list:
            #     for trail, event, rest, city, state in city_event_list:
            #         city = City.objects.get(city=city, state=state)
            #         city_dict = {'city': city,
            #                      # 'dist': dist,
            #                      'Stats':
            #                          [{'Label': 'Number of Outdoor Recreation '
            #                             'activities',
            #                             'number': trail},
            #                           {'Label': 'Number of Events such as '
            #                             'concerts or festivals',
            #                             'number': event},
            #                           {'Label': 'Number of Top rated '
            #                             'restaurants (rated 4.0 or '
            #                             'higher)',
            #                             'number': rest}]
            #                     }
            #         city_dict_list.append(city_dict)
            # else:
            city_dict_list = build_filter_dict(user_filter, city_event_list)

            context = {'city_dict': city_dict_list,
                       'filter': filter}
            return render(request, 'city_list.html', context)

        else:
            context = {'form': form}

            return render(request, 'index.html', context)
