from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from profiles.models import UserProfile, Education, Skill, Project, Experience
from profiles.resume_parser import parse_resume_content

class ProfileManagementTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='Password123!', email='u1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='Password123!', email='u2@example.com')
        self.profile1, _ = UserProfile.objects.get_or_create(user=self.user1, full_name='User One')
        self.profile2, _ = UserProfile.objects.get_or_create(user=self.user2, full_name='User Two')

        self.client1 = Client()
        self.client1.login(username='user1', password='Password123!')

    def test_add_and_delete_skill(self):
        # Add Skill
        response = self.client1.post(reverse('skill_add'), {
            'name': 'Python',
            'category': 'programming',
            'proficiency': 'Advanced'
        })
        self.assertEqual(response.status_code, 302)
        skill = Skill.objects.get(profile=self.profile1, name='Python')
        self.assertEqual(skill.proficiency, 'Advanced')

        # Delete Skill
        del_resp = self.client1.post(reverse('skill_delete', args=[skill.pk]))
        self.assertEqual(del_resp.status_code, 302)
        self.assertFalse(Skill.objects.filter(pk=skill.pk).exists())

    def test_data_ownership_isolation(self):
        # Create project belonging to user2
        proj2 = Project.objects.create(
            profile=self.profile2,
            title='User 2 Secret Project',
            description='Proprietary code'
        )

        # User1 attempts to delete User2's project
        response = self.client1.post(reverse('project_delete', args=[proj2.pk]))
        # Must return 404 Not Found due to get_object_or_404(Project, pk=pk, profile__user=request.user)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Project.objects.filter(pk=proj2.pk).exists())

    def test_resume_parser_contact_and_skills_extraction(self):
        sample_resume_text = """
        Jane SoftwareEngineer
        jane.engineer@example.com | (555) 234-5678 | San Francisco, CA
        https://linkedin.com/in/jane-engineer | https://github.com/jane-engineer

        Summary
        Experienced software engineer specialized in building scalable microservices and APIs.

        Skills: Python, Django, PostgreSQL, Docker, Redis, Kubernetes, React
        """
        extracted = parse_resume_content(sample_resume_text)
        self.assertEqual(extracted['email'], 'jane.engineer@example.com')
        self.assertIn('555', extracted['phone'])
        self.assertIn('Python', extracted['extracted_skills'])
        self.assertIn('Django', extracted['extracted_skills'])
        self.assertIn('PostgreSQL', extracted['extracted_skills'])
