from django.shortcuts import render_to_response
from django.shortcuts import render

def home(request):
    return render_to_response('home.html', locals())

def client_access(request):
    return render_to_response('client_access.html', locals())