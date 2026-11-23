from django.contrib import admin
from .models import Appointment
from AccountApp.models import Doctor


@admin.action(description="make them confirmed")
def confirmed_appointment(modeladmin, request, queryset):
    queryset.update(status="confirmed")


@admin.register(Appointment)
class AppointmentAdminPers(admin.ModelAdmin):
    # inlines = ...
    actions = [confirmed_appointment]
    list_display = ('reason', 'status', 'duration_minutes', 'appointment_date')
    list_filter = ('status', 'appointment_date')
    list_editable = ('appointment_date', 'status')
    search_fields = ('status', 'reason')
    list_per_page = 2
    ordering = ('-appointment_date',)
    fieldsets = (
        ('Description', {
            'fields': ('reason', 'status', 'prescription')
        }),
        ('Date + duration', {
            'fields': ('appointment_date', 'duration_minutes')
        }),
        ('Patients/Doctors', {
            'fields': ('patient', 'doctor')  # mets 'Doctor' si ton modèle l'écrit avec une majuscule
        }),
    )