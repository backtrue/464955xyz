from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum('client', 'pro', 'superadmin', name='user_roles'), nullable=False)
    company_name = db.Column(db.String(255), nullable=True)
    full_name = db.Column(db.String(255), nullable=True)
    credits = db.Column(db.Integer, default=0, nullable=False)
    profile_slug = db.Column(db.String(50), unique=True, nullable=True)  # Custom URL slug for professionals
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verification_token = db.Column(db.String(100), nullable=True)
    email_verification_sent_at = db.Column(db.DateTime, nullable=True)
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
    
    def is_superadmin(self):
        """Check if user is superadmin"""
        return self.role == 'superadmin'
    
    def has_credits(self, amount=1):
        """Check if user has enough credits"""
        return self.credits >= amount
    
    def deduct_credits(self, amount=1):
        """Deduct credits from user account"""
        if self.has_credits(amount):
            self.credits -= amount
            return True
        return False
    
    def add_credits(self, amount):
        """Add credits to user account"""
        self.credits += amount
    
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

class SystemSettings(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get_setting(key, default_value="0"):
        """Get a system setting value"""
        setting = SystemSettings.query.filter_by(setting_key=key).first()
        return setting.setting_value if setting else default_value
    
    @staticmethod
    def set_setting(key, value, description=None):
        """Set or update a system setting"""
        setting = SystemSettings.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = str(value)
            setting.updated_at = datetime.utcnow()
            if description:
                setting.description = description
        else:
            setting = SystemSettings(
                setting_key=key,
                setting_value=str(value),
                description=description
            )
            db.session.add(setting)
        return setting

class CreditTransaction(db.Model):
    __tablename__ = 'credit_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)  # Positive for credit, negative for debit
    transaction_type = db.Column(db.Enum('registration_bonus', 'brief_creation', 'proposal_submission', 'admin_adjustment', name='transaction_types'), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    related_brief_id = db.Column(db.Integer, db.ForeignKey('briefs.id'), nullable=True)
    related_proposal_id = db.Column(db.Integer, db.ForeignKey('proposals.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='credit_transactions')
    brief = db.relationship('Brief', backref='credit_transactions')
    proposal = db.relationship('Proposal', backref='credit_transactions')
    
    def __repr__(self):
        return f'<CreditTransaction {self.id}: {self.amount} credits for user {self.user_id}>'

class ProfessionalSkill(db.Model):
    __tablename__ = 'professional_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.Enum('meta_ads', 'google_ads', 'seo', name='skill_categories'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency_level = db.Column(db.Integer, nullable=False, default=1)  # 1-5 scale
    notes = db.Column(db.Text, nullable=True)
    portfolio_link = db.Column(db.String(500), nullable=True)
    display_order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='professional_skills')
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('proficiency_level >= 1 AND proficiency_level <= 5', name='check_proficiency_level'),
    )
    
    def __repr__(self):
        return f'<ProfessionalSkill {self.skill_name} ({self.category}) - Level {self.proficiency_level}>'
