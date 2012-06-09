from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from search import Search

def index(request):
    return render(request, 'index.html')

def search(request, category, location):
    return HttpResponse(Search.search(category, location))
