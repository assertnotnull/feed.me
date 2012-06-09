from django.shortcuts import render_to_response, render

def index(request):
    return render(request, 'index.html')