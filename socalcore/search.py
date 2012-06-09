import sys
import json
from yellowapi import YellowAPI

class Search:

	@staticmethod
	def search(arg, location):
		
		api = YellowAPI('s73bf2pqaswz5a6secydtsth', test_mode=True, format='JSON')

		data = api.find_business('Restaurant ' + arg, 'cZ' + location, 123, page_len=5);

		listings = json.loads(data)['listings']
			
		script = "<script type=''text/javascript'>"
		ret = "<ul>"
		for business in listings:
			ret += "<li>" + business['name'] + "</li>"
			script += "map.addMarker({ lat: " + business['geoCode']['latitude'] + ",  lng: " + business['geoCode']['longitude'] + ", title: '" + business['name'] + "'});"
			
		ret += "</ul>"
		
		return ret + script;