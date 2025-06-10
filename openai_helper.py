import os
import json
from openai import OpenAI
import logging

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_client_requirements(raw_input, service_type):
    """
    Analyze client's natural language input and generate a professional brief
    that helps marketing professionals quickly assess if a project is worth taking
    """
    
    service_context = {
        'meta_ads': 'Meta廣告投放 (Facebook & Instagram)',
        'google_ads': 'Google Ads 廣告投放', 
        'seo': '電商 SEO 搜尋引擎優化'
    }
    
    service_name = service_context.get(service_type, service_type)
    
    prompt = f"""
你是一位資深行銷顧問，專門幫助甲方（客戶）和乙方（行銷專業人士）建立有效的合作關係。

請分析以下甲方的自然語言需求，並生成一個專業的 brief 讓乙方能快速判斷是否值得接案：

原始需求：{raw_input}
服務類型：{service_name}

請按照以下格式分析並輸出：

📋【專案基本資訊】
• 產業類別：[從輸入中識別甲方所屬行業]
• 業務模式：[線上/線下/混合型]
• 目標受眾：[甲方心中的初步目標受眾]
• 行銷目標：[甲方想達成的具體目標]
• 月預算範圍：[從輸入中提取的預算資訊]

📋【專案描述】
[重新組織後的專業專案描述，讓乙方一目了然甲方的真實需求]

📋【建議服務項目】
根據需求和服務類型，建議的具體執行項目：
• 項目1
• 項目2  
• 項目3

📋【乙方專業評估】
🔍 機會分析：
[這個案子的潛在價值和發展機會]

⚠️ 需要確認的問題：
[乙方接案前應該向甲方釐清的關鍵問題]

🚨 潛在風險提醒：
[可能的挑戰、陷阱或需要注意的地方]

📋【建議合作條件】
• 建議專案週期：[週數]
• 建議平台組合：[根據需求推薦的廣告平台]
• 預估工作量：[輕度/中度/重度]

請用繁體中文回應，內容要專業且能幫助乙方快速做出接案決定。
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "你是專業的行銷策略顧問，擅長分析客戶需求並為行銷專業人士提供案件評估建議。回應要專業、客觀，幫助乙方做出明智的接案決定。"
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        analysis_result = response.choices[0].message.content
        if analysis_result:
            return analysis_result.strip()
        else:
            return "抱歉，無法分析需求。請提供更詳細的資訊。"
        
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return f"抱歉，無法分析需求。錯誤：{str(e)}"

def generate_structured_brief(raw_input, service_type):
    """
    Convert raw marketing requirements into structured brief format using GPT-4o-mini
    """
    
    # Service type mapping for context
    service_context = {
        'meta_ads': 'Meta廣告投放 (Facebook & Instagram)',
        'google_ads': 'Google Ads 廣告投放',
        'seo': '電商 SEO 搜尋引擎優化'
    }
    
    service_name = service_context.get(service_type, service_type)
    
    prompt = f"""
請將以下行銷需求轉換為結構化的專案簡介格式，針對{service_name}服務：

原始需求：
{raw_input}

請按照以下格式輸出結構化簡介：

📌【專案概要】
簡短敘述此專案的目的與背景

📌【目標族群】
明確指出受眾對象（年齡、性別、生活風格或購物習慣）

📌【需求項目】
列出本次希望乙方執行的具體行銷項目，例如：
- 項目1
- 項目2
- 項目3

📌【預算與時程】
- 預算範圍：根據原始需求推估或標註"待討論"
- 開始日期：YYYY/MM/DD 或 "待確認"
- 是否可分期／靈活調整：是／否

📌【專案目標】
本次行銷活動希望達成的商業指標或預期成果

📌【執行配合事項】
- 素材提供：需要進一步確認
- 文案撰寫：需要進一步確認  
- 溝通頻率：需要進一步確認

📌【其他說明或限制條件】
根據原始需求提及的特殊要求或限制

📌【可提供之資源】
根據原始需求推估可能有的資源

📌【乙方需特別具備】
根據{service_name}和原始需求，列出專業要求

📌【補充說明】
其他重要資訊或背景

請用繁體中文回應，內容要專業且具體。如果原始需求中某些資訊不足，請合理推估或標註"待確認"。
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini as requested
            messages=[
                {
                    "role": "system", 
                    "content": "你是一位專業的行銷專案經理，擅長將客戶需求轉換為結構化的專案簡介。請用繁體中文回應，內容要專業、具體且實用。"
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        structured_brief = response.choices[0].message.content
        if structured_brief:
            return structured_brief.strip()
        else:
            return "抱歉，無法生成結構化簡介。"
        
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return f"抱歉，無法生成結構化簡介。錯誤：{str(e)}"

def generate_followup_questions(structured_brief):
    """
    Generate the three follow-up questions based on the structured brief
    """
    questions = {
        'materials': {
            'question': '🟧 補問 1：素材由誰提供？\n行銷素材（圖片 / 影片）由誰提供？',
            'options': [
                '我方已有素材',
                '希望乙方提供', 
                '雙方協作製作'
            ]
        },
        'copywriting': {
            'question': '🟧 補問 2：文案由誰撰寫？\n本次行銷所需文案（如貼文、廣告標題、EDM）由誰撰寫？',
            'options': [
                '我方會提供',
                '希望乙方撰寫',
                '雙方協作產出'
            ]
        },
        'communication': {
            'question': '🟧 補問 3：溝通與開會頻率？\n雙方預期的對接頻率為何？',
            'options': [
                '每週一次會議',
                '每月一次',
                '關鍵節點對接即可',
                '不需會議，僅需非同步聯繫'
            ]
        }
    }
    
    return questions