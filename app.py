import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret-change-me')

# Simple in-memory project data — replace with real data or a DB as needed
# Images for projects are expected to live under "static/images/" — update these filenames or replace with a DB later.
PROJECTS = [
    { 
        'id': 1, 
        'title': 'Medical Data Management 2.0', 
        'description': 'Advanced system for patient record persistence using binary I/O and Python visualization for healthcare metrics.', 
        'image': 'images/medical.png', 
        'url': 'https://github.com/ds27sam-del/Medical-Database-System' 
    },
    { 
        'id': 2, 
        'title': 'Intelligent Task Manager', 
        'description': 'A robust productivity suite utilizing Flask and Tkinter for real-time task tracking and academic organization.', 
        'image': 'images/task.png', 
        'url': 'https://github.com/ds27sam-del/Task-Management' 
    },
    { 
        'id': 3, 
        'title': 'Sales & Inventory Architect', 
        'description': 'Business logic engine for automated revenue reporting, inventory tracking, and dynamic data representation.', 
        'image': 'images/sales.svg', 
        'url': 'https://github.com/ds27sam-del/Sales-Database-System' 
    },
    { 
        'id': 4, 
        'title': 'College Academic System', 
        'description': 'Centralized institutional database managing multi-departmental records with secure authentication protocols.', 
        'image': 'images/college.png', 
        'url': 'https://github.com/ds27sam-del/College-Database-System' 
    },
    { 
        'id': 5, 
        'title': 'C++ Algorithm Engine', 
        'description': 'A master repository of N-ary tree structures, pointer arithmetic, and cross-language arithmetic logic.', 
        'image': 'images/cpp.png', 
        'url': 'https://github.com/ds27sam-del/database-system-in-cpp' 
    },
    { 
        'id': 6, 
        'title': 'Core CS Fundamentals', 
        'description': 'Comprehensive logic implementations covering recursion, bitwise operations, and memory-efficient data swapping.', 
        'image': 'images/basics.png', 
        'url': 'https://github.com/ds27sam-del/struct-in-c' 
    },
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

@app.route('/Tech')
def tech():
    return render_template('Tech.html', active='Why Technology')

@app.route('/Story')
@app.route('/story')
def story():
    return render_template('story.html', active='Story')

@app.route('/Experience.html')
@app.route('/experience')
def Experience():
    return render_template('Experience.html', active='Experience')

@app.route('/Thoughts')
@app.route('/thoughts')
def Thoughts():
    return render_template('Thoughts.html', active='Thoughts')

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
