from django.test import TestCase

# Create your tests here.
from travel.utils import reduce_location_list, apply_user_filter


class UtilMethodTest(TestCase):

    def test_reduce_location_list_no_reduce(self):
        distance = 29
        location_list = [{'city': 'Las Vegas',
                         'state': 'NV',
                         'distance': 13}]
        result_list = [('Las Vegas', 'NV', 13)]

        self.assertTrue(
            reduce_location_list(distance, location_list) == result_list,
            "List is not reduced")

    def test_reduce_location_list_is_reduced(self):
        distance = 100
        location_list = [{'city': 'Las Vegas',
                         'state': 'NV',
                         'distance': 89},
                         {'city':'this city',
                          'state': 'this state',
                          'distance': 99},
                         {'city': 'this city2',
                          'state': 'this state2',
                          'distance': 25}]
        result_list = [('Las Vegas','NV',89),
                       ('this city', 'this state', 99)]

        self.assertTrue(
            reduce_location_list(distance, location_list) == result_list,
            "List was reduced")

    def test_apply_user_filter_no_list(self):
        city_list = []

        self.assertTrue(
            apply_user_filter('None', city_list) == [], "No list to filter")

    def test_apply_user_filter_hotel(self):
        city_list = [('Death Valley', 'CA', 95.322),
                     ('Fort Irwin', 'CA', 93.842),
                     ('Ludlow', 'CA', 98.195),
                     ('Alamo', 'NV', 88.591),
                     ('Essex', 'CA', 75.049),
                     ('Needles', 'CA', 84.451)]

        return_list = [('Needles', 'CA', 84.451),
                        ('Death Valley', 'CA', 95.322)
                       ]

        print('the return city tuple list is {}'.
              format(apply_user_filter('Hotel Price', city_list)))

        self.assertTrue(
            apply_user_filter('Hotel Price', city_list) == return_list,
            "List filtered out cities with no hotels")


#     def test_build_filter_dict(self):
#         self.assertFalse()
#
#
# class UserViewTests(TestCase):
#     def test_create_user_404(self):
#         url = reverse('detail_rater', args=[100])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404, msg='not found')
#
#     def test_user_profile(self):
#         test_user = User.objects.create_user('test', 'test@test.com', 'pass')
#         test_user.save()
#         time = timezone.now()
#         rating = Rating(rater=1, movie=3, rating=5, timestamp=time)
#         rating.save()
#
#         response = self.client.get(reverse('detail_rater', args=[rater.id]))
#         self.assertContains(response, 'Testing')
#
#
# class CityViewTests(TestCase):
#     def test_city_detail(self):
#         url = reverse('detail_rater', args=[100])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404, msg='not found')
#
#     def test_user_profile(self):
#         test_user = User.objects.create_user('test', 'test@test.com', 'pass')
#         test_user.save()
#         time = timezone.now()
#         rating = Rating(rater=1, movie=3, rating=5, timestamp=time)
#         rating.save()
#
#         response = self.client.get(reverse('detail_rater', args=[rater.id]))
#         self.assertContains(response, 'Testing')