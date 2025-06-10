"""
Title generation utility for creating optimized brief titles
Format: {服務類型}|{月預算}|{AI摘要}
"""
import re
from openai_helper import generate_structured_brief
import os
from openai import OpenAI

def generate_optimized_title(service_type, budget_min, budget_max, raw_input, structured_brief=None, budget_currency='USD'):
    """
    Generate optimized title in format: {服務類型}|{月預算}|{AI摘要}
    Maximum 60 Chinese characters
    """
    try:
        # Service type mapping
        service_type_map = {
            'meta_ads': 'Meta廣告',
            'google_ads': 'Google廣告', 
            'seo': 'SEO優化'
        }
        
        service_name = service_type_map.get(service_type, service_type)
        
        # Budget formatting with currency
        currency_symbols = {
            'USD': '$',
            'TWD': 'NT$',
            'JPY': '¥'
        }
        
        currency_symbol = currency_symbols.get(budget_currency, '$')
        
        if budget_min and budget_max:
            if budget_min == budget_max:
                budget_text = f"{currency_symbol}{budget_min:,}/月"
            else:
                budget_text = f"{currency_symbol}{budget_min:,}-{budget_max:,}/月"
        elif budget_min:
            budget_text = f"{currency_symbol}{budget_min:,}+/月"
        elif budget_max:
            budget_text = f"{currency_symbol}{budget_max:,}以下/月"
        else:
            budget_text = "預算面議"
        
        # Generate AI summary using OpenAI
        ai_summary = generate_ai_summary(raw_input, structured_brief)
        
        # Construct title
        title_parts = [service_name, budget_text, ai_summary]
        full_title = "|".join(title_parts)
        
        # Ensure title doesn't exceed 60 characters
        if len(full_title) > 60:
            # Trim the AI summary part
            max_summary_length = 60 - len(service_name) - len(budget_text) - 2  # 2 for the | separators
            if max_summary_length > 10:
                ai_summary = ai_summary[:max_summary_length-1] + "…"
                full_title = "|".join([service_name, budget_text, ai_summary])
            else:
                # If still too long, use basic format
                full_title = f"{service_name}|{budget_text}"
        
        return full_title
        
    except Exception as e:
        print(f"Title generation error: {e}")
        # Fallback to simple format
        service_type_map = {
            'meta_ads': 'Meta廣告',
            'google_ads': 'Google廣告', 
            'seo': 'SEO優化'
        }
        service_name = service_type_map.get(service_type, '行銷專案')
        return f"{service_name}|預算面議|行銷服務需求"

def generate_ai_summary(raw_input, structured_brief=None):
    """
    Generate a concise AI summary for the title
    """
    try:
        # Check if OpenAI API key is available
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        if not openai_api_key:
            return extract_simple_summary(raw_input)
        
        openai = OpenAI(api_key=openai_api_key)
        
        # Use structured brief if available, otherwise use raw input
        content = structured_brief if structured_brief else raw_input
        
        prompt = f"""
        請為以下行銷需求生成一個簡潔的摘要，用於標題顯示。
        要求：
        1. 最多15個中文字
        2. 突出核心需求或目標
        3. 使用簡潔的商業語言
        4. 不要包含預算資訊
        
        行銷需求：
        {content}
        
        請只回覆摘要文字，不要其他內容。
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.7
        )
        
        summary = response.choices[0].message.content or ""
        summary = summary.strip()
        
        # Clean up the summary
        summary = re.sub(r'^[「」『』"\'"]*|[「」『』"\'"]*$', '', summary)
        summary = summary.replace('\n', '').replace('\r', '')
        
        # Ensure it's not too long
        if len(summary) > 20:
            summary = summary[:19] + "…"
            
        return summary
        
    except Exception as e:
        print(f"AI summary generation error: {e}")
        return extract_simple_summary(raw_input)

def extract_simple_summary(text):
    """
    Extract a simple summary from text when AI is not available
    """
    try:
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Look for key business terms
        business_keywords = [
            '品牌推廣', '流量增長', '銷售提升', '會員招募', '產品行銷',
            '社群經營', '廣告投放', '內容行銷', '網站優化', '轉換率優化',
            '潛在客戶', '市場拓展', '數位行銷', '電商推廣', '客戶獲取'
        ]
        
        # Find matching keywords
        found_keywords = []
        for keyword in business_keywords:
            if keyword in text:
                found_keywords.append(keyword)
        
        if found_keywords:
            return found_keywords[0]
        
        # Extract first meaningful phrase (up to 15 chars)
        sentences = re.split(r'[。！？．,，]', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) >= 5 and len(sentence) <= 15:
                return sentence
        
        # Fallback: use first 10 characters
        if len(text) > 10:
            return text[:9] + "…"
        else:
            return text or "行銷服務"
            
    except Exception:
        return "行銷服務"