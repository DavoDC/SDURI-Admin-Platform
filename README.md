# SDURI Admin Platform

A web application built to administer the **Summer Down Under Research Internship (SDURI)** program at the University of Western Australia (UWA). It replaces manual Qualtrics-based workflows with a unified platform where students can apply for research internships and supervisors can manage and fill their projects.

---

## Background

**Department:** Computer Science & Software Engineering, The University of Western Australia
**Course:** CITS3200 Professional Computing (2020)

Prior to this platform, the SDURI program relied on Qualtrics forms for student applications and supervisor project submissions. This project replaced those with a purpose-built web platform to streamline matching, reduce administrative overhead, and maintain a record of past internships.

---

## Features

### Student Portal
- Register and verify account via email confirmation
- Complete a multi-page profile (personal details, passport info, address, emergency contact, university details, English proficiency, long-answer questions, CV and transcript uploads)
- Browse available research projects
- Submit applications for up to two projects with preference ranking
- View application status (Pending / Accepted / Denied)

### Supervisor Portal
- Register and verify account
- Create, edit, and manage research projects (title, description, skills, keywords, location, duration, max students)
- Archive and re-activate past projects for re-use in future years
- Review student applications (CV, transcript, personal statement, long-answer responses)
- Accept or deny student applicants after the application deadline

### Admin Panel
- Full database management via Flask-Admin interface (Users, Students, Supervisors, Projects, Deadlines, Admin Tasks)
- Set and manage key program deadlines:
  - Supervisor project submission deadline
  - Student application deadline
  - Supervisor candidate examination deadline
  - Round 1 / 2 / 3 decision deadlines
- Create and resolve admin tasks linked to specific users
- Remove or correct any database entries

### Authentication System
- Email/password registration with email confirmation (token-based)
- Password reset via email
- Role-based access control: Student, Supervisor, Administrator
- JWT token support for API access

---

## Technical Stack

### Backend
| Library | Version | Purpose |
|---|---|---|
| Python | 3.x | Primary language |
| Flask | 1.1.2 | Web framework |
| Flask-SQLAlchemy | 2.4.1 | ORM / database access |
| Flask-Migrate | 2.5.3 | Database schema migrations |
| Flask-Login | 0.5.0 | Session-based authentication |
| Flask-Mail | 0.9.1 | Email (Gmail SMTP) |
| Flask-WTF / WTForms | 0.14.3 / 2.3.1 | Form handling and validation |
| Flask-Bootstrap | 3.3.7.1 | Bootstrap integration |
| Flask-Admin | 1.5.6 | Admin interface |
| Flask-JWT-Extended | 3.24.1 | JWT tokens for API |
| Flask-HTTPAuth | 4.0.0 | HTTP authentication |
| Flask-Bcrypt | 0.7.1 | Password hashing |
| SQLAlchemy | 1.3.16 | ORM toolkit |
| Alembic | 1.4.2 | Migration engine |
| python-dotenv | 0.13.0 | Environment variable loading |
| email-validator | 1.0.5 | Email validation |
| PyJWT | 1.7.1 | JWT handling |

### Frontend
- HTML5 with **Jinja2** templating
- CSS3
- JavaScript
- Bootstrap 3.3.7.1

### Database
- **SQLite** (default, file: `sduri.db`)
- Supports other SQL databases via SQLAlchemy's URI configuration

---

## Database Schema

| Model | Key Fields |
|---|---|
| `User` | id, name, email, password (hashed), role (Student/Supervisor/Administrator), confirmed, registered_on |
| `Student` | Personal info, address, emergency contact, university details, English proficiency, long-answer responses, file uploads (CV, transcript), two project application slots |
| `Supervisor` | faculty, school, linked User |
| `Project` | title, description, skills, keywords, location, duration (weeks), max students, co-supervisor, linked User |
| `Deadline` | supervisor_project_dl, student_application_dl, supervisor_examine_dl, round1/2/3 |
| `AdminTask` | description, action, relatedUserEmail, resolved, resolved_on |

---

## Project Structure

```
SDURI-Admin-Platform/
├── app.py                  # Application entry point
├── config.py               # Configuration (DB, mail, secrets)
├── requirements.txt        # Python dependencies
├── setupDatabase.sh        # One-time database initialisation script
├── startSite.sh            # Site startup script
└── app/
    ├── __init__.py         # App factory, extension setup, blueprint registration
    ├── models.py           # SQLAlchemy database models
    ├── routes.py           # Core routes
    ├── forms.py            # WTForms form definitions
    ├── decorators.py       # Custom route decorators
    ├── email.py            # Email utility functions
    ├── api/                # REST API endpoints
    ├── auth/               # Authentication (routes, forms, models, tokens)
    ├── helper/             # Logging and utility helpers
    ├── myadmin/            # Admin portal routes and models
    ├── routing/            # Role-based routing (student.py, supervisor.py)
    ├── static/             # CSS, JavaScript, images
    └── templates/          # Jinja2 HTML templates
        ├── auth/           # Login, register, password reset
        ├── myadmin/        # Admin interface pages
        ├── student/        # Student portal pages
        ├── supervisor/     # Supervisor portal pages
        └── templ/          # Shared/reusable template components
```

---

## Installation

### Prerequisites
- Python 3.x — download from https://www.python.org/downloads/

### Steps

**1. Clone the repository and navigate into it:**
```bash
git clone <repo-url>
cd SDURI-Admin-Platform
```

**2. Install Python dependencies** (once only):
```bash
pip3 install -r requirements.txt
```

**3. Initialise the database** (once only):
```bash
flask db init
flask db migrate -m "Creating Tables"
flask db upgrade
```
This creates `sduri.db`. Back this file up to preserve data.

**4. Start the development server:**
```bash
flask run
```

Or use the provided script:
```bash
bash startSite.sh
```

For advanced options (custom host/port), see the Flask documentation.

> **Note:** Email functionality requires valid Gmail SMTP credentials configured in `config.py` or a `.env` file.

---

## Development Timeline

The project was developed over **~12 weeks** across three sprints as part of the CITS3200 unit at UWA:

| Milestone | Date |
|---|---|
| Project kick-off / charter | 14 August 2020 |
| Sprint 1 due | 19 August 2020 |
| Interim report / workshop | 16 September 2020 |
| Active development ends | October 2020 |
| Sprint 3 / project close | 21 November 2020 |

