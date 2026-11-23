from django.contrib import admin
from .models import Appointement


@admin.action(description="make them confirmed")
def confirmed_appointment(modeladmin, request, queryset):
    queryset.update(status=Appointement.Status.CONFIRMED)


@admin.register(Appointement)
class AppointmentAdminPers(admin.ModelAdmin):
    # inlines = ...
    actions = [confirmed_appointment]
    list_display = ('reason', 'status', 'duration_minutes', 'appointement_date')
    list_filter = ('status', 'appointement_date')
    list_editable = ('appointement_date', 'status')
    search_fields = ('status', 'reason')
    list_per_page = 2
    ordering = ('-appointement_date',)
    fieldsets = (
        ('Description', {
            'fields': ('reason', 'status', 'prescription')
        }),
        ('Date + duration', {
            'fields': ('appointement_date', 'duration_minutes')
        }),
        ('Patients/Doctors', {
            'fields': ('patient', 'doctor')
        }),
    )