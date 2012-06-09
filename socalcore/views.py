from django.shortcuts import render_to_response, render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def search(request):
    return HttpResponse('ca marche')
