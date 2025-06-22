from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import os
from .models import Staff, Nurse, School
from django.contrib.auth import get_user_model

User = get_user_model()
UserModel = get_user_model()


def welcomeView(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    UserModel = get_user_model()

    user = authenticate(
        request=request, **{UserModel.USERNAME_FIELD: username, "password": password})
    print(user)
    if user is not None:
        login(request, user)
        # Change 'home' to your desired redirect URL name

        if user.role == 'Nurse':
            return redirect('nurse_home')
        elif user.role == 'Staff':
            return redirect('staff_home')
        else:
            return redirect('home')
            return redirect('nurse_home')
    else:
        messages.error(request, 'Invalid username or password.')
    context = {}
    return render(request, 'landing_page.html', context)


def SignupView(request):
    context = {}
    # Get all unique school names from Nurse model
    context['schools'] = School.objects.all()

    if request.method == 'POST':
        role = request.POST.get('role')
        username = request.POST.get('username')
        email = request.POST.get('email')
        # Assuming you're using password1
        password = request.POST.get('password1')
        school_id = request.POST.get('school')

        try:
            school = School.objects.get(id=int(school_id))
        except (School.DoesNotExist, ValueError, TypeError):
            messages.error(request, 'Invalid or missing school selection.')
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        if role == 'Staff':
            staff = Staff(user=user, school=school)
            staff.save()
            login(request, user)
            return redirect('staff_home')

        elif role == 'Nurse':
            nurse = Nurse(user=user, school=school)
            nurse.save()
            login(request, user)
            return redirect('nurse_home')

        else:
            messages.error(request, 'Invalid role selected.')
            return redirect('signup')

    return render(request, 'signup_page.html', context)


def nursehomeView(request):
    context = {}
    context['user'] = request.user
    return render(request, 'nurse_home.html', context)
