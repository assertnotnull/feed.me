import urllib2
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from search import Search

def index(request):
    return render(request, 'index.html')

def wajam_search(place):
    query = 'https://api.wajam.com/trial/v1/search/places?q={0}'#&category={1}&type={3}'
    query.format(place)
    wajam_json = json.load(urllib2.urlopen(query))
    return wajam_json

def search(request, category, location):
    return HttpResponse(Search.search(category, location))
