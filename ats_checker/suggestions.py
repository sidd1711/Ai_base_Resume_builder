"""
Generates category-specific, actionable recommendations for resume improvement.
"""

def generate_actionable_suggestions(missing_req, missing_pref, available_profile_skills, section_audit, formatting_issues):
    suggestions = []

    # 1. High Priority: Skills present in profile but missing from this resume
    if available_profile_skills:
        suggestions.append({
            'category': 'Skills Alignment',
            'severity': 'high',
            'title': 'Add Verified Profile Skills',
            'message': f"You already have verified experience in {', '.join(available_profile_skills[:4])} in your profile! Add these to this resume to immediately boost keyword alignment without exaggerating."
        })

    # 2. Required Keywords Gap
    if missing_req:
        suggestions.append({
            'category': 'Job Requirements',
            'severity': 'medium',
            'title': 'Address Required Skill Gaps',
            'message': f"The job description specifically mentions {', '.join(missing_req[:5])}. If you have practical project or coursework experience with these, add them to your skills or project descriptions."
        })

    # 3. Section Completeness
    for sec_name, data in section_audit.items():
        if not data['present'] and data['is_critical']:
            suggestions.append({
                'category': 'Structure',
                'severity': 'high',
                'title': f'Complete {sec_name}',
                'message': f"{sec_name} is essential for standard ATS parsing. {data['status']}."
            })

    # 4. Formatting issues
    for issue in formatting_issues:
        suggestions.append({
            'category': 'Formatting & Readability',
            'severity': 'medium',
            'title': 'Readability Optimization',
            'message': issue
        })

    # 5. Preferred Skills
    if missing_pref:
        suggestions.append({
            'category': 'Competitive Edge',
            'severity': 'low',
            'title': 'Consider Bonus / Preferred Skills',
            'message': f"The role lists {', '.join(missing_pref[:3])} as preferred bonus qualifications. Highlighting relevant familiarity can help you stand out."
        })

    return suggestions
