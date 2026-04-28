import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret-change-me')

# Simple in-memory project data — replace with real data or a DB as needed
# Images for projects are expected to live under "static/images/" — update these filenames or replace with a DB later.
PROJECTS = [
    { 'id': 1, 'title': 'Medical Data Analysis 2.0', 'description': 'A Python application for managing patient records with integrated data visualization using Matplotlib.', 'image': 'images/1.png', 'url': 'https://github.com/ds27sam-del/Medical-Data-Management-And-Analysis-2.0' },
    { 'id': 2, 'title': 'Student Task Manager 2.0', 'description': 'A comprehensive productivity tool featuring a GUI for students to organize assignments and track academic progress.', 'image': 'images/2.png', 'url': 'https://github.com/ds27sam-del/Student_Task_Manager-2.0' },
    { 'id': 3, 'title': 'Sales Management System', 'description': 'A business-focused system designed for efficient inventory tracking and automated revenue graph generation.', 'image': 'images/3.svg', 'url': 'https://github.com/ds27sam-del/Sales-Data-Management-System-2.0' },
    { 'id': 4, 'title': 'College Management System', 'description': 'A centralized database solution for managing student enrollment and departmental academic records.', 'image': 'images/4.png', 'url': 'https://github.com/ds27sam-del/College-Data-Management-System' },
    { 'id': 5, 'title': 'CPP Logic & Algorithms', 'description': 'A collection of core programming challenges and algorithms demonstrating fundamental C++ proficiency.', 'image': 'images/5.png', 'url': 'https://github.com/ds27sam-del/CPP-Logic-and-Algorithms' },
    { 'id': 6, 'title': 'Library Management System', 'description': 'A secure Python application designed to manage book inventories and user borrowing records effectively.', 'image': 'images/6.png', 'url': 'https://github.com/ds27sam-del/Projects' },
]

# Path where contact messages are stored
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
CONTACTS_FILE = os.path.join(DATA_DIR, 'contacts.csv')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

@app.context_processor
def inject_year():
    return { 'current_year': datetime.utcnow().year }

@app.route('/')
@app.route('/')
def index():
    return render_template('index.html', active='home')

# Add this inside your app.py file
@app.route('/journey')
def journey():
    return render_template('journey.html', active='journey')

@app.route('/projects')
def projects():
    # And passing your projects data here!
    return render_template('projects.html', active='projects')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash('Please fill all fields before submitting.', 'error')
            return redirect(url_for('contacts'))

        # Append to CSV file
        write_header = not os.path.exists(CONTACTS_FILE)
        try:
            with open(CONTACTS_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if write_header:
                    writer.writerow(['timestamp', 'name', 'email', 'message'])
                writer.writerow([datetime.utcnow().isoformat(), name, email, message])
            flash('Thanks! Your message has been received.', 'success')
        except Exception as e:
            app.logger.exception('Failed to save contact message')
            flash('Sorry — could not save your message. Try again later.', 'error')

        return redirect(url_for('contacts'))

    return render_template('contacts.html', active='contacts')

# Simple error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', code=404, message='Page not found'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', code=500, message='Server error'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
