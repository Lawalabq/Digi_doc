
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, School, Staff, Student, Nurse


admin.site.register(Staff)
admin.site.register(Nurse)
admin.site.register(School)
admin.site.register(User, UserAdmin)

# Register your models here.
