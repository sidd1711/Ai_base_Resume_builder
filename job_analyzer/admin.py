from django.contrib import admin
from .models import JobAnalysis

@admin.register(JobAnalysis)
class JobAnalysisAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'user', 'company_name', 'is_role_preset', 'created_at')
    search_fields = ('job_title', 'company_name', 'user__username')
