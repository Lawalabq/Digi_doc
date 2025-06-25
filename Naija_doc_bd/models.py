from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    ROLE_CHOICES = (
        ('staff', 'Staff'),
        ('nurse', 'Nurse'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=30)
    email = models.EmailField()
    objects = UserManager()


class School(models.Model):

    address = models.CharField(max_length=100)
    name = models.CharField(max_length=20)


class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='nurses')


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    school = models.OneToOneField(School, on_delete=models.CASCADE)


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    medical_history = models.CharField(max_length=200)
    age = models.IntegerField()
    ROLE_CHOICES = (
        ('female', 'Female'),
        ('male', 'Male'),

    )
    sex = models.CharField(max_length=10, choices=ROLE_CHOICES)
    state = models.CharField(max_length=20)
    class_CHOICES = (
        ('SSS1', 'SSS1'),
        ('SSS2', 'SSS2'),
        ('SSS3', 'SSS3'))
    level = models.CharField(max_length=10, choices=class_CHOICES)


class Drug(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)


class Case(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)


class MedicationRecord(models.Model):
    case = models.ForeignKey(
        'case', on_delete=models.CASCADE, related_name='medication_records')
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    night = models.BooleanField(default=False)
    days = models.PositiveIntegerField()
