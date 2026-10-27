from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from profiles.models import UserProfile, Skill, Project, Experience
from resume_builder.models import Resume, ResumeVersion
from resume_builder.services import build_resume_from_profile
from resume_builder.rule_based_generator import enhance_bullet_point

class ResumeBuilderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='resumetestuser', password='Password123!', email='rt@example.com')
        self.profile = UserProfile.objects.create(
            user=self.user,
            full_name='Test Developer',
            email='rt@example.com',
            phone='+1 555-0199',
            city='Austin',
            country='USA',
            professional_summary='Passionate backend engineer with 3 years building web APIs.',
            years_of_experience=3.0,
            target_job_roles='Backend Engineer'
        )
        Skill.objects.create(profile=self.profile, name='Python', category='programming')
        Skill.objects.create(profile=self.profile, name='Django', category='framework')
        Project.objects.create(
            profile=self.profile,
            title='Inventory API',
            description='Made a REST API using Django and PostgreSQL.',
            responsibilities='Handled authentication with JWT tokens.',
            technologies='Python, Django, PostgreSQL'
        )

        self.client = Client()
        self.client.login(username='resumetestuser', password='Password123!')

    def test_build_resume_from_profile_service(self):
        resume = build_resume_from_profile(
            user=self.user,
            target_role='Backend Engineer',
            template_name='technical_resume'
        )
        self.assertEqual(resume.full_name, 'Test Developer')
        self.assertIn('Python', resume.selected_skills)
        self.assertIn('Django', resume.selected_skills)
        self.assertEqual(len(resume.selected_projects), 1)

        # Ensure initial snapshot version was created
        self.assertEqual(resume.versions.count(), 1)

    def test_rule_based_enhancer_fact_preservation(self):
        # Raw passive bullet
        raw = "made a website using Python and fixed bugs in payment flow"
        enhanced = enhance_bullet_point(raw)

        # Verifies action verb replacement
        self.assertIn("Architected and built", enhanced)
        self.assertIn("resolved critical defects", enhanced)
        # Preserves factual words
        self.assertIn("Python", enhanced)
        self.assertIn("payment flow", enhanced)

    def test_resume_duplication_and_versioning(self):
        resume = build_resume_from_profile(self.user, 'Backend Engineer')
        # Duplicate
        dup_resp = self.client.post(reverse('resume_duplicate', args=[resume.pk]))
        self.assertEqual(dup_resp.status_code, 302)
        self.assertTrue(Resume.objects.filter(title__contains='(Copy)').exists())

        # Save new version snapshot
        resume.title = "Updated Title v2"
        resume.save()
        resume.save_version(change_summary="Changed title")
        self.assertEqual(resume.versions.count(), 2)
