"""
High-Fidelity, ATS-Compliant PDF Generator using ReportLab.
Produces machine-parseable, single-column documents with selectable text.
"""

import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.units import inch

def generate_resume_pdf(resume):
    """
    Builds a clean, single-column ATS-friendly PDF.
    Returns bytes in a BytesIO buffer.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    styles = getSampleStyleSheet()

    # Custom Clean Styles
    name_style = ParagraphStyle(
        'ResumeName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1a202c'),
        spaceAfter=4,
        alignment=1 # Center
    )

    contact_style = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#4a5568'),
        alignment=1 # Center
    )

    section_heading = ParagraphStyle(
        'ResumeSection',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'ResumeBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#2d3748'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=2
    )

    item_title_style = ParagraphStyle(
        'ResumeItemTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1a202c'),
        spaceAfter=1
    )

    item_subtitle_style = ParagraphStyle(
        'ResumeItemSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#718096'),
        spaceAfter=3
    )

    story = []

    # 1. Header (Name + Contact Details)
    story.append(Paragraph(resume.full_name or "Resume", name_style))

    contact_parts = []
    if resume.email:
        contact_parts.append(resume.email)
    if resume.phone:
        contact_parts.append(resume.phone)
    if resume.location:
        contact_parts.append(resume.location)
    if resume.linkedin_url:
        contact_parts.append("LinkedIn")
    if resume.github_url:
        contact_parts.append("GitHub")
    if resume.portfolio_url:
        contact_parts.append("Portfolio")

    story.append(Paragraph(" • ".join(contact_parts), contact_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e0'), spaceAfter=8))

    # 2. Professional Summary
    if resume.professional_summary:
        story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
        story.append(Paragraph(resume.professional_summary, body_style))
        story.append(Spacer(1, 4))

    # 3. Core Skills
    if resume.selected_skills:
        story.append(Paragraph("TECHNICAL & CORE SKILLS", section_heading))
        skills_text = ", ".join(resume.selected_skills)
        story.append(Paragraph(skills_text, body_style))
        story.append(Spacer(1, 4))

    # 4. Work Experience
    if resume.selected_experiences:
        story.append(Paragraph("WORK EXPERIENCE", section_heading))
        for exp in resume.selected_experiences:
            org = exp.get('organization', '')
            title = exp.get('job_title', '')
            start = exp.get('start_date', '')
            end = exp.get('end_date', '')
            dates = f"{start} – {end}" if start or end else ""
            loc = exp.get('location', '')

            header_line = f"<b>{title}</b> | {org}"
            sub_line = f"{dates} {(' • ' + loc) if loc else ''}"

            story.append(Paragraph(header_line, item_title_style))
            if sub_line.strip():
                story.append(Paragraph(sub_line, item_subtitle_style))

            bullets = exp.get('bullets', [])
            for b in bullets:
                story.append(Paragraph(f"• {b}", bullet_style))
            story.append(Spacer(1, 4))

    # 5. Technical Projects
    if resume.selected_projects:
        story.append(Paragraph("PROJECTS", section_heading))
        for proj in resume.selected_projects:
            title = proj.get('title', '')
            tech = proj.get('technologies', '')
            head = f"<b>{title}</b>" + (f" | <i>Technologies: {tech}</i>" if tech else "")
            story.append(Paragraph(head, item_title_style))

            if proj.get('description'):
                story.append(Paragraph(proj['description'], body_style))

            for b in proj.get('bullets', []):
                # Don't repeat the exact description
                if b != proj.get('description'):
                    story.append(Paragraph(f"• {b}", bullet_style))
            story.append(Spacer(1, 4))

    # 6. Education
    if resume.selected_educations:
        story.append(Paragraph("EDUCATION", section_heading))
        for edu in resume.selected_educations:
            deg = edu.get('degree', '')
            inst = edu.get('institution', '')
            field = edu.get('field_of_study', '')
            start = edu.get('start_date', '')
            end = edu.get('end_date', '')
            dates = f"{start} – {end}" if start or end else ""
            gpa = edu.get('grade_or_gpa', '')

            full_deg = f"<b>{deg}</b>" + (f" in {field}" if field else "")
            story.append(Paragraph(full_deg, item_title_style))

            meta = f"{inst} ({dates})" + (f" • GPA: {gpa}" if gpa else "")
            story.append(Paragraph(meta, item_subtitle_style))
            if edu.get('description'):
                story.append(Paragraph(edu['description'], body_style))
            story.append(Spacer(1, 4))

    # 7. Certifications
    if resume.selected_certifications:
        story.append(Paragraph("CERTIFICATIONS", section_heading))
        for cert in resume.selected_certifications:
            c_text = f"• <b>{cert.get('name')}</b> – {cert.get('issuing_organization')} ({cert.get('issue_date', '')})"
            story.append(Paragraph(c_text, bullet_style))
        story.append(Spacer(1, 4))

    # 8. Achievements
    if resume.selected_achievements:
        story.append(Paragraph("ACHIEVEMENTS & AWARDS", section_heading))
        for ach in resume.selected_achievements:
            a_text = f"• <b>{ach.get('title')}</b>: {ach.get('description', '')}"
            story.append(Paragraph(a_text, bullet_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
