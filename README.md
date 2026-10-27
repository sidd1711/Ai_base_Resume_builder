# ResumeForge AI — AI-Powered ATS Resume Builder

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/Django-5.1%20%7C%206.1-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap 5" />
  <img src="https://img.shields.io/badge/ReportLab-PDF-E23D28?style=for-the-badge" alt="ReportLab" />
  <img src="https://img.shields.io/badge/ATS%20Compatibility-Conscious-059669?style=for-the-badge" alt="ATS Conscious" />
  <img src="https://img.shields.io/badge/Zero%20Hallucinations-Guaranteed-blue?style=for-the-badge" alt="Factual Integrity" />
</p>

> **A modern, production-oriented, fact-preserving web platform that helps candidates build job-specific, ATS-conscious resumes and evaluate keyword coverage without fabricating credentials or false claims.**

---

## 🌟 Overview & Workflow

**ResumeForge AI** solves the core challenge of modern job applications: aligning candidate qualifications with automated Applicant Tracking Systems (ATS) while maintaining strict **factual integrity**.

Unlike generic AI generators that invent past experience or revenue metrics, ResumeForge AI enhances wording using the **STAR method** (Situation, Task, Action, Result) and active power verbs, strictly preserving your real history.

```
┌─────────────────┐       ┌────────────────────┐
│  Master Profile │   +   │   Target Job Post  │
└────────┬────────┘       └─────────┬──────────┘
         │                          │
         ▼                          ▼
   ┌─────────────────────────────────────────┐
   │    NLP Requirement & Keyword Extractor  │
   │    (Required vs. Preferred Skills)      │
   └────────────────────┬────────────────────┘
                        │
                        ▼
   ┌─────────────────────────────────────────┐
   │    Fact-Checked AI/Rule-Based Tailoring │
   │    (STAR Structure & Action Verbs)      │
   └────────────────────┬────────────────────┘
                        │
                        ▼
   ┌─────────────────────────────────────────┐
   │    Transparent ATS Diagnostic Scoring   │
   │    (Keyword Match %, Section Health)    │
   └────────────────────┬────────────────────┘
                        │
                        ▼
   ┌─────────────────────────────────────────┐
   │    Live ATS Template Switcher           │
   │    (5 Universal Single-Column Layouts)  │
   └────────────────────┬────────────────────┘
                        │
                        ▼
   ┌─────────────────────────────────────────┐
   │    High-Fidelity PDF & Word DOCX Export │
   └─────────────────────────────────────────┘
```

---

## 🚀 Key Features

### 1. Master Profile Management
- Maintain your genuine personal details, education history, technical skills, projects, employment experience, certifications, and awards in one place.
- **Resume Upload & Parser**: Upload existing PDF or DOCX resumes to pre-fill profile data safely with an interactive review screen (never silently overwriting existing information).

### 2. Job Description NLP Analyzer
- **Workflow A (Role Selector)**: Searchable preset archetypes (Python Developer, Full-Stack, Data Analyst, DevOps, etc.).
- **Workflow B (Custom JD)**: Paste any job description to extract mandatory required skills, preferred qualifications, experience benchmarks, and degree requirements.
- **Canonical Alias Normalization**: Resolves equivalent terms (e.g., `Postgres` $\rightarrow$ `PostgreSQL`, `K8s` $\rightarrow$ `Kubernetes`, `Node` $\rightarrow$ `Node.js`).

### 3. Truth-Preserving AI & Offline Engine
- Enhances bullet points with strong action verbs and STAR structure.
- **Zero Hallucination Policy**: Never invents companies, dates, degrees, metrics, or technologies not confirmed by the user.
- **100% Offline Capability**: Fully functional deterministic rule-based NLP engine runs locally without internet access or API keys.
- **Optional Gemini API**: Supports Google Gemini API for natural language polish.
- **Interactive AI Polish**: Single-bullet refinement button via asynchronous AJAX.

### 4. 5 ATS-Compliant Resume Templates
- **Classic Professional**: Universal single-column standard for corporate and general applications.
- **Modern Minimal**: Clean typography with balanced whitespace.
- **Technical Resume**: Prioritizes technical stack, architectural contributions, and project repositories.
- **Graduate & Fresher**: Highlights academic coursework, hackathons, and certifications.
- **Experienced Professional**: Chronological layout emphasizing verified milestones and team leadership.

### 5. Transparent ATS Diagnostic Scoring
- **Keyword Coverage Rate**: $\frac{\text{Matched Required Keywords}}{\text{Total Required Keywords}} \times 100$
- **Section Completeness**: Audits Contact, Summary, Skills, Experience, Projects, and Education.
- **Formatting Diagnostics**: Flags excessively long bullet points, malformed emails, and invalid formats.
- **Profile Gap Finder**: Identifies verified skills already in your profile that are missing from your resume draft.

### 6. Document Generation
- **Machine-Readable PDF**: Generated via ReportLab with selectable text and clean reading hierarchy.
- **Editable Word (.docx)**: Generated via `python-docx` using standard Word headings and bullet styles (free of text boxes or nested tables).

### 7. Resume Versioning & Rollback
- Automatically creates historical snapshots on save.
- Compare and revert to any earlier version with one click.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.12, Django 5.1 / 6.1 |
| **Frontend** | HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons, JavaScript (Fetch API) |
| **Document Processing** | ReportLab (PDF), python-docx (Word DOCX), PyMuPDF (PDF Text Verification) |
| **NLP & AI** | Deterministic Regex Tokenizer, STAR Transformer, Optional Google Gemini API |
| **Database** | SQLite (development default), MySQL (production-ready switchable) |

---

## ⚡ Quick Start & Local Setup

### 1. Clone the Repository
```powershell
git clone https://github.com/sidd1711/Ai_base_Resume_builder.git
cd Ai_base_Resume_builder
```

### 2. Set Up Virtual Environment
```powershell
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run Migrations & Seed Demo Data
```powershell
python manage.py migrate
python manage.py seed_demo
```

### 5. Start the Development Server
```powershell
python manage.py runserver
```

Open your browser and navigate to:
- **Application**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Dashboard**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 👤 Pre-Configured Demo Accounts

For immediate evaluation, sample credentials have been pre-seeded:

| Account Type | Username | Password | Purpose |
|---|---|---|---|
| **Demo Candidate** | `alex_dev` | `Password123!` | Pre-populated profile, job analysis, tailored resume, and ATS report |
| **System Admin** | `admin` | `AdminPassword123!` | Full access to Django admin portal |

---

## 🧪 Automated Testing

Run the automated test suite (covering Auth, Profile CRUD, Ownership Isolation, Job NLP, AI Guardrails, ATS Engine, and Document Exporters):

```powershell
python manage.py test
```

```
Ran 16 tests in 70.555s
OK
System check identified no issues (0 silenced).
```

---

## 🔒 Privacy & Ethical Integrity

- **User Data Isolation**: Queries are strictly scoped per authenticated user (`request.user`).
- **No Data Fabrication**: We strictly adhere to fact preservation. The application never invents unverified achievements, false job titles, or fake qualifications.
- **Disclaimer**: ResumeForge AI provides diagnostic alignment metrics based on standard ATS parsing heuristics. We do not claim or guarantee that any resume will pass every automated ATS or guarantee employment.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
