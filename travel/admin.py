from django.contrib import admin
from .models import City, Customer, Hotel


class CityAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'img_url')
    list_filter = ['city', 'state']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name',
                    'address', 'city', 'state', 'zip_code', 'user_filter')


class HotelAdmin(admin.ModelAdmin):
    list_display = ('city', 'hotel_id', 'name', 'address', 'loc_city',
                    'state', 'low_rate', 'high_rate', 'rating', 'url')

admin.site.register(City, CityAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Hotel, HotelAdmin)
