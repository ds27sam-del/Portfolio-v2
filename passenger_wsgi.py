# passenger_wsgi.py
# For hosts that expect Passenger (cPanel / CloudLinux). This file imports the
# robust importer implemented in `wsgi.py`, so Passenger-based hosts benefit
# from the same fallback and logging behavior.
import os
import sys

project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

parent = os.path.dirname(project_home)
if parent not in sys.path:
    sys.path.insert(0, parent)

# Import the application from the central WSGI entrypoint
from wsgi import application
