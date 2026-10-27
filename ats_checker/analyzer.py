"""
ATS Compatibility & Scoring Engine.
Calculates section completeness, keyword coverage, formatting diagnostics, and transparent metrics.
"""

import re
from .suggestions import generate_actionable_suggestions

def audit_resume_sections(resume):
    """
    Evaluates presence and health of standard resume sections.
    """
    audit = {}

    # Contact Details
    contact_ok = bool(resume.full_name and resume.email and resume.phone)
    audit['Contact Information'] = {
        'present': contact_ok,
        'status': 'Complete' if contact_ok else 'Missing Phone or Email',
        'is_critical': True
    }

    # Summary
    summary_ok = bool(resume.professional_summary and len(resume.professional_summary.strip()) > 30)
    audit['Professional Summary'] = {
        'present': summary_ok,
        'status': 'Complete' if summary_ok else 'Empty or too brief',
        'is_critical': True
    }

    # Skills
    skills_count = len(resume.selected_skills) if isinstance(resume.selected_skills, list) else 0
    audit['Core Skills'] = {
        'present': skills_count >= 3,
        'status': f'{skills_count} skills listed' if skills_count >= 3 else 'Needs at least 3 relevant skills',
        'is_critical': True
    }

    # Experience / Internships
    exp_count = len(resume.selected_experiences) if isinstance(resume.selected_experiences, list) else 0
    audit['Work Experience'] = {
        'present': exp_count > 0,
        'status': f'{exp_count} entries' if exp_count > 0 else 'No experience entries added',
        'is_critical': False
    }

    # Projects
    proj_count = len(resume.selected_projects) if isinstance(resume.selected_projects, list) else 0
    audit['Technical Projects'] = {
        'present': proj_count > 0,
        'status': f'{proj_count} projects' if proj_count > 0 else 'No projects listed',
        'is_critical': False
    }

    # Education
    edu_count = len(resume.selected_educations) if isinstance(resume.selected_educations, list) else 0
    audit['Education'] = {
        'present': edu_count > 0,
        'status': f'{edu_count} qualifications' if edu_count > 0 else 'Missing education details',
        'is_critical': True
    }

    # Scoring: count present sections vs total applicable
    present_count = sum(1 for sec in audit.values() if sec['present'])
    section_score = (present_count / len(audit)) * 100.0

    return audit, round(section_score, 1)


def audit_formatting(resume):
    """
    Identifies common ATS parsing blockers (e.g. malformed contact info, excessively long bullets).
    """
    issues = []
    penalties = 0

    # Contact check
    if not re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume.email or ''):
        issues.append("Email address appears invalid or empty.")
        penalties += 15

    if not resume.phone or len(resume.phone.strip()) < 7:
        issues.append("Phone number is missing or incomplete.")
        penalties += 10

    # Long bullet points check (> 250 characters can diminish readability)
    long_bullets = 0
    if isinstance(resume.selected_projects, list):
        for proj in resume.selected_projects:
            for b in proj.get('bullets', []):
                if len(b) > 280:
                    long_bullets += 1

    if isinstance(resume.selected_experiences, list):
        for exp in resume.selected_experiences:
            for b in exp.get('bullets', []):
                if len(b) > 280:
                    long_bullets += 1

    if long_bullets > 0:
        issues.append(f"{long_bullets} bullet point(s) exceed 280 characters. Shorten them into concise, high-impact statements.")
        penalties += min(20, long_bullets * 5)

    # Empty summary
    if not resume.professional_summary:
        issues.append("Professional summary is empty.")
        penalties += 15

    formatting_score = max(0.0, 100.0 - penalties)
    return issues, round(formatting_score, 1)


def audit_keyword_coverage(resume, job_analysis):
    """
    Computes exact keyword alignment against required and preferred skills.
    """
    if not job_analysis:
        return 100.0, [], [], [], [], []

    resume_text = " ".join([
        resume.title,
        resume.target_role,
        resume.professional_summary,
        " ".join(resume.selected_skills if isinstance(resume.selected_skills, list) else []),
    ]).lower()

    if isinstance(resume.selected_projects, list):
        for p in resume.selected_projects:
            resume_text += " " + p.get('title', '').lower() + " " + p.get('technologies', '').lower()
            resume_text += " " + " ".join(p.get('bullets', [])).lower()

    if isinstance(resume.selected_experiences, list):
        for e in resume.selected_experiences:
            resume_text += " " + e.get('job_title', '').lower() + " " + e.get('organization', '').lower()
            resume_text += " " + " ".join(e.get('bullets', [])).lower()

    matched_req = []
    missing_req = []
    for skill in job_analysis.required_skills:
        pattern = r'(?<![a-z0-9])' + re.escape(skill.lower()) + r'(?![a-z0-9])'
        if re.search(pattern, resume_text):
            matched_req.append(skill)
        else:
            missing_req.append(skill)

    matched_pref = []
    missing_pref = []
    for skill in job_analysis.preferred_skills:
        pattern = r'(?<![a-z0-9])' + re.escape(skill.lower()) + r'(?![a-z0-9])'
        if re.search(pattern, resume_text):
            matched_pref.append(skill)
        else:
            missing_pref.append(skill)

    total_req = len(job_analysis.required_skills)
    if total_req > 0:
        keyword_score = (len(matched_req) / total_req) * 100.0
    else:
        keyword_score = 100.0

    # Check for skills in user profile that could be included
    user_profile = getattr(resume.user, 'profile', None)
    available_profile_skills = []
    if user_profile:
        resume_skills_lower = [s.lower() for s in resume.selected_skills]
        for skill in user_profile.skills.all():
            if skill.name.lower() in [s.lower() for s in missing_req] and skill.name.lower() not in resume_skills_lower:
                available_profile_skills.append(skill.name)

    return round(keyword_score, 1), matched_req, missing_req, matched_pref, missing_pref, available_profile_skills


def run_full_ats_analysis(resume, job_analysis=None):
    """
    Executes the entire ATS diagnostic pipeline.
    """
    section_audit, section_score = audit_resume_sections(resume)
    formatting_issues, formatting_score = audit_formatting(resume)
    keyword_score, matched_req, missing_req, matched_pref, missing_pref, available_profile = audit_keyword_coverage(resume, job_analysis)

    # Weighted composite score
    if job_analysis:
        overall_score = (0.50 * keyword_score) + (0.30 * section_score) + (0.20 * formatting_score)
    else:
        overall_score = (0.60 * section_score) + (0.40 * formatting_score)

    suggestions = generate_actionable_suggestions(
        missing_req=missing_req,
        missing_pref=missing_pref,
        available_profile_skills=available_profile,
        section_audit=section_audit,
        formatting_issues=formatting_issues
    )

    return {
        'keyword_score': keyword_score,
        'section_score': section_score,
        'formatting_score': formatting_score,
        'overall_score': round(overall_score, 1),
        'matched_required': matched_req,
        'missing_required': missing_req,
        'matched_preferred': matched_pref,
        'missing_preferred': missing_pref,
        'available_profile_skills': available_profile,
        'section_audit': section_audit,
        'formatting_issues': formatting_issues,
        'suggestions': suggestions,
    }
