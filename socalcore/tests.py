"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from views import yellow_search, wajam_search

from django.test import TestCase


class SimpleTest(TestCase):
    terme = 'Frite alors!'
    location = 'montreal'

    def test_yellow_api(self):
        result = yellow_search(self.terme, self.location)
        print result
        self.assertEqual(result[0].get('name'), 'Restaurant Frites Alors')

    def test_wajam_api(self):
        result = wajam_search(self.location)
        print result
        self.assertEqual(result)