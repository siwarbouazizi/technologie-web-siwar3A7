from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Speciality, Patient, Doctor
from AppoinmentApp.models import Appointement


class AppointementStacked(admin.StackedInline):
    model = Appointement
    extra = 0


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    inlines = [AppointementStacked]


@admin.register(Patient)
class PatientAdmin(UserAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Speciality)