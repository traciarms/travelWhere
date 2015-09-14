from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from travel.views import CityDetail, UserProfile, CreateRating

urlpatterns = [
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page':"/"},
        name='logout'),
    url(r'^login/', auth_views.login,
        {'extra_context': {'next': '/'}}, name='login'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', 'travel.views.location_search', name='index'),
    url(r'^profile/(?P<customer_id>[0-9]+)/',
        UserProfile.as_view(), name='profile'),
    url(r'^registration', 'travel.views.create_user', name='registration'),
    url(r'^city_list', 'travel.views.location_search', name='city_list'),
    url(r'^city_detail/(?P<city_id>[0-9]+)/', CityDetail.as_view(),
        name='city_detail'),
    url(r'^create_rating/(?P<city_id>[0-9]+)/',
        CreateRating.as_view(), name='create_rating'),
    url(r'^admin/', include(admin.site.urls)),

]
