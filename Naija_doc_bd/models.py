from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = (
        ('staff', 'Staff'),
        ('nurse', 'Nurse'),
        ('school', 'School'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=30)
    email = models.EmailField()


class School(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)


class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    school = models.OneToOneField(School, on_delete=models.CASCADE)


class Student(models.Model):
    school = models.OneToOneField(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    medical_history = models.CharField(max_length=200)
    age = models.IntegerField()
    ROLE_CHOICES = (
        ('female', 'Female'),
        ('male', 'Male'),

    )
    sex = models.CharField(max_length=10, choices=ROLE_CHOICES)
    state = models.CharField(max_length=20)


class Drug(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)


class case(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    medications = {}
