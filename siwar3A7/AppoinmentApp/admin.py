from django.contrib import admin
from .models import Appointement


@admin.register(Appointement)
class AppointementAdmin(admin.ModelAdmin):
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
            'fields': ('doctor', 'patient')
        }),
        ('Planification', {
            'fields': ('created_at', 'update_at')
        }),
    )
    readonly_fields = ('created_at', 'update_at')