"""
Resume Parser Service for PDF and DOCX documents.
Extracts contact information, sections, and keywords into an editable structured format.
Never directly overwrites user data without user confirmation.
"""

import re
import os

SKILL_LEXICON = [
    # Languages
    'python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'c', 'ruby', 'go', 'golang', 'rust',
    'php', 'swift', 'kotlin', 'sql', 'html', 'html5', 'css', 'css3', 'sass', 'bash', 'r',
    # Frameworks & Libraries
    'django', 'flask', 'fastapi', 'react', 'react.js', 'vue', 'vue.js', 'angular', 'next.js',
    'node.js', 'express', 'spring boot', 'laravel', 'asp.net', 'bootstrap', 'tailwind', 'tailwind css',
    'jquery', 'redux', 'pytorch', 'tensorflow', 'scikit-learn', 'pandas', 'numpy',
    # Databases & Caching
    'postgresql', 'postgres', 'mysql', 'sqlite', 'mongodb', 'redis', 'cassandra', 'oracle',
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'git', 'github', 'gitlab',
    'ci/cd', 'jenkins', 'linux', 'nginx', 'terraform', 'graphql', 'rest api', 'microservices',
    # Soft skills & domains
    'agile', 'scrum', 'problem solving', 'team leadership', 'communication', 'critical thinking'
]

def extract_text_from_file(file_obj, filename):
    """Safely extracts plain text from PDF or DOCX file object."""
    ext = filename.split('.')[-1].lower()
    text = ""

    if ext == 'pdf':
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(stream=file_obj.read(), filetype="pdf")
            for page in doc:
                text += page.get_text() + "\n"
        except ImportError:
            # Fallback simple reader or error explanation
            try:
                import pypdf
                reader = pypdf.PdfReader(file_obj)
                for page in reader.pages:
                    text += (page.extract_text() or "") + "\n"
            except Exception as e:
                text = f"[Text extraction requires PyMuPDF. Error: {str(e)}]"
        except Exception as e:
            text = f"[Error reading PDF: {str(e)}]"

    elif ext == 'docx':
        try:
            import docx
            doc = docx.Document(file_obj)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            text = "\n".join(paragraphs)
        except Exception as e:
            text = f"[Error reading DOCX: {str(e)}]"

    return text.strip()


def parse_resume_content(text):
    """
    Parses plain text from a resume and extracts structured components.
    Returns a dictionary of extracted fields.
    """
    data = {
        'full_name': '',
        'email': '',
        'phone': '',
        'linkedin_url': '',
        'github_url': '',
        'extracted_skills': [],
        'summary': '',
        'raw_text_preview': text[:2000] if text else '',
    }

    if not text:
        return data

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Extract Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_match:
        data['email'] = email_match.group(0).lower()

    # Extract Phone
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    if phone_match:
        data['phone'] = phone_match.group(0).strip()

    # Extract LinkedIn URL
    linkedin_match = re.search(r'(https?://(?:www\.)?linkedin\.com/in/[\w\-]+)', text, re.IGNORECASE)
    if linkedin_match:
        data['linkedin_url'] = linkedin_match.group(0)

    # Extract GitHub URL
    github_match = re.search(r'(https?://(?:www\.)?github\.com/[\w\-]+)', text, re.IGNORECASE)
    if github_match:
        data['github_url'] = github_match.group(0)

    # Extract Name (typically found in the top 3 non-empty lines, avoiding headers/labels)
    for line in lines[:5]:
        if (len(line.split()) <= 4 and
            not re.search(r'(@|phone|email|curriculum|resume|page|\d{4})', line, re.IGNORECASE) and
            any(c.isalpha() for c in line)):
            data['full_name'] = line
            break

    # Extract recognizable skills from lexicon
    lower_text = " " + text.lower() + " "
    matched_skills = set()
    from job_analyzer.skills_data import SKILL_ALIASES
    for skill in SKILL_LEXICON:
        # Use regex boundary matching
        pattern = r'(?<![a-z0-9])' + re.escape(skill) + r'(?![a-z0-9])'
        if re.search(pattern, lower_text):
            canonical = SKILL_ALIASES.get(skill.lower(), skill.capitalize())
            matched_skills.add(canonical)

    data['extracted_skills'] = sorted(list(matched_skills))

    # Extract Summary / Objective section if recognizable
    summary_match = re.search(
        r'(?:summary|professional summary|profile|about me|career objective)[\s:]*\n+(.*?)(?=\n+[A-Z\s]{4,}:|\n+(?:education|experience|skills|projects)\b)',
        text,
        re.IGNORECASE | re.DOTALL
    )
    if summary_match:
        data['summary'] = summary_match.group(1).strip()[:800]

    return data
