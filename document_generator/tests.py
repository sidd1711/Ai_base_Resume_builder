from django.test import TestCase
from django.contrib.auth.models import User
from resume_builder.models import Resume
from document_generator.pdf_generator import generate_resume_pdf
from document_generator.docx_generator import generate_resume_docx
import fitz  # PyMuPDF

class DocumentGeneratorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='docuser', password='Password123!')
        self.resume = Resume.objects.create(
            user=self.user,
            title='Full Stack Resume',
            target_role='Full Stack Developer',
            full_name='Jordan Developer',
            email='jordan@example.com',
            phone='+1 (555) 012-3456',
            location='Seattle, WA',
            professional_summary='Accomplished Full Stack engineer with strong Python and React background.',
            selected_skills=['Python', 'Django', 'React', 'PostgreSQL', 'Docker'],
            selected_educations=[{
                'degree': 'Bachelor of Science in Computer Science',
                'institution': 'University of Washington',
                'start_date': '2019',
                'end_date': '2023',
                'grade_or_gpa': '3.9 / 4.0'
            }],
            selected_projects=[{
                'title': 'Cloud Orchestrator',
                'technologies': 'Python, Docker, Kubernetes',
                'description': 'Automated multi-node container deployment system.',
                'bullets': ['Constructed automated CI/CD pipeline reducing deployment latency.']
            }],
            selected_experiences=[{
                'job_title': 'Software Engineer',
                'organization': 'Amazon',
                'start_date': '2023',
                'end_date': 'Present',
                'bullets': ['Architected high-throughput payment webhook consumers processing 10k RPS.']
            }],
            selected_certifications=[{
                'name': 'AWS Certified Developer',
                'issuing_organization': 'Amazon Web Services',
                'issue_date': '2024'
            }]
        )

    def test_pdf_generation_valid_and_extractable(self):
        pdf_buffer = generate_resume_pdf(self.resume)
        pdf_bytes = pdf_buffer.getvalue()

        # Valid PDF header
        self.assertTrue(pdf_bytes.startswith(b'%PDF-'))
        self.assertGreater(len(pdf_bytes), 1000)

        # PyMuPDF verification: extract text from generated PDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        self.assertGreater(doc.page_count, 0)

        extracted_text = ""
        for page in doc:
            extracted_text += page.get_text()

        # Ensure crucial candidate details and sections are parseable
        self.assertIn("Jordan Developer", extracted_text)
        self.assertIn("jordan@example.com", extracted_text)
        self.assertIn("PROFESSIONAL SUMMARY", extracted_text)
        self.assertIn("Python", extracted_text)
        self.assertIn("Amazon", extracted_text)

    def test_docx_generation_valid(self):
        docx_buffer = generate_resume_docx(self.resume)
        docx_bytes = docx_buffer.getvalue()

        # DOCX is a zip file starting with PK\x03\x04
        self.assertTrue(docx_bytes.startswith(b'PK\x03\x04'))
        self.assertGreater(len(docx_bytes), 1000)
