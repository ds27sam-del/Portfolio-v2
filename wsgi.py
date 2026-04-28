"""
Robust WSGI entrypoint for hosting providers.
This file exposes a WSGI callable named `application` that most servers expect.
It attempts multiple import strategies and writes an import traceback to
`wsgi-import-error.log` in the project root if it fails so that file-based
hosting logs are easier to diagnose.
"""
import os
import sys
import traceback

# Ensure the project directory (and its parent) are on sys.path so imports work
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

parent = os.path.dirname(project_home)
if parent not in sys.path:
    sys.path.insert(0, parent)


def _import_app():
    """Try several common module/attribute names to find the Flask app."""
    candidates = [
        ("app", "app"),
        ("app", "application"),
        ("main", "app"),
        ("main", "application"),
        ("application", "application"),
    ]
    for module_name, attr in candidates:
        try:
            module = __import__(module_name)
            app = getattr(module, attr)
            return app
        except Exception:
            continue

    # Try scanning project files as a last resort
    for fname in os.listdir(project_home):
        if fname.endswith('.py') and fname not in ('wsgi.py', 'passenger_wsgi.py'):
            mod = fname[:-3]
            try:
                module = __import__(mod)
                for attr in ("app", "application"):
                    if hasattr(module, attr):
                        return getattr(module, attr)
            except Exception:
                continue

    raise RuntimeError(
        "Could not find Flask WSGI application. Ensure your app defines `app` or `application` in a top-level module."
    )


try:
    application = _import_app()
except Exception:
    tb = traceback.format_exc()
    try:
        log_path = os.path.join(project_home, 'wsgi-import-error.log')
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(tb)
    except Exception:
        # If logging to a file fails, ensure the original exception still bubbles up
        pass
    raise
