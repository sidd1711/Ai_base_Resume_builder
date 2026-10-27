from django.db import models
from resume_builder.models import Resume
from job_analyzer.models import JobAnalysis

class ResumeAnalysis(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='ats_analyses')
    job_analysis = models.ForeignKey(JobAnalysis, on_delete=models.SET_NULL, null=True, blank=True)

    # Transparent Scoring Metrics (0 to 100)
    keyword_score = models.FloatField(default=0.0)
    section_score = models.FloatField(default=0.0)
    formatting_score = models.FloatField(default=0.0)
    overall_score = models.FloatField(default=0.0)

    # Keyword Coverage Details
    matched_required = models.JSONField(default=list)
    missing_required = models.JSONField(default=list)
    matched_preferred = models.JSONField(default=list)
    missing_preferred = models.JSONField(default=list)
    available_profile_skills = models.JSONField(default=list, help_text="Verified skills in user profile not yet placed on this resume.")

    # Structural & Formatting Audit
    section_audit = models.JSONField(default=dict)
    formatting_issues = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"ATS Report for {self.resume.title} ({self.overall_score:.0f}%)"
