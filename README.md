# AI-Powered Recruitment Assistant

Django-based web application for automated resume screening and skill matching. Built as a final-year B.Tech AI/DS project at Saranathan College of Engineering.

## Overview

This system automates the recruitment process by:
1. **Parsing resumes** (PDF/DOCX) and extracting candidate information
2. **Matching candidate skills** with job requirements and calculating match scores

Reduces manual screening time, removes human bias, and provides objective candidate rankings.

## Features

### Module 1: Resume Upload & Parsing
- Upload resume files (PDF, DOCX)
- Extract raw text from documents
- Normalize and clean extracted text
- Extract metadata (email, phone, skills)
- Store parsed data in database

### Module 2: Resume Screening & Skill Matching
- Accept job description input
- Extract required skills from JD
- Compare candidate skills with job requirements
- Calculate match percentage score
- Display ranked results with skill breakdown

## Tech Stack

**Backend:**
- Python 3.11+
- Django 4.2.7

**Frontend:**
- HTML5
- CSS3 (Bootstrap 5.1.3)
- JavaScript

**Libraries:**
- PyPDF2 3.0.1 (PDF parsing)
- python-docx 1.1.0 (DOCX parsing)

**Database:**
- SQLite (default Django DB)

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

## Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/AadhithyaPrakash/recruitment_assistant.git
cd recruitment_assistant
```

### 2. Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Required Directories

```bash
mkdir media
```

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow prompts to set username, email, and password.

### 7. Start Development Server

```bash
python manage.py runserver
```

Server will start at `http://127.0.0.1:8000/`

## Usage

### Analyze Resume

1. Open `http://127.0.0.1:8000/` in browser
2. Enter job title and paste job description
3. Upload candidate resume (PDF or DOCX, max 5MB)
4. Click "Analyze Resume"
5. View results showing:
   - Match percentage score
   - Required skills vs candidate skills
   - Matched skills (highlighted in green)
   - Extracted resume text
   - Contact information

### Admin Panel

1. Access `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Manage resumes, jobs, and match results

## Project Structure

```
recruitment_assistant/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # SQLite database
├── media/                             # Uploaded resume files
├── recruitment_assistant/             # Main project folder
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Root URL configuration
│   └── wsgi.py                        # WSGI configuration
└── screening/                         # Main application
    ├── models.py                      # Database models (Resume, Job, MatchResult)
    ├── views.py                       # Request handlers
    ├── urls.py                        # App URL routes
    ├── admin.py                       # Admin interface config
    ├── services/                      # Business logic layer
    │   ├── parser.py                  # PDF/DOCX text extraction
    │   ├── extractor.py               # Metadata extraction (email, phone, skills)
    │   └── matcher.py                 # Skill matching algorithm
    ├── templates/screening/           # HTML templates
    │   ├── analyze.html               # Upload form page
    │   └── result.html                # Results display page
    └── static/screening/
        └── skills.py                  # Skill keyword dictionary (50+ skills)
