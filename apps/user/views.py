from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from apps.user.forms import loginForm

def user_login(request):
    if request.method == "POST":
        form = loginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            
            if user and user is not None and user.is_active:
                login(request, user)
                return redirect('/galleries/')

        return render(request, 'user_login.html', {'form': form})
                     
    form = loginForm()
    return render(request, 'user_login.html', {'form': form})
    
def user_logout(request):
    logout(request)

    return redirect('/')