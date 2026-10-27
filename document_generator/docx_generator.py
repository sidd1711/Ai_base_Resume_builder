"""
ATS-Friendly Microsoft Word (.docx) Generator using python-docx.
Employs standard Word headings, paragraphs, and list styles without tables or textboxes.
"""

import io
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate_resume_docx(resume):
    """
    Builds a clean, standard DOCX document suitable for ATS parsing.
    Returns bytes in a BytesIO buffer.
    """
    doc = Document()

    # Set 0.5 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    # 1. Header (Name)
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title_p.add_run(resume.full_name or "Resume")
    run.bold = True
    run.font.size = Pt(20)
    run.font.color.rgb = RGBColor(26, 32, 44)

    # Contact line
    contact_parts = []
    if resume.email:
        contact_parts.append(resume.email)
    if resume.phone:
        contact_parts.append(resume.phone)
    if resume.location:
        contact_parts.append(resume.location)
    if resume.linkedin_url:
        contact_parts.append(f"LinkedIn: {resume.linkedin_url}")
    if resume.github_url:
        contact_parts.append(f"GitHub: {resume.github_url}")

    if contact_parts:
        contact_p = doc.add_paragraph()
        contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_run = contact_p.add_run(" | ".join(contact_parts))
        c_run.font.size = Pt(9.5)
        c_run.font.color.rgb = RGBColor(74, 85, 104)

    def add_section_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(title.upper())
        r.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(43, 108, 176)

    # 2. Professional Summary
    if resume.professional_summary:
        add_section_header("Professional Summary")
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(resume.professional_summary)
        r.font.size = Pt(10)

    # 3. Core Skills
    if resume.selected_skills:
        add_section_header("Technical & Core Skills")
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(", ".join(resume.selected_skills))
        r.font.size = Pt(10)

    # 4. Work Experience
    if resume.selected_experiences:
        add_section_header("Work Experience")
        for exp in resume.selected_experiences:
            org = exp.get('organization', '')
            job_title = exp.get('job_title', '')
            dates = f"{exp.get('start_date', '')} – {exp.get('end_date', '')}"

            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(1)
            t_run = p.add_run(f"{job_title} | {org}")
            t_run.bold = True
            t_run.font.size = Pt(10.5)

            p_sub = doc.add_paragraph()
            p_sub.paragraph_format.space_after = Pt(2)
            d_run = p_sub.add_run(dates)
            d_run.italic = True
            d_run.font.size = Pt(9)
            d_run.font.color.rgb = RGBColor(113, 128, 150)

            for b in exp.get('bullets', []):
                bp = doc.add_paragraph(style='List Bullet')
                bp.paragraph_format.space_after = Pt(1)
                br = bp.add_run(b)
                br.font.size = Pt(9.5)

    # 5. Projects
    if resume.selected_projects:
        add_section_header("Technical Projects")
        for proj in resume.selected_projects:
            title = proj.get('title', '')
            tech = proj.get('technologies', '')

            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(1)
            t_run = p.add_run(title)
            t_run.bold = True
            t_run.font.size = Pt(10.5)
            if tech:
                tech_run = p.add_run(f" | Technologies: {tech}")
                tech_run.italic = True
                tech_run.font.size = Pt(9.5)

            for b in proj.get('bullets', []):
                bp = doc.add_paragraph(style='List Bullet')
                bp.paragraph_format.space_after = Pt(1)
                br = bp.add_run(b)
                br.font.size = Pt(9.5)

    # 6. Education
    if resume.selected_educations:
        add_section_header("Education")
        for edu in resume.selected_educations:
            deg = edu.get('degree', '')
            inst = edu.get('institution', '')
            dates = f"{edu.get('start_date', '')} – {edu.get('end_date', '')}"

            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(1)
            e_run = p.add_run(f"{deg} – {inst}")
            e_run.bold = True
            e_run.font.size = Pt(10.5)

            p_sub = doc.add_paragraph()
            p_sub.paragraph_format.space_after = Pt(2)
            d_run = p_sub.add_run(dates)
            d_run.italic = True
            d_run.font.size = Pt(9)

    # 7. Certifications
    if resume.selected_certifications:
        add_section_header("Certifications")
        for cert in resume.selected_certifications:
            bp = doc.add_paragraph(style='List Bullet')
            bp.paragraph_format.space_after = Pt(1)
            r = bp.add_run(f"{cert.get('name')} – {cert.get('issuing_organization')} ({cert.get('issue_date', '')})")
            r.font.size = Pt(9.5)

    # 8. Achievements
    if resume.selected_achievements:
        add_section_header("Achievements")
        for ach in resume.selected_achievements:
            bp = doc.add_paragraph(style='List Bullet')
            bp.paragraph_format.space_after = Pt(1)
            r = bp.add_run(f"{ach.get('title')}: {ach.get('description', '')}")
            r.font.size = Pt(9.5)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
