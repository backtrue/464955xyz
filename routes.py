from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import app, db
from models import User, Brief, Proposal
from brief_generator import generate_brief_from_input
from openai_helper import generate_structured_brief
from admin_utils import superadmin_required, get_user_stats
from brief_parser import parse_structured_brief
from i18n import _, get_current_language, get_languages
import logging

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html', _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/set_language/<language>')
def set_language(language):
    """Set language and redirect back"""
    if language in app.config['LANGUAGES']:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', '')
        full_name = request.form.get('full_name', '').strip()
        company_name = request.form.get('company_name', '').strip()
        
        # Validation
        if not email or not password or not role or not full_name:
            flash('All fields are required.', 'error')
            return render_template('register.html', _=_, get_languages=get_languages, current_lang=get_current_language())
        
        if role not in ['client', 'pro']:
            flash('Invalid role selected.', 'error')
            return render_template('register.html', _=_, get_languages=get_languages, current_lang=get_current_language())
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html', _=_, get_languages=get_languages, current_lang=get_current_language())
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already registered.', 'error')
            return render_template('register.html', _=_, get_languages=get_languages, current_lang=get_current_language())
        
        # Create new user
        try:
            user = User()
            user.email = email
            user.role = role
            user.full_name = full_name
            user.company_name = company_name if company_name else None
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Registration error: {e}")
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html', _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            
            # Redirect based on user role
            if user.role == 'client':
                return redirect(url_for('client_dashboard'))
            else:
                return redirect(url_for('pro_dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html', _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/client/dashboard')
@login_required
def client_dashboard():
    """Client dashboard"""
    if current_user.role != 'client':
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    
    # Get user's briefs with proposal counts
    briefs = db.session.query(Brief).filter_by(user_id=current_user.id).order_by(Brief.created_at.desc()).all()
    
    # Add proposal count to each brief
    for brief in briefs:
        brief.proposal_count = len(brief.proposals)
    
    return render_template('client_dashboard.html', briefs=briefs, _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/pro/dashboard')
@login_required
def pro_dashboard():
    """Professional dashboard"""
    if current_user.role != 'pro':
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    
    # Get active briefs (not submitted by this user)
    active_briefs = Brief.query.filter(
        Brief.status == 'active',
        Brief.user_id != current_user.id
    ).order_by(Brief.created_at.desc()).all()
    
    # Get user's proposals
    my_proposals = Proposal.query.filter_by(user_id=current_user.id).order_by(Proposal.created_at.desc()).all()
    
    return render_template('pro_dashboard.html', active_briefs=active_briefs, my_proposals=my_proposals, _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/client/create-brief', methods=['GET', 'POST'])
@login_required
def create_brief():
    """Create a new brief"""
    if current_user.role != 'client':
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        raw_input = request.form.get('raw_input', '').strip()
        service_type = request.form.get('service_type', '').strip()
        
        if not raw_input:
            flash('Please describe your marketing needs.', 'error')
            return render_template('create_brief.html', _=_, get_languages=get_languages, current_lang=get_current_language())
        
        if not service_type:
            flash('Please select a service type.', 'error')
            return render_template('create_brief.html', _=_, get_languages=get_languages, current_lang=get_current_language())
            
        if len(raw_input) < 50:
            flash('Please provide more detailed information (at least 50 characters).', 'error')
            return render_template('create_brief.html', _=_, get_languages=get_languages, current_lang=get_current_language())
        
        try:
            # Get structured brief if provided (from AI generation)
            structured_brief = request.form.get('structured_brief', '').strip()
            
            # Get follow-up question answers
            materials_provider = request.form.get('materials_provider')
            copywriting_provider = request.form.get('copywriting_provider')
            communication_frequency = request.form.get('communication_frequency')
            
            # Generate structured brief from natural language input (fallback)
            brief_data = generate_brief_from_input(raw_input)
            
            # Create new brief
            brief = Brief(
                user_id=current_user.id,
                raw_input=raw_input,
                structured_brief=structured_brief if structured_brief else None,
                service_type=service_type,
                title=brief_data['title'],
                description=brief_data['description'],
                platform_preference=brief_data['platform_preference'],
                budget_min=brief_data['budget_min'],
                budget_max=brief_data['budget_max'],
                suggested_items=brief_data['suggested_items'],
                duration_weeks=brief_data['duration_weeks'],
                marketing_goals=brief_data['marketing_goals'],
                target_audience=brief_data['target_audience'],
                materials_provider=materials_provider,
                copywriting_provider=copywriting_provider,
                communication_frequency=communication_frequency
            )
            
            db.session.add(brief)
            db.session.commit()
            
            flash('Brief created successfully!', 'success')
            return redirect(url_for('view_brief', brief_id=brief.id))
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Brief creation error: {e}")
            flash('Failed to create brief. Please try again.', 'error')
    
    return render_template('create_brief.html', _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/brief/<int:brief_id>')
@login_required
def view_brief(brief_id):
    """View a specific brief"""
    brief = Brief.query.get_or_404(brief_id)
    
    # Check access permissions
    can_view = (current_user.role == 'client' and brief.user_id == current_user.id) or \
               (current_user.role == 'pro')
    
    if not can_view:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    
    # Get proposals if user is the brief owner
    proposals = []
    if current_user.role == 'client' and brief.user_id == current_user.id:
        proposals = Proposal.query.filter_by(brief_id=brief_id).order_by(Proposal.created_at.desc()).all()
    
    # Parse structured brief to extract target audience and marketing goals
    if brief.structured_brief:
        parsed_data = parse_structured_brief(brief.structured_brief)
        if parsed_data['target_audience'] and not brief.target_audience:
            brief.target_audience = parsed_data['target_audience']
            db.session.commit()
        if parsed_data['marketing_goals'] and not brief.marketing_goals:
            brief.marketing_goals = parsed_data['marketing_goals']
            db.session.commit()
    
    return render_template('view_brief.html', brief=brief, proposals=proposals, _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/brief/<int:brief_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_brief(brief_id):
    """Edit a brief (only by the owner)"""
    brief = Brief.query.get_or_404(brief_id)
    
    # Check if current user is the owner
    if brief.user_id != current_user.id:
        flash('You can only edit your own briefs.', 'error')
        return redirect(url_for('view_brief', brief_id=brief_id))
    
    # Check if brief is still editable (no accepted proposals)
    accepted_proposals = [p for p in brief.proposals if p.status == 'accepted']
    if accepted_proposals:
        flash('Cannot edit brief with accepted proposals.', 'error')
        return redirect(url_for('view_brief', brief_id=brief_id))
    
    if request.method == 'POST':
        # Update brief fields
        brief.title = request.form.get('title', '').strip()
        brief.description = request.form.get('description', '').strip()
        brief.service_type = request.form.get('service_type')
        
        # Optional fields
        budget_min = request.form.get('budget_min')
        budget_max = request.form.get('budget_max')
        brief.budget_min = int(budget_min) if budget_min and budget_min.isdigit() else None
        brief.budget_max = int(budget_max) if budget_max and budget_max.isdigit() else None
        
        duration = request.form.get('duration_weeks')
        brief.duration_weeks = int(duration) if duration and duration.isdigit() else None
        
        brief.platform_preference = request.form.get('platform_preference', '').strip() or None
        brief.marketing_goals = request.form.get('marketing_goals', '').strip() or None
        brief.target_audience = request.form.get('target_audience', '').strip() or None
        
        # Additional collaboration fields
        brief.materials_provider = request.form.get('materials_provider') or None
        brief.copywriting_provider = request.form.get('copywriting_provider') or None
        brief.communication_frequency = request.form.get('communication_frequency') or None
        
        # Validation
        if not brief.title or not brief.description or not brief.service_type:
            flash('Title, description, and service type are required.', 'error')
            return render_template('edit_brief.html', brief=brief, _=_, get_languages=get_languages, current_lang=get_current_language())
        
        try:
            db.session.commit()
            flash('Brief updated successfully!', 'success')
            return redirect(url_for('view_brief', brief_id=brief_id))
        except Exception as e:
            db.session.rollback()
            flash('Error updating brief. Please try again.', 'error')
            logging.error(f"Error updating brief: {e}")
    
    return render_template('edit_brief.html', brief=brief, _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/brief/<int:brief_id>/propose', methods=['GET', 'POST'])
@login_required
def submit_proposal(brief_id):
    """Submit a proposal for a brief"""
    if current_user.role != 'pro':
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    
    brief = Brief.query.get_or_404(brief_id)
    
    # Check if brief is active and not own brief
    if brief.status != 'active' or brief.user_id == current_user.id:
        flash('Cannot submit proposal for this brief.', 'error')
        return redirect(url_for('pro_dashboard'))
    
    # Check if already submitted proposal
    existing_proposal = Proposal.query.filter_by(brief_id=brief_id, user_id=current_user.id).first()
    if existing_proposal:
        flash('You have already submitted a proposal for this brief.', 'error')
        return redirect(url_for('view_brief', brief_id=brief_id))
    
    if request.method == 'POST':
        price = request.form.get('price', '')
        message = request.form.get('message', '').strip()
        sample_links = request.form.get('sample_links', '').strip()
        estimated_days = request.form.get('estimated_days', '')
        
        # Validation
        if not price or not message or not estimated_days:
            flash('Price, message, and estimated days are required.', 'error')
            return render_template('submit_proposal.html', brief=brief, _=_, get_languages=get_languages, current_lang=get_current_language())
        
        try:
            price = int(price)
            estimated_days = int(estimated_days)
            
            if price <= 0 or estimated_days <= 0:
                raise ValueError("Price and estimated days must be positive")
                
        except ValueError:
            flash('Please enter valid numbers for price and estimated days.', 'error')
            return render_template('submit_proposal.html', brief=brief, _=_, get_languages=get_languages, current_lang=get_current_language())
        
        if len(message) < 100:
            flash('Please provide a more detailed proposal (at least 100 characters).', 'error')
            return render_template('submit_proposal.html', brief=brief, _=_, get_languages=get_languages, current_lang=get_current_language())
        
        try:
            # Create proposal
            proposal = Proposal(
                brief_id=brief_id,
                user_id=current_user.id,
                price=price,
                message=message,
                sample_links=sample_links if sample_links else None,
                estimated_days=estimated_days
            )
            
            db.session.add(proposal)
            db.session.commit()
            
            flash('Proposal submitted successfully!', 'success')
            return redirect(url_for('view_brief', brief_id=brief_id))
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Proposal submission error: {e}")
            flash('Failed to submit proposal. Please try again.', 'error')
    
    return render_template('submit_proposal.html', brief=brief, _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/client/proposals/<int:brief_id>')
@login_required
def view_proposals(brief_id):
    """View proposals for a brief"""
    if current_user.role != 'client':
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    
    brief = Brief.query.get_or_404(brief_id)
    
    # Check if user owns this brief
    if brief.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('client_dashboard'))
    
    proposals = Proposal.query.filter_by(brief_id=brief_id).order_by(Proposal.created_at.desc()).all()
    
    return render_template('view_proposals.html', brief=brief, proposals=proposals, _=_, get_languages=get_languages, current_lang=get_current_language())

# API Routes
@app.route('/api/generate-brief', methods=['POST'])
@login_required
def api_generate_brief():
    """API endpoint to generate structured brief using OpenAI"""
    try:
        data = request.get_json()
        raw_input = data.get('raw_input', '').strip()
        service_type = data.get('service_type', '')
        
        if not raw_input or len(raw_input) < 50:
            return jsonify({
                'success': False,
                'error': '請提供至少 50 個字符的詳細行銷需求'
            }), 400
            
        if service_type not in ['meta_ads', 'google_ads', 'seo']:
            return jsonify({
                'success': False,
                'error': '請選擇有效的服務類型'
            }), 400
        
        # Generate structured brief using OpenAI
        structured_brief = generate_structured_brief(raw_input, service_type)
        
        # Parse structured brief to extract target audience and marketing goals
        parsed_data = parse_structured_brief(structured_brief)
        
        return jsonify({
            'success': True,
            'structured_brief': structured_brief,
            'target_audience': parsed_data['target_audience'],
            'marketing_goals': parsed_data['marketing_goals']
        })
        
    except Exception as e:
        logging.error(f"Error generating structured brief: {e}")
        return jsonify({
            'success': False,
            'error': f'生成失敗: {str(e)}'
        }), 500

# Admin Routes
@app.route('/admin')
@superadmin_required
def admin_dashboard():
    """Admin dashboard with statistics and overview"""
    stats = get_user_stats()
    return render_template('admin/dashboard.html', stats=stats, _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/admin/users')
@superadmin_required
def admin_users():
    """Manage all users"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    role_filter = request.args.get('role', '', type=str)
    
    query = User.query
    
    if search:
        query = query.filter(User.email.ilike(f'%{search}%') | User.full_name.ilike(f'%{search}%'))
    
    if role_filter:
        query = query.filter_by(role=role_filter)
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', users=users, search=search, role_filter=role_filter, _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/admin/users/<int:user_id>')
@superadmin_required
def admin_user_detail(user_id):
    """View user details"""
    user = User.query.get_or_404(user_id)
    user_briefs = Brief.query.filter_by(user_id=user_id).order_by(Brief.created_at.desc()).all()
    user_proposals = Proposal.query.filter_by(user_id=user_id).order_by(Proposal.created_at.desc()).all()
    
    return render_template('admin/user_detail.html', user=user, user_briefs=user_briefs, user_proposals=user_proposals, _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/admin/users/<int:user_id>/toggle-role', methods=['POST'])
@superadmin_required
def admin_toggle_user_role(user_id):
    """Toggle user role between client and pro"""
    user = User.query.get_or_404(user_id)
    
    if user.role == 'client':
        user.role = 'pro'
        flash(f'User {user.email} changed to Professional', 'success')
    elif user.role == 'pro':
        user.role = 'client'
        flash(f'User {user.email} changed to Client', 'success')
    else:
        flash('Cannot change superadmin role', 'error')
        return redirect(url_for('admin_user_detail', user_id=user_id))
    
    db.session.commit()
    return redirect(url_for('admin_user_detail', user_id=user_id))

@app.route('/admin/briefs')
@superadmin_required
def admin_briefs():
    """Manage all briefs"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    status_filter = request.args.get('status', '', type=str)
    service_filter = request.args.get('service', '', type=str)
    
    query = Brief.query
    
    if search:
        query = query.filter(Brief.title.ilike(f'%{search}%') | Brief.description.ilike(f'%{search}%'))
    
    if status_filter:
        query = query.filter_by(status=status_filter)
        
    if service_filter:
        query = query.filter_by(service_type=service_filter)
    
    briefs = query.order_by(Brief.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/briefs.html', briefs=briefs, search=search, status_filter=status_filter, service_filter=service_filter, _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/admin/briefs/<int:brief_id>')
@superadmin_required
def admin_brief_detail(brief_id):
    """View brief details"""
    brief = Brief.query.get_or_404(brief_id)
    proposals = Proposal.query.filter_by(brief_id=brief_id).order_by(Proposal.created_at.desc()).all()
    
    return render_template('admin/brief_detail.html', brief=brief, proposals=proposals, _=_, get_languages=get_languages, current_lang=get_current_language())

@app.route('/admin/briefs/<int:brief_id>/close', methods=['POST'])
@superadmin_required
def admin_close_brief(brief_id):
    """Close a brief"""
    brief = Brief.query.get_or_404(brief_id)
    brief.status = 'closed'
    db.session.commit()
    flash(f'Brief "{brief.title}" has been closed', 'success')
    return redirect(url_for('admin_brief_detail', brief_id=brief_id))

@app.route('/admin/briefs/<int:brief_id>/reopen', methods=['POST'])
@superadmin_required
def admin_reopen_brief(brief_id):
    """Reopen a brief"""
    brief = Brief.query.get_or_404(brief_id)
    brief.status = 'active'
    db.session.commit()
    flash(f'Brief "{brief.title}" has been reopened', 'success')
    return redirect(url_for('admin_brief_detail', brief_id=brief_id))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
