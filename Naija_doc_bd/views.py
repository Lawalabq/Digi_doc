from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def welcomeView(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Change 'home' to your desired redirect URL name
        return redirect('home')
    else:
        messages.error(request, 'Invalid username or password.')
    context = {}
    return render(request, 'naijaddoc_bd\landing_page.html', context)
