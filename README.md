# My Portfolio

This is a small Flask portfolio app. It includes:

- `app.py` — Flask application with simple project data and a contact form
- `templates/` — Jinja templates (base, index, projects, contacts, error)
- `static/` — CSS and images

Quick start

1. Create and activate a virtual environment (recommended):
   - python -m venv .venv
   - .\.venv\Scripts\Activate.ps1 (PowerShell)
2. Install dependencies:
   - pip install -r requirements.txt
3. Run the app:
   - python app.py
4. Open http://127.0.0.1:5000/ in your browser

Notes

- Contact form saves messages to `data/contacts.csv`.
- Set `FLASK_SECRET` env var in production for secure sessions.
