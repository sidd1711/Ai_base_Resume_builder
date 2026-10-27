# ResumeForge AI — Project Structure

This document outlines the architectural organization of the **ResumeForge AI** project. The project is designed with a modular Django architecture, cleanly separating business logic, AI/NLP analysis, document generation, and presentation.

```
AI Base Resume Builder/
├── .env.example                     # Sample environment variables (SECRET_KEY, GEMINI_API_KEY, DB config)
├── .env                             # Local environment secrets (not committed to VCS)
├── .gitignore                       # Git ignore file for Python, Django, SQLite, media, env
├── memory.md                        # Living progress log: completed tasks & next steps
├── structure.md                     # Complete project architecture & directory map (this file)
├── commands.md                      # Operational guide & terminal execution commands
├── requirements.txt                 # Pinned Python package dependencies
├── manage.py                        # Django administrative CLI
│
├── config/                          # Project Root Configuration
│   ├── __init__.py
│   ├── asgi.py                      # ASGI entry point
│   ├── wsgi.py                      # WSGI entry point
│   ├── urls.py                      # Global URL router
│   └── settings.py                  # Environment-driven Django settings
│
├── accounts/                        # User Authentication & Security App
│   ├── __init__.py
│   ├── admin.py                     # Admin registration
│   ├── apps.py                      # App configuration
│   ├── forms.py                     # Registration, Login, Profile forms
│   ├── models.py                    # Custom User model / security settings
│   ├── urls.py                      # /accounts/ routes
│   ├── views.py                     # Auth handlers (login, register, logout, profile settings)
│   └── tests.py                     # Auth unit & security tests
│
├── profiles/                        # Professional Profile Management App
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                     # Forms & Formsets for Education, Experience, Skills, Projects
│   ├── models.py                    # UserProfile, Education, Skill, Project, Experience, Certification
│   ├── resume_parser.py             # Extracts text & fields from uploaded PDF/DOCX
│   ├── urls.py                      # /profile/ routes
│   ├── views.py                     # Profile view, dynamic multi-section editors, resume upload
│   └── tests.py                     # Tests for profile CRUD and ownership
│
├── job_analyzer/                    # Job Role & Description NLP App
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                     # Job Description paste form & Role selector
│   ├── models.py                    # JobAnalysis model (stored target requirements)
│   ├── skill_extractor.py           # NLP & rule-based keyword/skill extraction engine
│   ├── skills_data.py               # Normalized taxonomy of tech skills, tools, and aliases
│   ├── services.py                  # Job analysis service layer
│   ├── urls.py                      # /jobs/ routes
│   ├── views.py                     # Role picker, JD parser view, analysis breakdown
│   └── tests.py                     # Tests for skill extraction and alias normalization
│
├── resume_builder/                  # Core Resume Construction & AI Content Engine
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                     # Multi-step resume wizard forms
│   ├── models.py                    # Resume, ResumeVersion, ResumeSection models
│   ├── services.py                  # Content tailoring, STAR bullet formatting
│   ├── ai_generator.py              # LLM (Gemini API) integration with strict factual guardrails
│   ├── rule_based_generator.py      # 100% offline rule-based fallback rewriter
│   ├── urls.py                      # /builder/ routes
│   ├── views.py                     # Step-by-step wizard views, live preview endpoint
│   └── tests.py                     # Integrity tests: never fabricate user history
│
├── ats_checker/                     # ATS Compatibility & Scoring Engine
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                    # ResumeAnalysis audit results
│   ├── analyzer.py                  # Keyword coverage, section completeness & format checker
│   ├── suggestions.py               # Honest, category-specific improvement suggestions
│   ├── urls.py                      # /ats-checker/ routes
│   ├── views.py                     # Score overview, keyword gap view, tips report
│   └── tests.py                     # Scoring formula and formatting check tests
│
├── document_generator/              # High-Fidelity Export App (PDF & DOCX)
│   ├── __init__.py
│   ├── pdf_generator.py             # Machine-readable PDF generation (ReportLab / xhtml2pdf)
│   ├── docx_generator.py            # Clean, table-free DOCX generation (python-docx)
│   ├── template_adapters.py         # Maps resume JSON to layout formats
│   ├── urls.py                      # /export/pdf/ and /export/docx/ routes
│   ├── views.py                     # Download endpoints with proper mime-types
│   └── tests.py                     # Document generation and text-extractability tests
│
├── templates/                       # Django HTML Templates (Bootstrap 5)
│   ├── base.html                    # Base layout with navbar, footer, messages, alerts
│   ├── landing.html                 # Modern, high-conversion landing page
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── password_reset.html
│   │   └── account_settings.html
│   ├── dashboard/
│   │   └── dashboard.html           # User hub (resumes, metrics, quick actions)
│   ├── profiles/
│   │   ├── profile_detail.html
│   │   ├── profile_form.html
│   │   └── upload_resume.html
│   ├── job_analyzer/
│   │   ├── analyze_job.html
│   │   └── analysis_results.html
│   ├── resume_builder/
│   │   ├── wizard_step1_target.html
│   │   ├── wizard_step2_content.html
│   │   ├── wizard_step3_ai_tune.html
│   │   ├── wizard_step4_template.html
│   │   ├── resume_edit.html
│   │   └── resume_preview.html
│   ├── ats_checker/
│   │   └── ats_report.html
│   └── resume_templates/            # 5 Clean, ATS-Compliant Layouts
│       ├── classic_professional.html
│       ├── modern_minimal.html
│       ├── technical_resume.html
│       ├── graduate_fresher.html
│       └── experienced_professional.html
│
├── static/                          # Static Assets
│   ├── css/
│   │   ├── custom.css               # Clean typography, subtle accents, spacing
│   │   └── resume_print.css         # Print & export stylesheet
│   ├── js/
│   │   ├── main.js                  # Global UI interactions, toasts, modals
│   │   ├── dynamic_formset.js       # Add/remove education/skill/project cards
│   │   └── resume_preview.js        # Live preview updates
│   └── images/
│       ├── logo.svg
│       └── template_previews/
│
├── media/                           # User-uploaded files (resumes, exports)
│   ├── uploads/
│   └── exports/
│
└── tests/                           # Global Integration & E2E Test Suite
    └── test_end_to_end.py
```

---

## Architectural Principles

1. **User Data Isolation**: All queries are filtered by `request.user`. Users can never read, modify, or export another user's profile, resume, or analysis reports.
2. **Deterministic Fallbacks**: Every AI feature has a reliable, zero-latency rule-based alternative that functions without internet or API keys.
3. **Data Integrity (Truth in Resumes)**: The AI engine improves tone, clarity, and keyword alignment, but never fabricates employment history, skills, or degrees.
4. **ATS Standards**: Resumes are generated using clean, single-column reading orders, standard section headers, and parseable text layers.
