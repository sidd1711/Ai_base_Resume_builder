# ResumeForge AI — Command Execution Guide

This document contains all terminal commands required to run, test, and maintain the **ResumeForge AI** platform.

---

## 1. Quick Start (Run the Application Right Now)

The virtual environment and database migrations are already set up and pre-seeded.

Run the local development server:
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

Open your browser and navigate to:
- **Application Landing Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **User Dashboard**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
- **Django Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 2. Pre-Configured Demo Credentials

For quick evaluation, sample accounts have already been seeded into the database:

| Role | Username | Password | Notes |
|---|---|---|---|
| **Demo Candidate** | `alex_dev` | `Password123!` | Pre-populated profile, job analysis, resume, and ATS report |
| **System Admin** | `admin` | `AdminPassword123!` | Full access to Django admin portal |

*(Or click **"Get Started Free"** on the landing page to register a new candidate account)*

---

## 3. Running Automated Tests

Run the full automated test suite (all 16 tests covering Auth, Profiles, Job NLP, AI Guardrails, ATS Engine, and Document Exporters):

```powershell
.\venv\Scripts\python.exe manage.py test
```

### Run Tests for Specific Modules:
```powershell
# Authentication & security tests
.\venv\Scripts\python.exe manage.py test accounts

# Profile CRUD, ownership isolation & resume parsing tests
.\venv\Scripts\python.exe manage.py test profiles

# Job description NLP & skill alias normalization tests
.\venv\Scripts\python.exe manage.py test job_analyzer

# Resume builder & fact-preserving bullet tailoring tests
.\venv\Scripts\python.exe manage.py test resume_builder

# ATS keyword coverage & scoring formula tests
.\venv\Scripts\python.exe manage.py test ats_checker

# PDF (ReportLab) & DOCX (python-docx) export tests
.\venv\Scripts\python.exe manage.py test document_generator
```

---

## 4. Environment Configuration (`.env`)

Configuration settings are stored in `.env`. A sample is provided in `.env.example`:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `True` for development, `False` for production
- `ALLOWED_HOSTS`: `127.0.0.1,localhost`
- `GEMINI_API_KEY`: *(Optional)* Your Google Gemini API key. If left blank, ResumeForge AI automatically runs its built-in 100% offline rule-based NLP engine.
- `DATABASE_ENGINE`: Defaults to SQLite (`django.db.backends.sqlite3`)

---

## 5. Database Migrations & Seeding

If you make changes to models or need to re-seed demo data:

```powershell
# Make migrations
.\venv\Scripts\python.exe manage.py makemigrations

# Apply migrations
.\venv\Scripts\python.exe manage.py migrate

# Seed or re-seed sample demo data
.\venv\Scripts\python.exe manage.py seed_demo
```

---

## 6. Switching to MySQL (Optional Production Step)

1. Ensure MySQL server is running and create the database:
   ```sql
   CREATE DATABASE resumeforge_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Install the MySQL client:
   ```powershell
   .\venv\Scripts\pip.exe install mysqlclient
   ```
3. Update `.env`:
   ```env
   DATABASE_ENGINE=django.db.backends.mysql
   DB_NAME=resumeforge_db
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```
4. Run migrations:
   ```powershell
   .\venv\Scripts\python.exe manage.py migrate
   ```
