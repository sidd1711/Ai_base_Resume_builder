from django import forms
from .models import (
    UserProfile, Education, Skill, Project, Experience,
    Certification, Achievement
)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'email', 'phone', 'city', 'country',
            'linkedin_url', 'github_url', 'portfolio_url',
            'professional_status', 'professional_summary',
            'years_of_experience', 'target_job_roles'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Alex Johnson'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'alex@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 019-2834'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'San Francisco'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'USA'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/alexjohnson'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/alexjohnson'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://alexjohnson.dev'}),
            'professional_status': forms.Select(attrs={'class': 'form-select'}),
            'professional_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Dedicated software engineer with 3+ years building scalable Python web applications...'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'target_job_roles': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Full-Stack Developer, Python Engineer'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'is_current', 'grade_or_gpa', 'description']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'University of California, Berkeley'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'B.S. in Computer Science'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Computer Science'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Aug 2020'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'May 2024'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'grade_or_gpa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '3.8 / 4.0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Dean’s Honor List, Relevant Coursework: Algorithms, OS, Distributed Systems'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'proficiency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Python, PostgreSQL, Docker'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'proficiency': forms.Select(attrs={'class': 'form-select'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'technologies', 'description', 'responsibilities', 'measurable_results', 'project_url', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-Commerce Microservices Engine'}),
            'technologies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, PostgreSQL, Redis, Docker'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Engineered a scalable multi-vendor checkout and inventory management backend.'}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Implemented asynchronous Celery task queues and Stripe webhooks.'}),
            'measurable_results': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Processed 15,000 daily orders with 99.98% uptime. (Only include verified facts)'}),
            'project_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/user/project'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jan 2023'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apr 2023'}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['organization', 'job_title', 'employment_type', 'location', 'start_date', 'end_date', 'is_current', 'responsibilities', 'achievements', 'technologies_used']
        widgets = {
            'organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Stripe / Tech Innovations Inc.'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Software Development Engineer'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'San Francisco, CA (Remote)'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jul 2022'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Present'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Spearheaded payment processing pipeline migration and API security improvements.'}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Accelerated database query speeds by 35% across core transaction endpoints.'}),
            'technologies_used': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django REST, AWS S3, PostgreSQL'}),
        }


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuing_organization', 'issue_date', 'expiration_date', 'credential_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AWS Certified Solutions Architect'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amazon Web Services'}),
            'issue_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sep 2023'}),
            'expiration_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sep 2026'}),
            'credential_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.credly.com/...'}),
        }


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'category', 'description', 'date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1st Place Winner - Hackathon 2023'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Built an AI-driven accessibility tool in 36 hours among 120 competing teams.'}),
            'date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nov 2023'}),
        }


class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(
        label="Select PDF or DOCX Resume",
        help_text="Supported formats: .pdf, .docx (Max 5MB). We extract your facts into an editable review form without overwriting your profile automatically.",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.docx'})
    )

    def clean_resume_file(self):
        f = self.cleaned_data.get('resume_file')
        if f:
            ext = f.name.split('.')[-1].lower()
            if ext not in ['pdf', 'docx']:
                raise forms.ValidationError("Unsupported file extension. Please upload a PDF or DOCX file.")
            if f.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size exceeds 5MB limit.")
        return f
