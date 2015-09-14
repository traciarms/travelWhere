from functools import reduce
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q, F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, CreateView
import operator
from travel.zipcode_api import call_zipcode_api
from travel.forms import InitSearchForm, CustomerCreationForm, \
    LoggedInSearchForm, CustomerProfile
from travel.models import Customer, City, CityClick, Rating
from travel.utils import apply_user_filter, build_filter_dict, \
    reduce_location_list, find_user_clicked


def create_user(request):
    """
        This view creates the customer gets the registration page and
        posts to the profile page after creation
        :param request:
        :return:
    """
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
                # return HttpResponseRedirect(reverse('profile',
                #                                      args=[user.customer.id]))
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect(reverse('index'))
    else:
        form = CustomerCreationForm()

    return render(request, 'registration/registration.html', {'form': form})


class CityDetail(DetailView):
    """
        This view creates the city detail view.  Loads up all the detail
        information from the database.
    """
    model = City
    pk_url_kwarg = 'city_id'
    template_name = 'city_detail.html'

    def get(self, request, *args, **kwargs):
        city = super(CityDetail, self).get_object()

        if self.request.user.is_authenticated():
            customer = self.request.user.customer
            try:
                city_click = CityClick.objects.get(city=city, customer=customer)
                city_click.num_clicks = F('num_clicks') + 1

            except CityClick.DoesNotExist:
                city_click = CityClick.objects.create(city=city, customer=customer,
                                              num_clicks=1)
            city_click.save()

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        city = self.object
        context = super(CityDetail, self).get_context_data(**kwargs)
        city = City.objects.get(pk=city.id)

        outdoors_trails = len(city.outdoorrecreation_set.filter(
                name__icontains='trail'))
        outdoors_mountain_resorts = len(city.outdoorrecreation_set.filter(
                name__icontains='mountain resort'))
        outdoors_campground = len(city.outdoorrecreation_set.filter(
                name__icontains='campground'))
        outdoors_state_park = len(city.outdoorrecreation_set.filter(
                name__icontains='state park'))
        outdoors_peak = len(city.outdoorrecreation_set.filter(
                Q(name__icontains='peak') | Q(name__icontains='lookout')))
        outdoors_lake = len(city.outdoorrecreation_set.filter(
                name__icontains='lake'))
        outdoors_other = len(city.outdoorrecreation_set.exclude(reduce(
                                operator.or_,
                                    (Q(name__icontains='trail'),
                                     Q(name__icontains='mountain resort'),
                                     Q(name__icontains='campground'),
                                     Q(name__icontains='state park'),
                                     Q(name__icontains='peak'),
                                     Q(name__icontains='lookout'),
                                     Q(name__icontains='lake')))))
        context['outdoors_trails'] = outdoors_trails
        context['outdoors_mountain_resorts'] = outdoors_mountain_resorts
        context['outdoors_campground'] = outdoors_campground
        context['outdoors_state_park'] = outdoors_state_park
        context['outdoors_peak'] = outdoors_peak
        context['outdoors_lake'] = outdoors_lake
        context['outdoors_other'] = outdoors_other
        context['outdoor'] = ((outdoors_trails > 0) or
                              (outdoors_mountain_resorts > 0) or
                              (outdoors_campground > 0) or
                              (outdoors_state_park > 0) or
                              (outdoors_peak > 0) or
                              (outdoors_lake > 0) or
                              (outdoors_other > 0))

        hotels_lt50 = len(city.hotel_set.filter(high_rate__lt=50))
        hotels_50_100 = len(city.hotel_set.filter(low_rate__gt=50,
                                                  high_rate__lt=100))
        hotels100_125 = len(city.hotel_set.filter(low_rate__gt=100,
                                                  high_rate__lt=125))
        context['hotels'] = ((hotels_lt50 > 0) or
                             (hotels_50_100 > 0) or
                             (hotels100_125 > 0))
        context['hotels_lt50'] = hotels_lt50
        context['hotels_50_100'] = hotels_50_100
        context['hotels100_125'] = hotels100_125

        restaurants4 = len(city.restaurant_set.filter(rating=4.0))
        restaurants4_5 = len(city.restaurant_set.filter(rating=4.5))
        restaurants5 = len(city.restaurant_set.filter(rating=5.0))
        context['restaurants4'] = restaurants4
        context['restaurants4_5'] = restaurants4_5
        context['restaurants5'] = restaurants5
        context['restaurants'] = ((restaurants4 > 0) or
                                  (restaurants4_5 > 0) or
                                  (restaurants5 > 0))

        events_festivals = \
            len(city.event_set.filter(title__icontains='fest'))
        events_music = \
            len(city.event_set.exclude(title__icontains='fest'))
        context['events_festivals'] = events_festivals
        context['events_music'] = events_music
        context['music'] = ((events_festivals > 0) or
                            (events_music > 0))

        nights_pub = \
            len(city.nightlife_set.filter(category__icontains='pub'))
        nights_bar = \
            len(city.nightlife_set.filter(category__icontains='bar'))
        nights_sports_bar = \
            len(city.nightlife_set.filter(category__icontains='sports bar'))
        nights_music_venues = \
            len(city.nightlife_set.filter(category__icontains='music venue'))
        nights_night_club = \
            len(city.nightlife_set.filter(category__icontains='night club'))
        context['nights_pub'] = nights_pub
        context['nights_bar'] = nights_bar
        context['nights_sports_bar'] = nights_sports_bar
        context['nights_music_venues'] = nights_music_venues
        context['nights_night_club'] = nights_night_club
        context['nights'] = ((nights_pub > 0) or
                             (nights_bar > 0) or
                             (nights_sports_bar > 0) or
                             (nights_music_venues > 0) or
                             (nights_night_club > 0))

        return context


