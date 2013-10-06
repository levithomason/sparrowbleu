from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html', locals())

def get_form_errors(form):
    errors = []

    for error in form.errors:
        errors.append(error)
    
    return errors