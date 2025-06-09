from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user

def superadmin_required(f):
    """Decorator to require superadmin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        
        if not current_user.is_superadmin():
            flash('Access denied. Superadmin privileges required.', 'error')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def get_user_stats():
    """Get user statistics for admin dashboard"""
    from models import User, Brief, Proposal
    
    total_users = User.query.count()
    total_clients = User.query.filter_by(role='client').count()
    total_professionals = User.query.filter_by(role='pro').count()
    total_briefs = Brief.query.count()
    total_proposals = Proposal.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_briefs = Brief.query.order_by(Brief.created_at.desc()).limit(5).all()
    
    return {
        'total_users': total_users,
        'total_clients': total_clients,
        'total_professionals': total_professionals,
        'total_briefs': total_briefs,
        'total_proposals': total_proposals,
        'recent_users': recent_users,
        'recent_briefs': recent_briefs
    }