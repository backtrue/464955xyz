import os
import logging
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure internationalization
app.config['LANGUAGES'] = {
    'en': 'English',
    'zh': '繁體中文',
    'ja': '日本語'
}

def get_current_language():
    # 1. Check if language is set in session
    if 'language' in session:
        return session['language']
    
    # 2. Check if language is in URL parameters
    if request.args.get('lang'):
        session['language'] = request.args.get('lang')
        return session['language']
    
    # 3. Use browser's preferred language
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'en'

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    import models  # noqa: F401
    db.create_all()
    logging.info("Database tables created")
