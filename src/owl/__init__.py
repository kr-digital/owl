# Start owl core
from owl.storage.core import Core
core = Core()

# Start flask app
from flask import Flask
app = Flask(__name__)

# Flask debug mode
from werkzeug.debug import DebuggedApplication
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
app.debug = True

# Load flask views
from owl.storage import views
from owl.api import views