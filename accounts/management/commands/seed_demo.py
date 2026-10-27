from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import (
    UserProfile, Education, Skill, Project, Experience, Certification, Achievement
)
from job_analyzer.models import JobAnalysis
from resume_builder.services import build_resume_from_profile
from ats_checker.analyzer import run_full_ats_analysis
from ats_checker.models import ResumeAnalysis

class Command(BaseCommand):
    help = 'Seeds sample demonstration data for ResumeForge AI'

    def handle(self, *args, **options):
        # 1. Create or get Demo User
        user, created = User.objects.get_or_create(
            username='alex_dev',
            defaults={
                'email': 'alex.johnson@example.com',
                'first_name': 'Alex',
                'last_name': 'Johnson'
            }
        )
        if created:
            user.set_password('Password123!')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created user: alex_dev (Password: Password123!)'))

        # 2. Master Profile
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'full_name': 'Alex Johnson',
                'email': 'alex.johnson@example.com',
                'phone': '+1 (555) 234-8901',
                'city': 'San Francisco',
                'country': 'USA',
                'linkedin_url': 'https://linkedin.com/in/alexjohnson-dev',
                'github_url': 'https://github.com/alexjohnson-dev',
                'portfolio_url': 'https://alexjohnson.dev',
                'professional_status': 'experienced',
                'years_of_experience': 3.5,
                'target_job_roles': 'Python Developer, Full-Stack Engineer',
                'professional_summary': (
                    'Results-driven Software Engineer with 3.5+ years of hands-on experience designing, '
                    'building, and maintaining scalable web applications and microservices. Proficient in Python, '
                    'Django, PostgreSQL, and cloud deployments with a focus on code reliability and database efficiency.'
                )
            }
        )

        # 3. Skills
        skills = [
            ('Python', 'programming', 'Advanced'),
            ('Django', 'framework', 'Advanced'),
            ('PostgreSQL', 'database', 'Advanced'),
            ('REST APIs', 'framework', 'Advanced'),
            ('Docker', 'tool', 'Intermediate'),
            ('Git', 'tool', 'Advanced'),
            ('Linux', 'tool', 'Intermediate'),
            ('JavaScript', 'programming', 'Intermediate'),
            ('Redis', 'database', 'Intermediate'),
            ('React', 'framework', 'Intermediate'),
        ]
        for name, cat, prof in skills:
            Skill.objects.get_or_create(profile=profile, name=name, defaults={'category': cat, 'proficiency': prof})

        # 4. Education
        Education.objects.get_or_create(
            profile=profile,
            institution='University of California, Berkeley',
            defaults={
                'degree': 'Bachelor of Science',
                'field_of_study': 'Computer Science',
                'start_date': 'Aug 2017',
                'end_date': 'May 2021',
                'grade_or_gpa': '3.8 / 4.0',
                'description': 'Coursework: Data Structures, Distributed Systems, Database Management, Operating Systems'
            }
        )

        # 5. Work Experience
        Experience.objects.get_or_create(
            profile=profile,
            organization='Apex Cloud Systems',
            job_title='Software Development Engineer',
            defaults={
                'employment_type': 'full_time',
                'location': 'San Francisco, CA',
                'start_date': 'Jul 2022',
                'end_date': 'Present',
                'responsibilities': (
                    'Spearheaded development of core payment and analytics APIs handling 2M monthly transactions.\n'
                    'Optimized PostgreSQL database schemas and indexing, reducing query latencies by 35%.\n'
                    'Collaborated with frontend teams to integrate responsive user dashboards.'
                ),
                'achievements': 'Automated deployment pipelines using Docker and GitHub Actions, cutting release cycles by 50%.',
                'technologies_used': 'Python, Django, PostgreSQL, Redis, Docker'
            }
        )

        # 6. Projects
        Project.objects.get_or_create(
            profile=profile,
            title='E-Commerce Inventory Engine',
            defaults={
                'technologies': 'Python, Django REST Framework, PostgreSQL, Docker',
                'description': 'High-performance inventory tracking system supporting real-time multi-warehouse stock sync.',
                'responsibilities': 'Implemented asynchronous Celery tasks and webhook consumers with idempotent processing.',
                'measurable_results': 'Successfully tested under simulated load of 5,000 concurrent requests with zero deadlock occurrences.',
                'project_url': 'https://github.com/alexjohnson-dev/inventory-engine',
                'start_date': 'Jan 2023',
                'end_date': 'May 2023'
            }
        )

        # 7. Job Analysis
        job, _ = JobAnalysis.objects.get_or_create(
            user=user,
            job_title='Senior Python Developer',
            defaults={
                'company_name': 'Stripe Partner Network',
                'raw_description': (
                    'Requirements:\n'
                    '- 3+ years experience with Python and Django.\n'
                    '- Deep knowledge of PostgreSQL, REST APIs, and Git.\n'
                    '- Experience with Docker, Redis, and Linux.\n\n'
                    'Preferred:\n'
                    '- Familiarity with Kubernetes, AWS, and Celery.'
                ),
                'required_skills': ['Python', 'Django', 'PostgreSQL', 'REST APIs', 'Git', 'Docker', 'Redis', 'Linux'],
                'preferred_skills': ['Kubernetes', 'AWS', 'Celery'],
                'experience_required': '3+ years experience',
                'education_required': "Bachelor's degree in CS or equivalent"
            }
        )

        # 8. Resume
        resume = build_resume_from_profile(
            user=user,
            target_role='Senior Python Developer',
            job_analysis=job,
            template_name='classic_professional'
        )

        # 9. Run ATS Analysis
        analysis_data = run_full_ats_analysis(resume, job)
        ResumeAnalysis.objects.create(
            resume=resume,
            job_analysis=job,
            keyword_score=analysis_data['keyword_score'],
            section_score=analysis_data['section_score'],
            formatting_score=analysis_data['formatting_score'],
            overall_score=analysis_data['overall_score'],
            matched_required=analysis_data['matched_required'],
            missing_required=analysis_data['missing_required'],
            matched_preferred=analysis_data['matched_preferred'],
            missing_preferred=analysis_data['missing_preferred'],
            available_profile_skills=analysis_data['available_profile_skills'],
            section_audit=analysis_data['section_audit'],
            formatting_issues=analysis_data['formatting_issues'],
            suggestions=analysis_data['suggestions']
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded complete demo dataset: profile, job analysis, tailored resume, and ATS report!'))
