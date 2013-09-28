from django.shortcuts import render_to_response
from django.shortcuts import render

def Home(request):
    return render_to_response('home.html', locals())

def ClientAccess(request):
    return render_to_response('client_access.html', locals())