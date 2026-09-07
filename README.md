# Student Result Management System (SRMS)

### IGNOU BCA Final Year Major Project — BCSP-064

**Student Name:** Prince Kumar  
**Enrolment Number:** 2350382985  
**Programme:** Bachelor of Computer Applications (BCA)  
**Course Code:** BCSP-064  
**Study Centre:** Maharaja Agrasen College (07107)  
**Session:** July 2023  

---

## 📋 Project Overview

The **Student Result Management System (SRMS)** is a secure, role-based, database-driven web application developed using **Python Flask** and **SQLite/PostgreSQL**.

The system replaces manual, paper-based, and spreadsheet-driven academic evaluation workflows with an automated three-tier architecture.

### Key Modules

#### 👨‍💼 Admin Module

- Complete student profile management (CRUD)
- Subject and curriculum maintenance
- Transactional CSV bulk student uploads
- Academic reporting and management
- User and academic data administration

#### 👨‍🏫 Faculty Module

- Student marks entry portal
- Internal marks validation: **0–30**
- External marks validation: **0–70**
- Real-time total score calculation
- Real-time grade calculation
- Save marks as draft
- Permanent marks finalization and locking
- Protection against unauthorized modification of finalized marks

#### 👨‍🎓 Student Module

- Secure individual login
- Personal academic profile
- Semester-wise result listings
- Published academic records
- Printable A4-compliant marksheets

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Backend | Python 3.10+ |
| Web Framework | Flask 3.x |
| Architecture | Application Factory Pattern |
| ORM | Flask-SQLAlchemy / SQLAlchemy 2.x |
| Authentication | Flask-Login |
| Forms & CSRF | Flask-WTF / WTForms |
| Password Hashing | Werkzeug Security (PBKDF2-SHA256) |
| Database | SQLite 3 / PostgreSQL |
| Frontend | HTML5, CSS3, JavaScript ES6 |
| UI Framework | Bootstrap 5 |
| Icons | Bootstrap Icons |
| Testing | Pytest |

---

## 📁 Directory Structure

```text
student-result-management-system/
│
├── app/
│   ├── __init__.py                # Flask Application Factory & Blueprints
│   ├── extensions.py              # db, login_manager, csrf instances
│   ├── models.py                  # 3NF Database Models
│   ├── forms.py                   # Flask-WTF Forms with validation
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                # Login, Logout, Change Password
│   │   ├── admin.py               # Student CRUD, Subject CRUD, CSV Import
│   │   ├── faculty.py             # Marks Entry and Finalization
│   │   └── student.py             # Student Dashboard and Marksheets
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── decorators.py          # RBAC decorators
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Custom styling and print layout
│   │   └── js/
│   │
│   └── templates/
│       ├── base.html              # Core Bootstrap 5 layout & navbar
│       │
│       ├── auth/
│       │   ├── login.html
│       │   └── change_password.html
│       │
│       ├── admin/
│       │   ├── dashboard.html
│       │   ├── students_list.html
│       │   ├── student_form.html
│       │   ├── subjects_list.html
│       │   ├── subject_form.html
│       │   └── import_csv.html
│       │
│       ├── faculty/
│       │   ├── dashboard.html
│       │   └── mark_entry.html
│       │
│       ├── student/
│       │   └── dashboard.html
│       │
│       └── errors/
│           ├── 403.html
│           ├── 404.html
│           └── 500.html
│
├── instance/
│   └── student_results.db         # SQLite local database
│
├── tests/
│   └── ...
│
├── .env.example
├── .gitignore
├── config.py                      # Development, Testing & Production configs
├── requirements.txt               # Python package dependencies
├── run.py                         # Application local runner
└── seed.py                        # Database schema & sample data seeder
```

---

# 🚀 Prerequisites & Installation

## 1. Prerequisites

Make sure **Python 3.10 or higher** is installed.

Verify the Python installation:

```powershell
python --version
```

Expected output:

```text
Python 3.10.x
```

or a newer version.

---

## 2. Clone or Open the Project

Open **PowerShell** inside the project directory:

```powershell
cd C:\Users\Rims\Code\student-result-management-system
```

---

## 3. Create a Virtual Environment

Create the Python virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

When the virtual environment is active, your PowerShell prompt should contain:

```text
(venv)
```

For example:

