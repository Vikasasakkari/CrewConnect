from django.contrib import admin
from hr.models import Department, Designation, Employee
from .models import CalendarEvent

# Register your models here.
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Employee)

@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'category',
        'start_date',
        'end_date',
        'created_by',
    )

    list_filter = (
        'category',
        'start_date',
    )

    search_fields = (
        'title',
        'description',
    )

    ordering = (
        '-start_date',
    )