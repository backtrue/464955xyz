"""
Credit management system for handling user credits and transactions
"""
from app import db
from models import User, CreditTransaction, SystemSettings
import logging

def record_credit_transaction(user_id, amount, transaction_type, description=None, brief_id=None, proposal_id=None):
    """
    Record a credit transaction and update user balance
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
        
        # Create transaction record
        transaction = CreditTransaction(
            user_id=user_id,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            related_brief_id=brief_id,
            related_proposal_id=proposal_id
        )
        
        # Update user credits
        user.credits += amount
        
        db.session.add(transaction)
        db.session.commit()
        
        logging.info(f"Credit transaction recorded: {amount} credits for user {user_id}, type: {transaction_type}")
        return True, "Transaction recorded successfully"
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error recording credit transaction: {e}")
        return False, str(e)

def deduct_credit_for_brief(user_id, brief_id):
    """
    Deduct 1 credit for creating a brief
    """
    return record_credit_transaction(
        user_id=user_id,
        amount=-1,
        transaction_type='brief_creation',
        description='Credit deducted for creating a brief',
        brief_id=brief_id
    )

def deduct_credit_for_proposal(user_id, proposal_id, brief_id):
    """
    Deduct 1 credit for submitting a proposal
    """
    return record_credit_transaction(
        user_id=user_id,
        amount=-1,
        transaction_type='proposal_submission',
        description='Credit deducted for submitting a proposal',
        brief_id=brief_id,
        proposal_id=proposal_id
    )

def grant_registration_bonus(user_id):
    """
    Grant registration bonus credits to new user
    """
    bonus_amount = int(SystemSettings.get_setting('registration_bonus_credits', '5'))
    
    if bonus_amount > 0:
        return record_credit_transaction(
            user_id=user_id,
            amount=bonus_amount,
            transaction_type='registration_bonus',
            description=f'Registration bonus: {bonus_amount} credits'
        )
    return True, "No registration bonus configured"

def admin_adjust_credits(user_id, amount, description="Admin credit adjustment"):
    """
    Admin function to manually adjust user credits
    """
    return record_credit_transaction(
        user_id=user_id,
        amount=amount,
        transaction_type='admin_adjustment',
        description=description
    )

def get_registration_bonus_credits():
    """
    Get current registration bonus amount
    """
    return int(SystemSettings.get_setting('registration_bonus_credits', '5'))

def set_registration_bonus_credits(amount):
    """
    Set registration bonus amount
    """
    SystemSettings.set_setting(
        'registration_bonus_credits', 
        amount, 
        f'Number of credits given to new users upon registration'
    )
    db.session.commit()

def initialize_credit_settings():
    """
    Initialize default credit system settings
    """
    try:
        # Set default registration bonus if not exists
        if not SystemSettings.query.filter_by(setting_key='registration_bonus_credits').first():
            SystemSettings.set_setting('registration_bonus_credits', '5', 'Default credits for new registrations')
            db.session.commit()
            logging.info("Initialized default credit settings")
    except Exception as e:
        logging.error(f"Error initializing credit settings: {e}")
        db.session.rollback()