```

## How It Works

### Resume Parsing Pipeline

1. **File Upload:** User uploads PDF/DOCX resume
2. **Text Extraction:** 
   - PDF: PyPDF2 extracts text from pages
   - DOCX: python-docx reads document paragraphs
3. **Text Normalization:**
   - Convert to lowercase
   - Remove extra whitespace
   - Clean special characters
4. **Metadata Extraction:**
   - Email: Regex pattern matching
   - Phone: Regex with multiple format support
   - Skills: Keyword matching from predefined list

### Skill Matching Algorithm

1. **JD Parsing:** Extract required skills from job description text
2. **Resume Parsing:** Extract candidate skills from resume text
3. **Skill Comparison:** Find intersection between JD skills and resume skills
4. **Score Calculation:**
   ```
   Match Score = (Matched Skills Count / JD Skills Count) × 100
   ```
5. **Result Display:** Show matched skills, missing skills, and percentage

### Skill Dictionary

50+ technical skills covering:
- Programming languages (Python, Java, JavaScript, C++, etc.)
- Web technologies (HTML, CSS, React, Django, Flask, etc.)
- Data Science/AI (Machine Learning, Deep Learning, NLP, TensorFlow, PyTorch, etc.)
- Databases (SQL, MySQL, PostgreSQL, MongoDB, etc.)
- DevOps/Cloud (AWS, Azure, Docker, Kubernetes, Git, etc.)

Located in: `screening/static/screening/skills.py`

## Database Schema

### Resume Model
- `id`: Primary key
- `candidate_name`: Extracted name (optional)
- `email`: Extracted email
- `phone`: Extracted phone number
- `resume_file`: Uploaded file path
- `extracted_text`: Full parsed text
- `created_at`: Upload timestamp

### Job Model
- `id`: Primary key
- `job_title`: Position title
- `description`: Full job description text
- `created_at`: Creation timestamp

### MatchResult Model
- `id`: Primary key
- `resume`: Foreign key to Resume
- `job`: Foreign key to Job
- `score`: Match percentage (0-100)
- `matched_skills`: Comma-separated matched skills
- `created_at`: Analysis timestamp

## Troubleshooting

### Issue: "No module named 'screening'"

**Solution:**
```bash
# Verify screening app structure exists
dir screening  # Windows
ls screening   # Linux/Mac

# Ensure __init__.py exists
New-Item screening\__init__.py  # Windows
touch screening/__init__.py     # Linux/Mac
```

### Issue: "no such table: screening_resume"

**Solution:**
```bash
python manage.py makemigrations screening
python manage.py migrate
```

### Issue: File upload fails

**Solution:**
- Check `media/` directory exists
- Verify file size under 5MB
- Ensure file format is PDF or DOCX

### Issue: No skills detected

**Solution:**
- Job description must contain skills from keyword list
- Check `screening/static/screening/skills.py` for available skills
- Skills are case-insensitive but must match exactly (e.g., "python", "machine learning")

## Sample Test Data

### Test Job Description
```
Job Title: AI Engineer (Entry-Level)

We are looking for an AI Engineer to work on machine learning and NLP projects.

Required Skills:
- Python
- Machine Learning
- Deep Learning
- TensorFlow or PyTorch
- SQL
- Git

Responsibilities:
- Build ML models
- Deploy AI solutions
- Work with Python and Django
```

### Expected Output
- System extracts: python, machine learning, deep learning, tensorflow, pytorch, sql, git, django
- Match score calculated based on resume skills
- Result page shows matched vs missing skills

## Future Enhancements

- Interview question generation based on job role
- Multi-resume batch processing and ranking
- Advanced NER using spaCy/NLTK
- Experience level extraction
- Certification and education parsing
- API endpoint for programmatic access
- Machine learning-based matching (beyond keyword)
- Integration with ATS platforms

## Academic Context

**Project Type:** Final Year B.Tech Project (AI/DS)

**Institution:** Saranathan College of Engineering

**Review Modules:**
1. Resume Upload & Parsing Module
2. Resume Screening & Skill Matching Module

**Documentation:**
- Abstract
- Problem Statement
- Objectives
- Module-wise Description
- SRS Document

## Contributing

This is an academic project. For collaboration:
1. Fork the repository
2. Create feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Add feature"`)
4. Push to branch (`git push origin feature-name`)
5. Open Pull Request

## License

Educational use only. Not licensed for commercial deployment.

## Contact

**Developer:** Aadhithya Prakash  
**Role:** AI Intern, Intellect Design Arena Ltd  
**Institution:** Saranathan College of Engineering  
**GitHub:** [@AadhithyaPrakash](https://github.com/AadhithyaPrakash)

## Acknowledgments

- Saranathan College of Engineering, Department of AI & Data Science
- Project Guide and Faculty Reviewers
- Intellect Design Arena Ltd for internship support

---

**Project Status:** ✅ Review Ready (Jan 19-20, 2026)

For questions or issues, open a GitHub issue or contact the developer.