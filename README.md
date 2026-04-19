# Resume Matching Engine - Django Web App

A Django-based Resume Matching Engine with an interactive bluish-purple UI, animated charts, circular role fit indicators, SQLite database support, and an ML-based role recommendation flow.

## Features
- Upload candidate resumes in PDF, DOCX, or TXT format
- Extract resume text automatically
- Predict **Top 3 best-fit roles** using a trained ML pipeline
- Show role-fit percentages in animated circular cards
- Store candidates and predictions in SQLite database
- Admin panel support
- Dashboard with moving charts and role analytics
- Bluish-purple modern UI with glow effects

## Roles Covered
- Data Analytics Intern
- Web Development Intern
- Graphic Design Intern
- Digital Marketing Intern
- HR/Operations Intern

## Quick Start
```bash
python -m venv venv
venv\Scriptsctivate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

Admin login:
```bash
python manage.py createsuperuser
```

## Important
This project is designed to run cleanly with SQLite by default. The ML model is trained from a built-in sample training dataset and saved automatically on first prediction or when demo data is seeded.
