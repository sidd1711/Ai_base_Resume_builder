from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    STATUS_CHOICES = [
        ('student', 'Student'),
        ('fresh_graduate', 'Fresh Graduate'),
        ('job_seeker', 'Active Job Seeker'),
        ('experienced', 'Experienced Professional'),
        ('career_changer', 'Career Changer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True, max_length=255)
    github_url = models.URLField(blank=True, max_length=255)
    portfolio_url = models.URLField(blank=True, max_length=255)

    professional_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='job_seeker')
    professional_summary = models.TextField(blank=True, help_text="Concise career objective or executive summary.")
    years_of_experience = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    target_job_roles = models.CharField(max_length=255, blank=True, help_text="Comma-separated target roles (e.g., Python Developer, Data Analyst)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name or self.user.username

    @property
    def location(self):
        parts = [p for p in (self.city, self.country) if p]
        return ", ".join(parts)


class Education(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=150, help_text="e.g., Bachelor of Science, High School Diploma")
    field_of_study = models.CharField(max_length=150, blank=True, help_text="e.g., Computer Science")
    start_date = models.CharField(max_length=50, blank=True, help_text="e.g., Aug 2020 or 2020")
    end_date = models.CharField(max_length=50, blank=True, help_text="e.g., May 2024 or Present")
    is_current = models.BooleanField(default=False)
    grade_or_gpa = models.CharField(max_length=50, blank=True, help_text="e.g., 3.8 / 4.0 or 85%")
    description = models.TextField(blank=True, help_text="Relevant coursework, honors, or activities")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.degree} at {self.institution}"


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming Languages'),
        ('framework', 'Frameworks & Libraries'),
        ('database', 'Databases'),
        ('tool', 'Tools & Platforms'),
        ('domain', 'Domain Knowledge'),
        ('soft_skill', 'Soft Skills'),
    ]

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='programming')
    proficiency = models.CharField(max_length=50, blank=True, default='Intermediate',
                                  choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Expert', 'Expert')])

    class Meta:
        ordering = ['category', 'name']
        unique_together = ('profile', 'name')

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Project(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Overview of the project and its goals.")
    technologies = models.CharField(max_length=300, blank=True, help_text="e.g., Python, Django, PostgreSQL, Docker")
    responsibilities = models.TextField(blank=True, help_text="Specific features you personally built.")
    measurable_results = models.TextField(blank=True, help_text="Verified metrics (e.g., reduced response time by 30%). Never invent numbers.")
    project_url = models.URLField(blank=True, max_length=255)
    start_date = models.CharField(max_length=50, blank=True)
    end_date = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title


class Experience(models.Model):
    TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
    ]

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='experiences')
    organization = models.CharField(max_length=200)
    job_title = models.CharField(max_length=150)
    employment_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='full_time')
    location = models.CharField(max_length=100, blank=True)
    start_date = models.CharField(max_length=50, blank=True, help_text="e.g., Jun 2022")
    end_date = models.CharField(max_length=50, blank=True, help_text="e.g., Present or Dec 2023")
    is_current = models.BooleanField(default=False)
    responsibilities = models.TextField(help_text="Key duties and day-to-day operations.")
    achievements = models.TextField(blank=True, help_text="Verified contributions and outcomes.")
    technologies_used = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.job_title} at {self.organization}"


class Certification(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.CharField(max_length=50, blank=True)
    expiration_date = models.CharField(max_length=50, blank=True)
    credential_url = models.URLField(blank=True, max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"


class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('award', 'Award / Honor'),
        ('publication', 'Publication'),
        ('volunteer', 'Volunteer Experience'),
        ('language', 'Language Proficiency'),
        ('extracurricular', 'Extracurricular Activity'),
    ]

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='award')
    description = models.TextField(blank=True)
    date = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.get_category_display()}: {self.title}"
