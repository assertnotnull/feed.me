import urllib2
import json
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from yellowapi import YellowAPI

def index(request):
    return render(request, 'index.html')

def wajam_search(query, **kwargs):
    query = query.format(kwargs)
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

def search_wajam(request, resturant, page=1):
    if page > 1:
        wajamurl = 'https://api.wajam.com/trial/v1/search?q={query}&offset={offset}'
    else:
        wajamurl = 'https://api.wajam.com/trial/v1/search?q={query}}'
    result = {'wajam' : wajam_search(wajamurl, query='games', offset=page)}
    paginator = Paginator(result['results'], result['next_offset'])
    try:
        paged_result = paginator.page(page)
    except EmptyPage:
        paged_result = wajam_search()
    return render(request, 'wajam.html', paged_result)
