"""
Script to update existing briefs with extracted target audience and marketing goals
"""
from app import app, db
from models import Brief
from brief_parser import parse_structured_brief
import logging

def update_existing_briefs():
    """
    Update all existing briefs to extract target audience and marketing goals
    from their structured brief content
    """
    with app.app_context():
        # Get all briefs that have structured_brief but missing target_audience or marketing_goals
        briefs_to_update = Brief.query.filter(
            Brief.structured_brief.isnot(None),
            Brief.structured_brief != ''
        ).filter(
            (Brief.target_audience.is_(None)) | 
            (Brief.marketing_goals.is_(None)) |
            (Brief.target_audience == '') |
            (Brief.marketing_goals == '')
        ).all()
        
        print(f"Found {len(briefs_to_update)} briefs to update")
        
        updated_count = 0
        for brief in briefs_to_update:
            try:
                parsed_data = parse_structured_brief(brief.structured_brief)
                
                updated = False
                if parsed_data['target_audience'] and not brief.target_audience:
                    brief.target_audience = parsed_data['target_audience']
                    updated = True
                    print(f"Brief {brief.id}: Updated target audience")
                
                if parsed_data['marketing_goals'] and not brief.marketing_goals:
                    brief.marketing_goals = parsed_data['marketing_goals']
                    updated = True
                    print(f"Brief {brief.id}: Updated marketing goals")
                
                if updated:
                    db.session.commit()
                    updated_count += 1
                    
            except Exception as e:
                print(f"Error updating brief {brief.id}: {e}")
                db.session.rollback()
        
        print(f"Successfully updated {updated_count} briefs")

if __name__ == "__main__":
    update_existing_briefs()