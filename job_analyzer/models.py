from django.db import models
from django.contrib.auth.models import User

class JobAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_analyses')
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=150, blank=True)
    raw_description = models.TextField(help_text="Original job description pasted by the user.")
    required_skills = models.JSONField(default=list, help_text="List of mandatory technical and domain skills extracted.")
    preferred_skills = models.JSONField(default=list, help_text="List of bonus / preferred skills extracted.")
    experience_required = models.CharField(max_length=150, blank=True)
    education_required = models.CharField(max_length=200, blank=True)
    is_role_preset = models.BooleanField(default=False, help_text="True if generated from preset template instead of raw JD text.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.job_title} ({self.created_at.strftime('%Y-%m-%d')})"

    @property
    def total_skills_count(self):
        return len(self.required_skills) + len(self.preferred_skills)
