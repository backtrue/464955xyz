from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum('client', 'pro', name='user_roles'), nullable=False)
    company_name = db.Column(db.String(255), nullable=True)
    full_name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    briefs = db.relationship('Brief', backref='client', lazy=True)
    proposals = db.relationship('Proposal', backref='professional', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Brief(db.Model):
    __tablename__ = 'briefs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    raw_input = db.Column(db.Text, nullable=False)  # Original natural language input
    structured_brief = db.Column(db.Text, nullable=True)  # AI-generated structured brief
    service_type = db.Column(db.Enum('meta_ads', 'google_ads', 'seo', name='service_types'), nullable=False)
    platform_preference = db.Column(db.String(255), nullable=True)
    budget_min = db.Column(db.Integer, nullable=True)
    budget_max = db.Column(db.Integer, nullable=True)
    suggested_items = db.Column(db.Text, nullable=True)
    duration_weeks = db.Column(db.Integer, nullable=True)
    marketing_goals = db.Column(db.Text, nullable=True)
    target_audience = db.Column(db.String(500), nullable=True)
    # Follow-up question answers
    materials_provider = db.Column(db.Enum('client', 'agency', 'collaboration', name='materials_provider_types'), nullable=True)
    copywriting_provider = db.Column(db.Enum('client', 'agency', 'collaboration', name='copywriting_provider_types'), nullable=True)
    communication_frequency = db.Column(db.Enum('weekly', 'monthly', 'milestones', 'async', name='communication_frequency_types'), nullable=True)
    status = db.Column(db.Enum('active', 'closed', 'in_progress', name='brief_status'), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    proposals = db.relationship('Proposal', backref='brief', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Brief {self.title}>'

class Proposal(db.Model):
    __tablename__ = 'proposals'
    
    id = db.Column(db.Integer, primary_key=True)
    brief_id = db.Column(db.Integer, db.ForeignKey('briefs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    sample_links = db.Column(db.Text, nullable=True)
    estimated_days = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected', name='proposal_status'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Proposal {self.id} for Brief {self.brief_id}>'
