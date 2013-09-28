from django.shortcuts import render, redirect
from django.contrib.auth import logout

def home(request):
    return render(request, 'home.html', locals())

def client_access(request):
    return render(request, 'client_access.html', locals())

from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
        
                return redirect('/galleries/')
            else:
                return redirect('/client-access/')
        else:
            return redirect('/client-access/')

def user_logout(request):
    logout(request)

    return redirect('/')