```text
(venv) PS C:\Users\Rims\Code\student-result-management-system>
```

---

## 4. PowerShell Execution Policy

If PowerShell prevents the activation script from running, execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Then activate the virtual environment again:

```powershell
.\venv\Scripts\Activate.ps1
```

> **Note:** `-Scope Process` applies the setting only to the current PowerShell session.

---

# 📦 Install Dependencies

Make sure the virtual environment is activated, then run:

```powershell
pip install -r requirements.txt
```

To verify Flask is installed:

```powershell
python -c "import flask; print(flask.__version__)"
```

---

# 🗄️ Database Initialization & Seeding

The project includes an **idempotent `seed.py` script**.

The script:

- Creates the required relational database tables
- Maintains the database structure in **Third Normal Form (3NF)**
- Adds standard BCA curriculum demo records
- Creates default application accounts
- Can safely be executed again without unnecessarily duplicating seed data

Run:

```powershell
python seed.py
```

For local development, the SQLite database is generated at:

```text
instance/student_results.db
```

---

# 🔐 Default Login Accounts

The application provides the following pre-seeded demo accounts.

| Role | Username / Roll No | Default Password | Access |
|---|---|---|---|
| **Admin** | `admin` | `AdminPassword@123` | Student/subject CRUD, CSV import, administration |
| **Faculty** | `faculty` | `FacultyPassword@123` | Marks entry and finalization |
| **Student** | `2350382985` | `StudentPassword@123` | Profile, semester results and marksheet |

> ⚠️ **Security Notice:** These are development/demo credentials. Change all default passwords before deploying the application to a production environment.

---

# ▶️ Running the Application

Start the Flask development server:

```powershell
python run.py
```

The application should start on:

```text
http://127.0.0.1:5000/
```

### Web Portal

Open:

```text
http://127.0.0.1:5000/
```

### Health Check API

Open:

```text
http://127.0.0.1:5000/health
```

The health endpoint can be used to verify that the application is running correctly.

---

# 🔄 Application Workflow

## 1. Admin Verification

Log in using:

```text
Username: admin
Password: AdminPassword@123
```

The Admin can:

1. Add new students.
2. Search existing students.
3. Edit student profiles.
4. Delete student records.
5. Manage curriculum and subjects.
6. Import students in bulk using CSV.
7. Access academic administration features.

### CSV Import Format

The CSV file should contain the following headers:

```csv
roll_no,name,course,semester,dob,email,phone
BCS003,Deepak Verma,BCA,5,2003-05-12,deepak@example.com,9876543212
```

### Required CSV Columns

```text
roll_no
name
course
semester
dob
email
phone
```

---

## 2. Faculty Verification

Log in using:

```text
Username: faculty
Password: FacultyPassword@123
```

Faculty users can:

1. Select a subject from the subject dropdown.
2. Select a student.
3. Enter internal marks.
4. Enter external marks.
5. View the automatically calculated total.
6. View the automatically calculated grade.
7. Save marks as a draft.
8. Finalize marks permanently.

### Marks Validation

| Component | Maximum Marks |
|---|---:|
| Internal | 30 |
| External | 70 |
| **Total** | **100** |

The system validates marks before saving them.

### Draft vs Finalized Marks

**Save as Draft**

- Marks remain editable.
- Faculty can make corrections later.
- Record is not permanently locked.

**Submit & Finalize Marks**

- Marks become permanently finalized.
- The record is locked against unauthorized modification.
- Finalized marks cannot be casually edited through the normal marks-entry workflow.

---

## 3. Student Verification

Log in using:

```text
Username: 2350382985
Password: StudentPassword@123
```

Students can:

- View their personal profile.
- View enrolled academic information.
- View published semester results.
- View individual subject marks.
- Access their marksheet.
- Print the marksheet in an A4-friendly format.

---

# 🧪 Testing

The project uses **Pytest** for automated testing.

Run the test suite with:

```powershell
pytest
```

For more detailed output:

```powershell
pytest -v
```

---

# 🔒 Security Features

The application implements several security mechanisms:

- Role-Based Access Control (RBAC)
- Flask-Login authentication
- Secure password hashing
- PBKDF2-SHA256 password hashing
- CSRF protection using Flask-WTF
- Server-side form validation
- Client-side input validation
- Marks range validation
- Finalized marks locking
- Database-backed user sessions
- HTTP error handling
- Separate Admin, Faculty and Student permissions

