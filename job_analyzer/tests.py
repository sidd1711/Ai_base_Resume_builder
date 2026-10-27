from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from job_analyzer.models import JobAnalysis
from job_analyzer.skill_extractor import extract_job_requirements

class JobAnalyzerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testjobuser', password='Password123!')
        self.client = Client()
        self.client.login(username='testjobuser', password='Password123!')

    def test_extract_job_requirements_and_aliases(self):
        jd_text = """
        Job Title: Senior Backend Developer
        Requirements:
        - Must have 4+ years of work experience with Python and Django.
        - Required proficiency with Postgres, Redis, and REST APIs.
        - Strong foundation in Git, Linux, and SQL.
        - Bachelor's degree in Computer Science or equivalent.

        Preferred Qualifications:
        - Experience with K8s, Docker, and AWS is a plus.
        - Nice to have experience with GraphQL and Celery.
        """
        extracted = extract_job_requirements(jd_text)

        # Alias Normalization check: "Postgres" -> "PostgreSQL", "K8s" -> "Kubernetes"
        self.assertIn('PostgreSQL', extracted['required_skills'])
        self.assertIn('Python', extracted['required_skills'])
        self.assertIn('Django', extracted['required_skills'])

        # Distinguish Required vs Preferred
        self.assertIn('Kubernetes', extracted['preferred_skills'])
        self.assertIn('Docker', extracted['preferred_skills'])
        self.assertIn('AWS', extracted['preferred_skills'])

        # Experience & Education extraction
        self.assertIn('4+ years', extracted['experience_required'].lower())
        self.assertIn('bachelor', extracted['education_required'].lower())

    def test_job_analysis_view_creation(self):
        response = self.client.post(reverse('job_analyze'), {
            'job_title': 'Python Developer',
            'company_name': 'Acme Corp',
            'raw_description': 'Required: Python, Django, PostgreSQL. Nice to have: Docker.'
        })
        self.assertEqual(response.status_code, 302)
        analysis = JobAnalysis.objects.get(job_title='Python Developer')
        self.assertEqual(analysis.company_name, 'Acme Corp')
        self.assertIn('Python', analysis.required_skills)
        self.assertIn('Django', analysis.required_skills)
