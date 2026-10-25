from django.contrib import admin
from .models import Job
# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "job_type", "salary", "employer", "created_at", "is_active")
    list_filter = ("job_type", "is_active")
    search_fields = ("title", "company", "location", "description")
    ordering = ("-created_at",)