---

# 🏗️ Application Architecture

The application follows a structured three-tier architecture:

```text
┌──────────────────────────────────────┐
│           Presentation Layer         │
│ HTML5 + CSS3 + Bootstrap + JS        │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          Application Layer            │
│ Flask Routes + Forms + RBAC + Logic  │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│             Data Layer               │
│ Flask-SQLAlchemy + SQLite/PostgreSQL │
└──────────────────────────────────────┘
```

---

# 🗃️ Database Design

The database is designed using **Third Normal Form (3NF)** principles.

The core entities include:

```text
Users
Students
Subjects
Marks
Results
```

The ORM layer is implemented using:

```text
Flask-SQLAlchemy
SQLAlchemy 2.x
```

### Development Database

```text
SQLite 3
```

Database file:

```text
instance/student_results.db
```

### Production Database

The application can be configured to use:

```text
PostgreSQL
```

for production deployment.

---

# ⚙️ Configuration

The project includes:

```text
config.py
```

for environment-specific configuration.

Supported configuration environments include:

- Development
- Testing
- Production

Environment variables can be maintained using:

```text
.env
```

A sample configuration is provided in:

```text
.env.example
```

> Never commit production passwords, secret keys, database credentials, or other sensitive configuration values to Git.

---

# 🩺 Troubleshooting

## 1. `ModuleNotFoundError: No module named 'flask'`

### Cause

The terminal is using the global Python interpreter instead of the project's virtual environment.

### Solution

Activate the virtual environment:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
```

Then install the dependencies:

```powershell
pip install -r requirements.txt
```

Verify:

```powershell
python -c "import flask; print('Flask installed successfully')"
```

---

## 2. `Activate.ps1 cannot be loaded because running scripts is disabled`

### Cause

Windows PowerShell's execution policy is preventing the virtual environment activation script from running.

### Solution

Run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Missing SQLite Database File

### Cause

The database has not been generated yet.

### Solution

Run:

```powershell
python seed.py
```

The application should create:

```text
instance/student_results.db
```

and populate the required demo records.

---

## 4. Application Does Not Start

First verify that the virtual environment is active:

```powershell
python --version
```

Then verify dependencies:

```powershell
pip install -r requirements.txt
```

Initialize the database:

```powershell
python seed.py
```

Finally start the application:

```powershell
python run.py
```

---

# 📌 Important Commands

### Create virtual environment

```powershell
python -m venv venv
```

### Activate virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Initialize database

```powershell
python seed.py
```

### Run application

```powershell
python run.py
```

### Run tests

```powershell
pytest -v
```

---

# 📄 Project Information

| Field | Details |
|---|---|
| Project Title | Student Result Management System |
| Abbreviation | SRMS |
| University | IGNOU |
| Programme | Bachelor of Computer Applications (BCA) |
| Project Type | Final Year Major Project |
| Course Code | BCSP-064 |
| Student | Prince Kumar |
| Enrolment Number | 2350382985 |
| Study Centre | Maharaja Agrasen College (07107) |
| Session | July 2023 |

---

# 🎯 Project Objectives

The primary objectives of the Student Result Management System are:

- To digitize student result management.
- To reduce manual academic record maintenance.
- To minimize data-entry errors.
- To provide secure role-based access.
- To simplify faculty marks entry.
- To automatically calculate totals and grades.
- To prevent unauthorized modification of finalized marks.
- To provide students with convenient access to academic results.
- To support printable digital marksheets.
- To provide administrators with efficient student and curriculum management.
- To support bulk student data import through CSV.

---

# 🚀 Future Enhancements

Potential future improvements include:

- Email notifications for published results.
- SMS notifications.
- Advanced academic analytics and dashboards.
- Result export to PDF.
- Excel report generation.
- GPA/CGPA calculation.
- Attendance management.
- Multiple academic sessions.
- University-wide deployment.
- PostgreSQL-based production deployment.
- REST API integration.
- Two-factor authentication.
- Advanced audit logging.

---

# 👨‍💻 Author

**Prince Kumar**

Bachelor of Computer Applications (BCA)  
IGNOU  
Course Code: **BCSP-064**  
Session: **July 2023**

---

## 📜 License

This project has been developed as an **IGNOU BCA Final Year Major Project** for academic and educational purposes.
