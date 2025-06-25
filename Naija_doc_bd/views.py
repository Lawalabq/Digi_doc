from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import os
from .models import Staff, Nurse, School, Drug, Case, MedicationRecord

from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from .models import Student
from django.urls import reverse_lazy
from django.utils import timezone

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


def StudentCreateView(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        medical_history = request.POST.get('medical_history')
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        state = request.POST.get('state')
        nurse = Nurse.objects.get(user_id=int(request.user.id))
        school = School.objects.get(id=int(nurse.school_id))
        level = request.POST.get('level')
        student = Student(name=name, medical_history=medical_history,
                          age=age, sex=sex, state=state, school=school, level=level)
        student.save()
        return redirect('nurse_home')

    context = {}
    return render(request, 'student_form.html', context)


def CreatecaseView(request):
    if request.method == 'POST':
        notes = request.POST.get('notes')
        student_id = request.POST.get('student')
        student = Student.objects.get(id=student_id)
        date = timezone.now()
        case = Case(diagnosis=notes, date=date, student=student)
        case.save()

        total_forms = int(request.POST.get('medication-TOTAL_FORMS'))
        for i in range(total_forms):
            drug_id = request.POST.get(f'medication-{i}-drug')
            morning = request.POST.get(f'medication-{i}-morning') == 'on'
            afternoon = request.POST.get(f'medication-{i}-afternoon') == 'on'
            night = request.POST.get(f'medication-{i}-night') == 'on'
            days = request.POST.get(f'medication-{i}-days')

            # Only save if a drug is selected
            if drug_id:
                # Create MedicationRecord for this case
                MedicationRecord.objects.create(
                    case=case,  # replace with your created case object
                    drug_id=drug_id,
                    morning=morning,
                    afternoon=afternoon,
                    night=night,
                    days=days
                )

    context = {}
    context['students'] = Student.objects.all()
    context['drugs'] = Drug.objects.all()
    return render(request, 'create_case.html', context)


def ActivecaseView(request):
    context = {}
    return render(request, 'view_activecases.html', context)