class UserProfile(UpdateView):
    """
        This is the customer profile view
    """
    model = Customer
    form_class = CustomerProfile
    pk_url_kwarg = 'customer_id'
    template_name = 'profile.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


def location_search(request):
    """
        This is the search view.  It calls the zip code api with the
        starting location of the user and the distance to search.

        It reduces the list to the outer 25% of the radius

        It also applies any filter if the user selected one and then
        builds the dictionary with info for the template
        :param request:
        :return:
    """
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
                selected_filter = data['user_filter']
                filter = True
            else:
                selected_filter = 'None'
                filter = False

            location_list = call_zipcode_api(zipcode, distance)

            city_list = reduce_location_list(distance, location_list)

            city_event_list = apply_user_filter(selected_filter, city_list)

            city_dict_list = build_filter_dict(selected_filter,
                                               city_event_list,
                                               request.user)

            city_click_list = find_user_clicked(selected_filter)

            context = {'city_dict': city_dict_list,
                       'filter': filter,
                       'selected_filter': selected_filter,
                       'city_click_list': city_click_list}
            return render(request, 'city_list.html', context)

        else:
            context = {'form': form}

            return render(request, 'index.html', context)


class CreateRating(CreateView):
    model = Rating
    fields = ('rating',)
    success_url = reverse_lazy('city_detail')
    template_name = "create_rating.html"

    def get_success_url(self):
        return reverse('city_detail',
                       kwargs={'city_id': self.kwargs.get('city_id', None)})

    def get_context_data(self, **kwargs):
        context = super(CreateRating, self).get_context_data(**kwargs)
        context['city'] = City.objects.get(pk=self.kwargs.get('city_id', None))
        return context

    def form_valid(self, form):
        form.instance.customer_id = self.request.user.customer.id
        form.instance.city_id = self.kwargs.get('city_id', None)
        form.instance.rating = form.cleaned_data.get('rating', None)
        return super(CreateRating, self).form_valid(form)