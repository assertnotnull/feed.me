# -*- coding: utf-8 -*-
import logging
import urllib2
import json
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from yellowapi import YellowAPI
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('appfeedme', 'templates'))
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def wajam_search(url, query, offset):
    url = url.format(query=query, offset=offset)
    logger.debug(url)
    wajam_json = json.load(urllib2.urlopen(url))
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
    offset = request.GET.get('offset', None)
    if offset is not None:
        wajamurl = 'https://api.wajam.com/trial/v1/search?q={query}&offset={offset}&count=1'
    else:
        wajamurl = 'https://api.wajam.com/trial/v1/search?q={query}&count=1'
    result = {'wajam' : wajam_search(wajamurl, query='games', offset=offset)}
#    paginator = Paginator(result['results'], result['next_offset'])
#    try:
#        paged_result = paginator.page(page)
#    except EmptyPage:
#        paged_result = wajam_search()
    return render(request, 'wajam.html', result)
