from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import UserProfile, Skill
from resume_builder.models import Resume
from job_analyzer.models import JobAnalysis
from ats_checker.analyzer import run_full_ats_analysis

class AtsCheckerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='atsuser', password='Password123!')
        self.profile = UserProfile.objects.create(
            user=self.user,
            full_name='ATS Candidate',
            email='candidate@example.com',
            phone='+1 555-4321'
        )
        Skill.objects.create(profile=self.profile, name='Docker') # in profile but maybe not in resume

        self.resume = Resume.objects.create(
            user=self.user,
            title='Python Resume',
            target_role='Python Developer',
            full_name='ATS Candidate',
            email='candidate@example.com',
            phone='+1 555-4321',
            professional_summary='Experienced Python and Django developer building high performance web servers.',
            selected_skills=['Python', 'Django', 'PostgreSQL'],
            selected_educations=[{'degree': 'B.S. CS', 'institution': 'State Univ', 'start_date': '2019', 'end_date': '2023'}],
            selected_projects=[{'title': 'Web App', 'bullets': ['Architected API endpoints with Django.']}],
            selected_experiences=[{'job_title': 'Developer', 'organization': 'Tech Inc', 'bullets': ['Engineered backend services.']}]
        )

        self.job = JobAnalysis.objects.create(
            user=self.user,
            job_title='Python Developer',
            raw_description='Looking for Python, Django, Docker, and Redis developer.',
            required_skills=['Python', 'Django', 'Docker'],
            preferred_skills=['Redis']
        )

    def test_ats_keyword_coverage_and_profile_gap_detection(self):
        analysis = run_full_ats_analysis(self.resume, self.job)

        # Python and Django are matched (2 out of 3 required)
        self.assertIn('Python', analysis['matched_required'])
        self.assertIn('Django', analysis['matched_required'])
        # Docker is missing from resume
        self.assertIn('Docker', analysis['missing_required'])

        # Expected keyword coverage: 2 / 3 * 100 = 66.7%
        self.assertAlmostEqual(analysis['keyword_score'], 66.7, delta=0.5)

        # Profile Gaps: Docker is in user's verified profile and should be recommended!
        self.assertIn('Docker', analysis['available_profile_skills'])

    def test_transparent_score_composition(self):
        analysis = run_full_ats_analysis(self.resume, self.job)
        # All sections (contact, summary, skills, exp, proj, edu) are complete -> 100%
        self.assertEqual(analysis['section_score'], 100.0)
        self.assertEqual(analysis['formatting_score'], 100.0)

        # Expected overall score: 0.50 * 66.7 + 0.30 * 100 + 0.20 * 100 = 33.35 + 30 + 20 = 83.35
        expected_overall = (0.50 * analysis['keyword_score']) + (0.30 * 100.0) + (0.20 * 100.0)
        self.assertAlmostEqual(analysis['overall_score'], expected_overall, delta=0.5)
