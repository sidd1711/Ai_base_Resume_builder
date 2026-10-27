"""
Resume Construction & Assembly Service.
"""

from .models import Resume
from .ai_generator import (
    generate_tailored_summary_ai,
    enhance_bullet_point_ai
)
from .rule_based_generator import (
    tailor_project_bullets,
    tailor_experience_bullets
)

def build_resume_from_profile(user, target_role, job_analysis=None, template_name='classic_professional'):
    """
    Constructs an initial structured Resume from user's verified profile data.
    All content remains completely editable by the user.
    """
    profile = getattr(user, 'profile', None)
    if not profile:
        raise ValueError("User must have a profile created before building a resume.")

    # 1. Gather Personal Details
    full_name = profile.full_name or user.get_full_name() or user.username
    email = profile.email or user.email
    phone = profile.phone
    location = profile.location
    linkedin_url = profile.linkedin_url
    github_url = profile.github_url
    portfolio_url = profile.portfolio_url

    # 2. Extract target skills from JobAnalysis if present
    target_skills = []
    if job_analysis:
        target_skills = job_analysis.required_skills + job_analysis.preferred_skills

    # 3. Select and prioritize user's skills
    user_skills = list(profile.skills.all())
    selected_skills = []
    # Place skills that match target role at top
    target_skills_lower = [s.lower() for s in target_skills]
    matching_skills = [s.name for s in user_skills if s.name.lower() in target_skills_lower]
    other_skills = [s.name for s in user_skills if s.name.lower() not in target_skills_lower]
    selected_skills = matching_skills + other_skills

    # 4. Tailor Summary
    summary = generate_tailored_summary_ai(profile, target_role, target_skills)

    # 5. Format Education
    selected_educations = []
    for edu in profile.educations.all():
        selected_educations.append({
            'institution': edu.institution,
            'degree': edu.degree,
            'field_of_study': edu.field_of_study,
            'start_date': edu.start_date,
            'end_date': edu.end_date,
            'grade_or_gpa': edu.grade_or_gpa,
            'description': edu.description,
        })

    # 6. Format Projects with Tailored Bullets
    selected_projects = []
    for proj in profile.projects.all():
        bullets = tailor_project_bullets(proj, target_skills)
        selected_projects.append({
            'title': proj.title,
            'technologies': proj.technologies,
            'description': proj.description,
            'bullets': bullets,
            'project_url': proj.project_url,
            'start_date': proj.start_date,
            'end_date': proj.end_date,
        })

    # 7. Format Experience with Tailored Bullets
    selected_experiences = []
    for exp in profile.experiences.all():
        bullets = tailor_experience_bullets(exp, target_skills)
        selected_experiences.append({
            'organization': exp.organization,
            'job_title': exp.job_title,
            'employment_type': exp.get_employment_type_display(),
            'location': exp.location,
            'start_date': exp.start_date,
            'end_date': exp.end_date,
            'bullets': bullets,
            'technologies_used': exp.technologies_used,
        })

    # 8. Format Certifications & Achievements
    selected_certifications = []
    for cert in profile.certifications.all():
        selected_certifications.append({
            'name': cert.name,
            'issuing_organization': cert.issuing_organization,
            'issue_date': cert.issue_date,
            'credential_url': cert.credential_url,
        })

    selected_achievements = []
    for ach in profile.achievements.all():
        selected_achievements.append({
            'title': ach.title,
            'category': ach.get_category_display(),
            'description': ach.description,
            'date': ach.date,
        })

    title = f"{target_role} Resume"

    resume = Resume.objects.create(
        user=user,
        title=title,
        target_role=target_role,
        job_analysis=job_analysis,
        template_name=template_name,
        full_name=full_name,
        email=email,
        phone=phone,
        location=location,
        linkedin_url=linkedin_url,
        github_url=github_url,
        portfolio_url=portfolio_url,
        professional_summary=summary,
        selected_skills=selected_skills,
        selected_educations=selected_educations,
        selected_projects=selected_projects,
        selected_experiences=selected_experiences,
        selected_certifications=selected_certifications,
        selected_achievements=selected_achievements,
    )

    resume.save_version(change_summary="Initial generated draft")
    return resume
