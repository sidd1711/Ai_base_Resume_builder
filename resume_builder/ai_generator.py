"""
AI Resume Content Generator with Gemini API integration.
Features strict prompt guardrails and automatic offline fallback to rule_based_generator.
"""

from django.conf import settings
from .rule_based_generator import (
    enhance_bullet_point as fallback_bullet,
    generate_professional_summary as fallback_summary,
    tailor_project_bullets as fallback_proj_bullets,
    tailor_experience_bullets as fallback_exp_bullets
)

def get_gemini_client():
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except Exception:
        return None


def generate_tailored_summary_ai(user_profile, target_role="", target_skills=None):
    """Generates an executive summary using LLM if available, otherwise rule-based fallback."""
    client = get_gemini_client()
    if not client:
        return fallback_summary(user_profile, target_role, target_skills)

    skills_list = [s.name for s in user_profile.skills.all()]
    prompt = f"""
Act as a factual ATS resume editor.
Candidate Profile:
- Name: {user_profile.full_name}
- Years of Experience: {user_profile.years_of_experience}
- Target Role: {target_role or user_profile.target_job_roles}
- Verified Skills: {', '.join(skills_list)}
- Raw Summary/Objective: {user_profile.professional_summary}

STRICT INTEGRITY RULES:
1. Never invent credentials, certifications, degrees, or companies.
2. Only mention skills listed in Verified Skills.
3. Keep the summary between 2 and 4 sentences.
4. Return ONLY the final summary text without introductory remarks.
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        if response and response.text:
            return response.text.strip()
    except Exception:
        pass

    return fallback_summary(user_profile, target_role, target_skills)


def enhance_bullet_point_ai(raw_bullet, target_role=""):
    """Improves a single bullet point using LLM if available, otherwise rule-based fallback."""
    client = get_gemini_client()
    if not client:
        return fallback_bullet(raw_bullet, target_role)

    prompt = f"""
Rewrite the following resume bullet point to make it compelling, action-verb driven, and ATS-friendly for a {target_role} role.
Original Bullet: "{raw_bullet}"

STRICT INTEGRITY RULES:
- Never fabricate metrics, percentages, dollar amounts, or technologies not present in the original bullet.
- Begin with a strong action verb.
- Keep to 1 clear sentence.
- Output ONLY the rewritten bullet point text.
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        if response and response.text:
            cleaned = response.text.strip().strip('"').strip("'")
            return cleaned
    except Exception:
        pass

    return fallback_bullet(raw_bullet, target_role)
