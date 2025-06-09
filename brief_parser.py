"""
Parse structured brief content to extract specific information
"""
import re

def parse_structured_brief(structured_brief_text):
    """
    Parse structured brief to extract target audience and marketing goals
    """
    if not structured_brief_text:
        return {
            'target_audience': None,
            'marketing_goals': None
        }
    
    # Initialize results
    target_audience = None
    marketing_goals = None
    
    # Split text into lines for parsing
    lines = structured_brief_text.split('\n')
    current_section = None
    section_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for section headers
        if '【目標族群】' in line or '【目標受眾】' in line or '【Target Audience】' in line:
            # Save previous section if it was marketing goals
            if current_section == 'marketing_goals' and section_content:
                marketing_goals = '\n'.join(section_content).strip()
            
            current_section = 'target_audience'
            section_content = []
            # Extract content after the header on the same line
            content_after_header = line.split('】', 1)
            if len(content_after_header) > 1 and content_after_header[1].strip():
                section_content.append(content_after_header[1].strip())
                
        elif '【專案概要】' in line or '【需求項目】' in line or '【行銷目標】' in line or '【Marketing Goals】' in line or '【Project Overview】' in line:
            # Save previous section if it was target audience
            if current_section == 'target_audience' and section_content:
                target_audience = '\n'.join(section_content).strip()
            
            current_section = 'marketing_goals'
            section_content = []
            # Extract content after the header on the same line
            content_after_header = line.split('】', 1)
            if len(content_after_header) > 1 and content_after_header[1].strip():
                section_content.append(content_after_header[1].strip())
                
        elif current_section and line and not line.startswith('【'):
            # Add content to current section
            section_content.append(line)
            
        # Stop collecting if we hit another major section
        elif line.startswith('【') and current_section:
            if current_section == 'target_audience' and section_content:
                target_audience = '\n'.join(section_content).strip()
            elif current_section == 'marketing_goals' and section_content:
                marketing_goals = '\n'.join(section_content).strip()
            current_section = None
            section_content = []
    
    # Handle the last section
    if current_section == 'target_audience' and section_content:
        target_audience = '\n'.join(section_content).strip()
    elif current_section == 'marketing_goals' and section_content:
        marketing_goals = '\n'.join(section_content).strip()
    
    # Alternative parsing for different formats
    if not target_audience:
        # Try regex patterns for target audience
        patterns = [
            r'【目標族群】\s*([^【]*)',
            r'【目標受眾】\s*([^【]*)',
            r'【Target Audience】\s*([^【]*)',
            r'目標族群[：:]\s*([^【\n]*)',
            r'目標受眾[：:]\s*([^【\n]*)',
        ]
        for pattern in patterns:
            match = re.search(pattern, structured_brief_text, re.DOTALL | re.IGNORECASE)
            if match:
                target_audience = match.group(1).strip()
                break
    
    if not marketing_goals:
        # Try regex patterns for marketing goals
        patterns = [
            r'【專案概要】\s*([^【]*)',
            r'【需求項目】\s*([^【]*)',
            r'【行銷目標】\s*([^【]*)',
            r'【Marketing Goals】\s*([^【]*)',
            r'【Project Overview】\s*([^【]*)',
            r'行銷目標[：:]\s*([^【\n]*)',
            r'專案概要[：:]\s*([^【\n]*)',
        ]
        for pattern in patterns:
            match = re.search(pattern, structured_brief_text, re.DOTALL | re.IGNORECASE)
            if match:
                marketing_goals = match.group(1).strip()
                break
    
    # Clean up the extracted content
    if target_audience:
        target_audience = clean_extracted_text(target_audience)
    if marketing_goals:
        marketing_goals = clean_extracted_text(marketing_goals)
    
    return {
        'target_audience': target_audience,
        'marketing_goals': marketing_goals
    }

def clean_extracted_text(text):
    """
    Clean extracted text by removing extra whitespace and formatting
    """
    if not text:
        return None
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Remove common prefixes
    text = re.sub(r'^[-\s]*', '', text)
    
    # Remove trailing punctuation and whitespace
    text = text.rstrip('.,;:')
    
    return text if text else None