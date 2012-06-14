import urllib2
import json
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from yellowapi import YellowAPI

def index(request):
    return render(request, 'index.html')

def wajam_search(query, args):
    query = query.format(args)
    wajam_json = json.load(urllib2.urlopen(query))
    return wajam_json

def yellow_search(api, arg, location):
    data = api.find_business('Restaurant ' + arg, 'cZ' + location, 123, page_len=5);
    listings = json.loads(data)['listings']
    return listings

def search(request, category, location):
    yellow = YellowAPI('s73bf2pqaswz5a6secydtsth', test_mode=True, format='JSON')
    result = {'yellow' : yellow_search(yellow, category, location)}
    return render(request, 'search.html', result)

def search_wajam(request, resturant):
    wajamurl = 'https://api.wajam.com/trial/v1/search?q={0}'
    if resturant is not '':
        result = {'wajam' : wajam_search(wajamurl, 'games')}
    else:
        result = None
    return render(request, 'wajam.html', result)
