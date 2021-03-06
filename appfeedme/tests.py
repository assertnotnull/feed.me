from yellowapi import YellowAPI
from views import yellow_search, wajam_search

from django.test import TestCase


class SimpleTest(TestCase):
    terme = 'Frite alors!'
    location = 'montreal'

    def test_yellow_api(self):
        #TODO a mocker
        yellow = YellowAPI('s73bf2pqaswz5a6secydtsth', test_mode=True, format='JSON')
        result = yellow_search(yellow, self.terme, self.location)
        self.assertEqual(result[0].get('name'), 'Restaurant Frites Alors')

    def test_wajam_api(self):
        #TODO a mocker
        wajamurl = 'https://api.wajam.com/trial/v1/search?q={0}'
        result = wajam_search(wajamurl, 'suchi')
        self.assertEqual(result.get('total_found'), 0)