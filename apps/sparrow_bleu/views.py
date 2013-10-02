from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html', locals())

def client_access(request):
    return render(request, 'client_access.html', locals())