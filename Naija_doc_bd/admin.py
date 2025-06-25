
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, School, Staff, Student, Nurse, Drug, Case, MedicationRecord


admin.site.register(Staff)
admin.site.register(Case)
admin.site.register(Drug)
admin.site.register(Student)
admin.site.register(Nurse)
admin.site.register(School)
admin.site.register(MedicationRecord)
admin.site.register(User, UserAdmin)

# Register your models here.
