from django.contrib import admin
from .models import ResumeAnalysis

@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ('resume', 'job_analysis', 'overall_score', 'keyword_score', 'section_score', 'created_at')
    list_filter = ('created_at',)
