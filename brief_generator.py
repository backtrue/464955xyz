import re
import logging

def generate_brief_from_input(raw_input):
    """
    Generate structured brief from natural language input using rule-based logic
    """
    raw_input_lower = raw_input.lower()
    
    # Initialize brief data
    brief_data = {
        'title': 'Marketing Project',
        'description': raw_input,
        'platform_preference': None,
        'budget_min': None,
        'budget_max': None,
        'suggested_items': '',
        'duration_weeks': None,
        'marketing_goals': '',
        'target_audience': ''
    }
    
    try:
        # Extract title from input (use first sentence or first 50 chars)
        title_match = re.search(r'^([^.!?]+)', raw_input.strip())
        if title_match:
            title = title_match.group(1).strip()
            if len(title) > 5:
                brief_data['title'] = title[:100]
        
        # Extract budget information
        budget_patterns = [
            r'budget.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:to|[-~])\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:to|[-~])\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'budget.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        ]
        
        for pattern in budget_patterns:
            budget_match = re.search(pattern, raw_input_lower)
            if budget_match:
                try:
                    if len(budget_match.groups()) == 2:
                        brief_data['budget_min'] = int(budget_match.group(1).replace(',', ''))
                        brief_data['budget_max'] = int(budget_match.group(2).replace(',', ''))
                    else:
                        budget_amount = int(budget_match.group(1).replace(',', ''))
                        brief_data['budget_min'] = budget_amount
                        brief_data['budget_max'] = budget_amount
                    break
                except ValueError:
                    continue
        
        # Extract platform preferences
        platforms = {
            'instagram': ['instagram', 'ig', 'insta'],
            'facebook': ['facebook', 'fb'],
            'google ads': ['google ads', 'google adwords', 'ppc', 'search ads'],
            'tiktok': ['tiktok', 'tik tok'],
            'youtube': ['youtube', 'yt'],
            'linkedin': ['linkedin'],
            'twitter': ['twitter', 'x.com'],
            'email': ['email', 'newsletter', 'edm'],
            'seo': ['seo', 'search engine optimization'],
            'content marketing': ['content marketing', 'blog', 'articles']
        }
        
        detected_platforms = []
        for platform, keywords in platforms.items():
            for keyword in keywords:
                if keyword in raw_input_lower:
                    detected_platforms.append(platform)
                    break
        
        if detected_platforms:
            brief_data['platform_preference'] = ', '.join(detected_platforms[:3])
        
        # Extract duration/timeline
        duration_patterns = [
            r'(\d+)\s*week',
            r'(\d+)\s*month',
            r'(\d+)\s*day'
        ]
        
        for pattern in duration_patterns:
            duration_match = re.search(pattern, raw_input_lower)
            if duration_match:
                duration_num = int(duration_match.group(1))
                if 'week' in pattern:
                    brief_data['duration_weeks'] = duration_num
                elif 'month' in pattern:
                    brief_data['duration_weeks'] = duration_num * 4
                elif 'day' in pattern:
                    brief_data['duration_weeks'] = max(1, duration_num // 7)
                break
        
        # Default duration if not specified
        if not brief_data['duration_weeks']:
            brief_data['duration_weeks'] = 4
        
        # Extract marketing goals
        goal_keywords = {
            'brand awareness': ['brand awareness', 'awareness', 'visibility', 'recognition'],
            'lead generation': ['leads', 'lead generation', 'customers', 'inquiries'],
            'sales': ['sales', 'revenue', 'conversions', 'purchases'],
            'engagement': ['engagement', 'community', 'followers', 'interaction'],
            'traffic': ['traffic', 'website visits', 'clicks']
        }
        
        detected_goals = []
        for goal, keywords in goal_keywords.items():
            for keyword in keywords:
                if keyword in raw_input_lower:
                    detected_goals.append(goal)
                    break
        
        if detected_goals:
            brief_data['marketing_goals'] = ', '.join(detected_goals[:3])
        else:
            brief_data['marketing_goals'] = 'Brand awareness, lead generation'
        
        # Extract target audience
        audience_patterns = [
            r'target(?:ing|ed)?\s+(?:audience|customers?|users?)\s+(?:is|are|include[s]?)?\s*([^.!?]+)',
            r'(?:audience|customers?|users?)\s+(?:is|are|include[s]?)?\s*([^.!?]+)',
            r'for\s+([a-zA-Z\s]+(?:aged?|years?|demographics?)[^.!?]*)',
        ]
        
        for pattern in audience_patterns:
            audience_match = re.search(pattern, raw_input_lower)
            if audience_match:
                audience = audience_match.group(1).strip()
                if len(audience) > 10 and len(audience) < 200:
                    brief_data['target_audience'] = audience.capitalize()
                    break
        
        if not brief_data['target_audience']:
            brief_data['target_audience'] = 'General consumers'
        
        # Generate suggested items based on detected platforms and goals
        suggested_items = []
        
        if brief_data['platform_preference']:
            if 'instagram' in brief_data['platform_preference'].lower():
                suggested_items.extend(['Instagram content creation', 'Story campaigns', 'Influencer outreach'])
            if 'facebook' in brief_data['platform_preference'].lower():
                suggested_items.extend(['Facebook ad campaigns', 'Community management'])
            if 'google ads' in brief_data['platform_preference'].lower():
                suggested_items.extend(['PPC campaign setup', 'Keyword research', 'Ad optimization'])
            if 'email' in brief_data['platform_preference'].lower():
                suggested_items.extend(['Email marketing campaigns', 'Newsletter design'])
            if 'seo' in brief_data['platform_preference'].lower():
                suggested_items.extend(['SEO audit', 'Content optimization', 'Link building'])
        
        if 'sales' in brief_data['marketing_goals'].lower():
            suggested_items.append('Conversion optimization')
        if 'lead' in brief_data['marketing_goals'].lower():
            suggested_items.append('Lead magnet creation')
        if 'engagement' in brief_data['marketing_goals'].lower():
            suggested_items.append('Community engagement strategy')
        
        # Default suggestions if none detected
        if not suggested_items:
            suggested_items = ['Strategy development', 'Content creation', 'Campaign management', 'Performance reporting']
        
        brief_data['suggested_items'] = ', '.join(list(set(suggested_items))[:6])
        
    except Exception as e:
        logging.error(f"Brief generation error: {e}")
        # Return basic brief data on error
        pass
    
    return brief_data
