from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from apps.user.forms import loginForm


def user_login(request):
    if request.method == "POST":
        form = loginForm(request.POST)
        errors = []

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                errors.append('User "%s" does not exist.' % username)
                return render(request, 'user_login.html', {'form': form, 'errors': errors})

            if user and user is not None and user.is_active:
                login(request, user)
                return redirect('/galleries/')
            else:
                errors.append('Wrong password for "%s".' % username)
                return render(request, 'user_login.html', {'form': form, 'errors': errors})

        return render(request, 'user_login.html', {'form': form})

    form = loginForm()
    return render(request, 'user_login.html', {'form': form})


def user_logout(request):
    logout(request)

    return redirect('/')
