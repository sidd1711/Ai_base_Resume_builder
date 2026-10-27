from django.db import models
from django.contrib.auth.models import User
from job_analyzer.models import JobAnalysis

TEMPLATE_CHOICES = [
    ('classic_professional', 'Classic Professional (Universal ATS Standard)'),
    ('modern_minimal', 'Modern Minimal (Clean & Elegant Whitespace)'),
    ('technical_resume', 'Technical Resume (Optimized for Software & Engineering)'),
    ('graduate_fresher', 'Graduate & Fresher (Education & Projects Focus)'),
    ('experienced_professional', 'Experienced Professional (Chronology & Achievements)'),
]

def default_section_order():
    return [
        'summary',
        'skills',
        'experience',
        'projects',
        'education',
        'certifications',
        'achievements'
    ]

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200, help_text="e.g. Senior Python Developer - Stripe")
    target_role = models.CharField(max_length=200)
    job_analysis = models.ForeignKey(JobAnalysis, on_delete=models.SET_NULL, null=True, blank=True, related_name='resumes')
    template_name = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, default='classic_professional')

    # Contact & Header Details
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=150, blank=True)
    linkedin_url = models.URLField(blank=True, max_length=255)
    github_url = models.URLField(blank=True, max_length=255)
    portfolio_url = models.URLField(blank=True, max_length=255)

    # Core Content
    professional_summary = models.TextField(blank=True)
    selected_skills = models.JSONField(default=list, help_text="List of skills selected for this specific resume.")
    selected_educations = models.JSONField(default=list, help_text="List of education records included.")
    selected_projects = models.JSONField(default=list, help_text="List of project objects with tailored bullets.")
    selected_experiences = models.JSONField(default=list, help_text="List of experience objects with tailored bullets.")
    selected_certifications = models.JSONField(default=list, help_text="List of certifications included.")
    selected_achievements = models.JSONField(default=list, help_text="List of achievements included.")

    # Section ordering and typography
    section_order = models.JSONField(default=default_section_order)
    font_family = models.CharField(max_length=50, default='Helvetica, Arial, sans-serif')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.get_template_name_display()})"

    def save_version(self, change_summary="Saved checkpoint"):
        """Creates a snapshot version of the current resume state."""
        version_num = self.versions.count() + 1
        snapshot = {
            'title': self.title,
            'target_role': self.target_role,
            'template_name': self.template_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'linkedin_url': self.linkedin_url,
            'github_url': self.github_url,
            'portfolio_url': self.portfolio_url,
            'professional_summary': self.professional_summary,
            'selected_skills': self.selected_skills,
            'selected_educations': self.selected_educations,
            'selected_projects': self.selected_projects,
            'selected_experiences': self.selected_experiences,
            'selected_certifications': self.selected_certifications,
            'selected_achievements': self.selected_achievements,
            'section_order': self.section_order,
        }
        return ResumeVersion.objects.create(
            resume=self,
            version_number=version_num,
            content_snapshot=snapshot,
            change_summary=change_summary
        )


class ResumeVersion(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    content_snapshot = models.JSONField()
    change_summary = models.CharField(max_length=255, default='Manual Save')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-version_number']

    def __str__(self):
        return f"{self.resume.title} - v{self.version_number} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
