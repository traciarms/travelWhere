"""travelWhere URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from travel.views import CityDetail, UserProfile

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
    url(r'^admin/', include(admin.site.urls)),

]
