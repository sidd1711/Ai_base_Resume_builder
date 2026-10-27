"""
NLP & Rule-Based Skill Extractor for Job Descriptions.
Extracts required/preferred skills, education requirements, and experience requirements.
"""

import re
from .skills_data import SKILL_ALIASES

REQUIRED_TRIGGERS = [
    'required', 'must have', 'must possess', 'minimum', 'essential',
    'qualifications', 'requirements', 'mandatory', 'needed', 'core requirements'
]

PREFERRED_TRIGGERS = [
    'preferred', 'nice to have', 'plus', 'bonus', 'desired',
    'good to have', 'advantage', 'beneficial', 'optional'
]

def extract_job_requirements(job_description):
    """
    Analyzes job description text and returns structured requirements.
    """
    if not job_description or not job_description.strip():
        return {
            'required_skills': [],
            'preferred_skills': [],
            'all_skills': [],
            'experience_required': '',
            'education_required': '',
            'responsibilities': [],
        }

    text = job_description
    lower_text = " " + text.lower() + " "

    # 1. Identify Sections or Sentences for Required vs Preferred
    sentences = re.split(r'[\n\.\;•\*\-]', text)

    found_required = set()
    found_preferred = set()
    found_general = set()

    for sentence in sentences:
        s_lower = sentence.lower().strip()
        if not s_lower:
            continue

        is_req = any(trig in s_lower for trig in REQUIRED_TRIGGERS)
        is_pref = any(trig in s_lower for trig in PREFERRED_TRIGGERS)

        # Check which skills appear in this sentence
        for alias, canonical in SKILL_ALIASES.items():
            pattern = r'(?<![a-z0-9])' + re.escape(alias) + r'(?![a-z0-9])'
            if re.search(pattern, s_lower):
                if is_pref:
                    found_preferred.add(canonical)
                elif is_req:
                    found_required.add(canonical)
                else:
                    found_general.add(canonical)

    # Resolve overlaps: if marked preferred, keep in preferred unless explicitly required elsewhere
    for skill in found_general:
        if skill not in found_preferred and skill not in found_required:
            # Default general mentions to required skills for ATS matching
            found_required.add(skill)

    # 2. Extract Experience Requirements (e.g. "3+ years", "5-7 years")
    exp_match = re.search(r'(\d{1,2}(?:\+|-|\s*to\s*\d{1,2})?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|work experience)?)', text, re.IGNORECASE)
    experience_req = exp_match.group(0).strip() if exp_match else "Not explicitly specified"

    # 3. Extract Education Requirements (e.g. "Bachelor's degree in Computer Science")
    edu_match = re.search(r'((?:bachelor|master|phd|b\.s\.|m\.s\.|associate)[\'s]*\s*(?:degree)?(?:\s+in\s+[\w\s,]+)?)', text, re.IGNORECASE)
    education_req = edu_match.group(0).strip() if edu_match else "Relevant degree or equivalent experience"

    all_skills = sorted(list(found_required.union(found_preferred)))

    return {
        'required_skills': sorted(list(found_required)),
        'preferred_skills': sorted(list(found_preferred - found_required)),
        'all_skills': all_skills,
        'experience_required': experience_req,
        'education_required': education_req,
    }
