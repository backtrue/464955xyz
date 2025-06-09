"""
Internationalization utility functions and translations
"""

from flask import session, request
from app import app

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        # Navigation
        'marketing_hub': 'Marketing Hub',
        'dashboard': 'Dashboard',
        'create_brief': 'Create Brief',
        'login': 'Login',
        'register': 'Register',
        'logout': 'Logout',
        
        # Landing page
        'welcome_title': 'Welcome to 464955.xyz',
        'welcome_subtitle': '4649 (よろしく) = Let\'s work together, 55 = You and me, achieving together. A digital bulletin board that tells stories through marketing and matches through data.',
        'get_started': 'Get Started',
        'sign_in': 'Sign In',
        'go_to_dashboard': 'Go to Dashboard',
        
        # Features
        'for_clients': 'For Clients',
        'for_clients_desc': 'Describe your marketing needs in natural language. Our system automatically generates structured briefs and connects you with qualified professionals.',
        'smart_brief_generation': 'Smart Brief Generation',
        'smart_brief_desc': 'Advanced algorithms analyze your requirements and create detailed project briefs with budget estimates, timelines, and recommended strategies.',
        'for_professionals': 'For Professionals',
        'for_professionals_desc': 'Browse structured briefs, submit competitive proposals, and showcase your expertise to win new clients in the marketing industry.',
        
        # How it works
        'how_it_works': 'How It Works',
        'client_step_1': 'Register as a client and complete your profile',
        'client_step_2': 'Describe your marketing needs in natural language',
        'client_step_3': 'Review the automatically generated structured brief',
        'client_step_4': 'Publish your brief and receive proposals',
        'client_step_5': 'Choose the best professional for your project',
        'pro_step_1': 'Register as a professional and build your profile',
        'pro_step_2': 'Browse available project briefs',
        'pro_step_3': 'Submit detailed proposals with pricing',
        'pro_step_4': 'Showcase your portfolio and expertise',
        'pro_step_5': 'Win projects and grow your business',
        
        # Registration
        'create_account': 'Create Account',
        'i_am_a': 'I am a:',
        'client': 'Client',
        'client_desc': 'I need marketing services',
        'professional': 'Professional',
        'professional_desc': 'I provide marketing services',
        'full_name': 'Full Name',
        'email_address': 'Email Address',
        'company_name': 'Company Name',
        'optional': '(Optional)',
        'password': 'Password',
        'password_requirement': 'Password must be at least 6 characters long.',
        'already_have_account': 'Already have an account?',
        'sign_in_here': 'Sign in here',
        
        # Login
        'dont_have_account': "Don't have an account?",
        'register_here': 'Register here',
        
        # Dashboard
        'client_dashboard': 'Client Dashboard',
        'professional_dashboard': 'Professional Dashboard',
        'welcome_back': 'Welcome back',
        'create_new_brief': 'Create New Brief',
        'total_briefs': 'Total Briefs',
        'active_briefs': 'Active Briefs',
        'total_proposals': 'Total Proposals',
        'available_briefs': 'Available Briefs',
        'my_proposals': 'My Proposals',
        'accepted': 'Accepted',
        'your_briefs': 'Your Briefs',
        
        # Brief creation
        'create_marketing_brief': 'Create Marketing Brief',
        'describe_needs': 'Describe your marketing needs in natural language. Our system will automatically generate a structured brief.',
        'tips_for_better_results': 'Tips for better results:',
        'describe_your_marketing_needs': 'Describe Your Marketing Needs',
        'need_inspiration': 'Need inspiration? Try these examples:',
        'back_to_dashboard': 'Back to Dashboard',
        'generate_brief': 'Post Project',
        
        # Brief details
        'project_description': 'Project Description',
        'marketing_goals': 'Marketing Goals',
        'target_audience': 'Target Audience',
        'suggested_services': 'Suggested Services',
        'original_request': 'Original Request',
        'submit_proposal': 'Submit Proposal',
        'view_proposals': 'View Proposals',
        'brief_details': 'Brief Details',
        'budget_range': 'Budget Range',
        'duration': 'Duration',
        'weeks': 'weeks',
        'preferred_platforms': 'Preferred Platforms',
        'client': 'Client',
        'posted': 'Posted',
        'proposals_received': 'Proposals Received',
        'proposals': 'proposals',
        
        # Proposal submission
        'submit_proposal_title': 'Submit Proposal',
        'submit_proposal_for': 'Submit your proposal for:',
        'your_price': 'Your Price (USD)',
        'estimated_duration_days': 'Estimated Duration (Days)',
        'proposal_details': 'Proposal Details',
        'portfolio_sample_links': 'Portfolio/Sample Links',
        'tips_for_winning_proposal': 'Tips for a winning proposal:',
        'back_to_brief': 'Back to Brief',
        
        # Common
        'title': 'Title',
        'platform': 'Platform',
        'budget': 'Budget',
        'status': 'Status',
        'created': 'Created',
        'actions': 'Actions',
        'active': 'Active',
        'closed': 'Closed',
        'pending': 'Pending',
        'rejected': 'Rejected',
        'view': 'View',
        'propose': 'Propose',
        'price': 'Price',
        'message': 'Message',
        'days': 'days',
        'submitted': 'Submitted',
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
        'info': 'Info',
        'warning': 'Warning',
        
        # Language selector
        'language': 'Language',
        'select_language': 'Select Language',
        
        # Additional common phrases
        'no_proposals': 'No proposals',
        'to_be_discussed': 'To be discussed',
        'not_specified': 'Not specified',
        'weeks_short': 'weeks',
        'professional_dashboard': 'Professional Dashboard',
        'available_briefs': 'Available Briefs',
        'my_proposals': 'My Proposals',
        'accepted': 'Accepted',
        'preferred_platforms': 'Preferred Platforms',
        'posted': 'Posted',
        'proposals_for': 'Proposals for',
        
        # Create brief form tips
        'tip_business_type': 'Mention your business type and target audience',
        'tip_platforms': 'Specify platforms you\'re interested in (Instagram, Facebook, Google Ads, etc.)',
        'tip_budget': 'Include your budget range if known',
        'tip_goals': 'Mention your goals (brand awareness, lead generation, sales, etc.)',
        'tip_timeline': 'Specify timeline preferences',
        'textarea_placeholder': 'Example: I run a fitness studio and need help with social media marketing to attract new members. I\'m particularly interested in Instagram and Facebook campaigns to reach young professionals aged 25-40 in my local area. My budget is around $2,000-3,000 per month, and I want to focus on increasing brand awareness and generating leads for trial memberships. I\'d like to start with a 2-month campaign to test effectiveness...',
        'textarea_help_text': 'Please provide at least 50 characters with detailed information about your marketing needs.',
        'ecommerce_example': 'E-commerce Example',
        'ecommerce_example_text': '"I have an online clothing store targeting millennials. Need comprehensive digital marketing including Instagram ads, influencer partnerships, and email campaigns. Budget is $5,000/month for 3 months to boost holiday sales."',
        'service_example': 'Service Business Example',
        'service_example_text': '"I\'m a financial advisor looking to generate qualified leads through LinkedIn and Google Ads. Target audience is business owners and high-income professionals. Budget around $3,000/month, need content creation and lead nurturing campaigns."',
        'use_this': 'Use This',
        'ready_to_get_started': 'Ready to Get Started?',
        'join_platform_desc': 'Join our platform and connect with the right marketing professionals today.',
        'start_now': 'Start Now',
    },
    
    'zh': {
        # Navigation
        'marketing_hub': '行銷媒合平台',
        'dashboard': '控制台',
        'create_brief': '建立專案',
        'login': '登入',
        'register': '註冊',
        'logout': '登出',
        
        # Landing page
        'welcome_title': '歡迎來到 464955.xyz',
        'welcome_subtitle': '4649（よろしく）= 讓我們一起工作，55 = 是你，也是我，我們互相成就。用行銷說故事，也用數據媒合的數位佈告欄。',
        'get_started': '開始使用',
        'sign_in': '登入',
        'go_to_dashboard': '前往控制台',
        
        # Features
        'for_clients': '客戶服務',
        'for_clients_desc': '用自然語言描述您的行銷需求。我們的系統會自動生成結構化的專案簡介，並為您連接合格的專業人士。',
        'smart_brief_generation': '智能簡介生成',
        'smart_brief_desc': '先進的演算法分析您的需求，創建包含預算估算、時程安排和推薦策略的詳細專案簡介。',
        'for_professionals': '專業人士服務',
        'for_professionals_desc': '瀏覽結構化的專案簡介，提交具競爭力的提案，展示您的專業知識以贏得新客戶。',
        
        # How it works
        'how_it_works': '運作方式',
        'client_step_1': '註冊為客戶並完善您的個人資料',
        'client_step_2': '用自然語言描述您的行銷需求',
        'client_step_3': '審核自動生成的結構化專案簡介',
        'client_step_4': '發布您的專案簡介並接收提案',
        'client_step_5': '選擇最適合您專案的專業人士',
        'pro_step_1': '註冊為專業人士並建立您的個人資料',
        'pro_step_2': '瀏覽可用的專案簡介',
        'pro_step_3': '提交包含定價的詳細提案',
        'pro_step_4': '展示您的作品集和專業知識',
        'pro_step_5': '贏得專案並發展您的業務',
        
        # Registration
        'create_account': '建立帳戶',
        'i_am_a': '我是：',
        'client': '客戶',
        'client_desc': '我需要行銷服務',
        'professional': '專業人士',
        'professional_desc': '我提供行銷服務',
        'full_name': '姓名',
        'email_address': '電子郵件地址',
        'company_name': '公司名稱',
        'optional': '（選填）',
        'password': '密碼',
        'password_requirement': '密碼必須至少6個字元。',
        'already_have_account': '已經有帳戶了？',
        'sign_in_here': '在此登入',
        
        # Login
        'dont_have_account': '還沒有帳戶？',
        'register_here': '在此註冊',
        
        # Dashboard
        'client_dashboard': '客戶控制台',
        'professional_dashboard': '專業人士控制台',
        'welcome_back': '歡迎回來',
        'create_new_brief': '建立新專案',
        'total_briefs': '總專案數',
        'active_briefs': '進行中專案',
        'total_proposals': '總提案數',
        'available_briefs': '可用專案',
        'my_proposals': '我的提案',
        'accepted': '已接受',
        'your_briefs': '您的專案',
        
        # Brief creation
        'create_marketing_brief': '建立行銷專案簡介',
        'describe_needs': '用自然語言描述您的行銷需求。我們的系統將自動生成結構化的專案簡介。',
        'tips_for_better_results': '獲得更好結果的提示：',
        'describe_your_marketing_needs': '描述您的行銷需求',
        'need_inspiration': '需要靈感？試試這些範例：',
        'back_to_dashboard': '返回控制台',
        'generate_brief': '我要發案',
        
        # Brief details
        'project_description': '專案描述',
        'marketing_goals': '行銷目標',
        'target_audience': '目標受眾',
        'suggested_services': '建議服務',
        'original_request': '原始需求',
        'submit_proposal': '提交提案',
        'view_proposals': '查看提案',
        'brief_details': '專案詳情',
        'budget_range': '預算範圍',
        'duration': '持續時間',
        'weeks': '週',
        'preferred_platforms': '偏好平台',
        'client': '客戶',
        'posted': '發布於',
        'proposals_received': '收到的提案',
        'proposals': '個提案',
        
        # Proposal submission
        'submit_proposal_title': '提交提案',
        'submit_proposal_for': '為以下專案提交您的提案：',
        'your_price': '您的報價（美元）',
        'estimated_duration_days': '預估天數',
        'proposal_details': '提案詳情',
        'portfolio_sample_links': '作品集/範例連結',
        'tips_for_winning_proposal': '獲勝提案的技巧：',
        'back_to_brief': '返回專案簡介',
        
        # Common
        'title': '標題',
        'platform': '平台',
        'budget': '預算',
        'status': '狀態',
        'created': '建立時間',
        'actions': '操作',
        'active': '進行中',
        'closed': '已關閉',
        'pending': '待審核',
        'rejected': '已拒絕',
        'view': '查看',
        'propose': '提案',
        'price': '價格',
        'message': '訊息',
        'days': '天',
        'submitted': '已提交',
        'loading': '載入中...',
        'error': '錯誤',
        'success': '成功',
        'info': '資訊',
        'warning': '警告',
        
        # Language selector
        'language': '語言',
        'select_language': '選擇語言',
        
        # Additional common phrases
        'no_proposals': '暫無提案',
        'to_be_discussed': '待討論',
        'not_specified': '未指定',
        'weeks_short': '週',
        'professional_dashboard': '專業人員儀表板',
        'available_briefs': '可接案件',
        'my_proposals': '我的提案',
        'accepted': '已接受',
        'preferred_platforms': '偏好平台',
        'posted': '發布於',
        'proposals_for': '提案 -',
        
        # Create brief form tips
        'tip_business_type': '提及您的業務類型和目標受眾',
        'tip_platforms': '指定您感興趣的平台（Instagram、Facebook、Google Ads 等）',
        'tip_budget': '如果知道的話，請包含您的預算範圍',
        'tip_goals': '提及您的目標（品牌知名度、潛在客戶生成、銷售等）',
        'tip_timeline': '指定時間線偏好',
        'textarea_placeholder': '範例：我經營一家健身工作室，需要幫助進行社交媒體行銷以吸引新會員。我特別感興趣的是 Instagram 和 Facebook 活動，以觸及我當地 25-40 歲的年輕專業人士。我的預算大約是每月 2,000-3,000 美元，我想專注於提高品牌知名度並為試用會員資格產生潛在客戶。我想從為期 2 個月的活動開始測試效果...',
        'textarea_help_text': '請提供至少 50 個字符，詳細說明您的行銷需求。',
        'ecommerce_example': '電商範例',
        'ecommerce_example_text': '"我有一家針對千禧世代的線上服裝店。需要全面的數位行銷，包括 Instagram 廣告、影響者合作夥伴關係和電子郵件活動。預算為每月 5,000 美元，為期 3 個月，以促進節日銷售。"',
        'service_example': '服務業範例',
        'service_example_text': '"我是一名財務顧問，希望通過 LinkedIn 和 Google Ads 產生合格的潛在客戶。目標受眾是企業主和高收入專業人士。預算約每月 3,000 美元，需要內容創建和潛在客戶培養活動。"',
        'use_this': '使用此範例',
        'ready_to_get_started': '準備好開始了嗎？',
        'join_platform_desc': '加入我們的平台，今天就與合適的行銷專業人士聯繫。',
        'start_now': '立即開始',
    },
    
    'ja': {
        # Navigation
        'marketing_hub': 'マーケティングハブ',
        'dashboard': 'ダッシュボード',
        'create_brief': 'ブリーフ作成',
        'login': 'ログイン',
        'register': '登録',
        'logout': 'ログアウト',
        
        # Landing page
        'welcome_title': '464955.xyz へようこそ',
        'welcome_subtitle': '4649（よろしく）= Let\'s work together、55 = あなたも私も、お互いに成長し合う。マーケティングでストーリーを語り、データでマッチングするデジタル掲示板。',
        'get_started': '始める',
        'sign_in': 'サインイン',
        'go_to_dashboard': 'ダッシュボードへ',
        
        # Features
        'for_clients': 'クライアント向け',
        'for_clients_desc': '自然言語でマーケティングニーズを記述してください。システムが自動的に構造化されたブリーフを生成し、資格のある専門家と繋げます。',
        'smart_brief_generation': 'スマートブリーフ生成',
        'smart_brief_desc': '高度なアルゴリズムがご要望を分析し、予算見積もり、タイムライン、推奨戦略を含む詳細なプロジェクトブリーフを作成します。',
        'for_professionals': '専門家向け',
        'for_professionals_desc': '構造化されたブリーフを閲覧し、競争力のあるプロポーザルを提出して、専門知識を活かして新しいクライアントを獲得しましょう。',
        
        # How it works
        'how_it_works': '仕組み',
        'client_step_1': 'クライアントとして登録し、プロフィールを完成させる',
        'client_step_2': '自然言語でマーケティングニーズを記述する',
        'client_step_3': '自動生成された構造化ブリーフを確認する',
        'client_step_4': 'ブリーフを公開してプロポーザルを受け取る',
        'client_step_5': 'プロジェクトに最適な専門家を選ぶ',
        'pro_step_1': '専門家として登録し、プロフィールを構築する',
        'pro_step_2': '利用可能なプロジェクトブリーフを閲覧する',
        'pro_step_3': '価格を含む詳細なプロポーザルを提出する',
        'pro_step_4': 'ポートフォリオと専門知識をアピールする',
        'pro_step_5': 'プロジェクトを獲得してビジネスを成長させる',
        
        # Registration
        'create_account': 'アカウント作成',
        'i_am_a': '私は：',
        'client': 'クライアント',
        'client_desc': 'マーケティングサービスが必要',
        'professional': '専門家',
        'professional_desc': 'マーケティングサービスを提供',
        'full_name': '氏名',
        'email_address': 'メールアドレス',
        'company_name': '会社名',
        'optional': '（任意）',
        'password': 'パスワード',
        'password_requirement': 'パスワードは6文字以上である必要があります。',
        'already_have_account': 'すでにアカウントをお持ちですか？',
        'sign_in_here': 'こちらからサインイン',
        
        # Login
        'dont_have_account': 'アカウントをお持ちでない方は',
        'register_here': 'こちらから登録',
        
        # Dashboard
        'client_dashboard': 'クライアントダッシュボード',
        'professional_dashboard': '専門家ダッシュボード',
        'welcome_back': 'おかえりなさい',
        'create_new_brief': '新しいブリーフを作成',
        'total_briefs': '総ブリーフ数',
        'active_briefs': 'アクティブなブリーフ',
        'total_proposals': '総プロポーザル数',
        'available_briefs': '利用可能なブリーフ',
        'my_proposals': '私のプロポーザル',
        'accepted': '承認済み',
        'your_briefs': 'あなたのブリーフ',
        
        # Brief creation
        'create_marketing_brief': 'マーケティングブリーフ作成',
        'describe_needs': '自然言語でマーケティングニーズを記述してください。システムが自動的に構造化されたブリーフを生成します。',
        'tips_for_better_results': 'より良い結果を得るためのコツ：',
        'describe_your_marketing_needs': 'マーケティングニーズを記述',
        'need_inspiration': 'インスピレーションが必要ですか？以下の例をお試しください：',
        'back_to_dashboard': 'ダッシュボードに戻る',
        'generate_brief': 'プロジェクト投稿',
        
        # Brief details
        'project_description': 'プロジェクト概要',
        'marketing_goals': 'マーケティング目標',
        'target_audience': 'ターゲット層',
        'suggested_services': '推奨サービス',
        'original_request': '元のリクエスト',
        'submit_proposal': 'プロポーザル提出',
        'view_proposals': 'プロポーザル確認',
        'brief_details': 'ブリーフ詳細',
        'budget_range': '予算範囲',
        'duration': '期間',
        'weeks': '週間',
        'preferred_platforms': '希望プラットフォーム',
        'client': 'クライアント',
        'posted': '投稿日',
        'proposals_received': '受信プロポーザル',
        'proposals': '件のプロポーザル',
        
        # Proposal submission
        'submit_proposal_title': 'プロポーザル提出',
        'submit_proposal_for': '以下のプロジェクトにプロポーザルを提出：',
        'your_price': 'お見積もり価格（USD）',
        'estimated_duration_days': '予想期間（日数）',
        'proposal_details': 'プロポーザル詳細',
        'portfolio_sample_links': 'ポートフォリオ/サンプルリンク',
        'tips_for_winning_proposal': '勝てるプロポーザルのコツ：',
        'back_to_brief': 'ブリーフに戻る',
        
        # Common
        'title': 'タイトル',
        'platform': 'プラットフォーム',
        'budget': '予算',
        'status': 'ステータス',
        'created': '作成日',
        'actions': 'アクション',
        'active': 'アクティブ',
        'closed': 'クローズ',
        'pending': '審査中',
        'rejected': '却下',
        'view': '表示',
        'propose': '提案',
        'price': '価格',
        'message': 'メッセージ',
        'days': '日',
        'submitted': '提出済み',
        'loading': '読み込み中...',
        'error': 'エラー',
        'success': '成功',
        'info': '情報',
        'warning': '警告',
        
        # Language selector
        'language': '言語',
        'select_language': '言語選択',
        
        # Additional common phrases
        'no_proposals': 'プロポーザルなし',
        'to_be_discussed': '要相談',
        'not_specified': '未指定',
        'weeks_short': '週間',
        'professional_dashboard': 'プロフェッショナルダッシュボード',
        'available_briefs': '利用可能なブリーフ',
        'my_proposals': '私の提案',
        'accepted': '承認済み',
        'preferred_platforms': '希望プラットフォーム',
        'posted': '投稿日',
        'proposals_for': '提案 -',
        
        # Create brief form tips
        'tip_business_type': 'ビジネスタイプとターゲットオーディエンスを記載してください',
        'tip_platforms': '興味のあるプラットフォームを指定してください（Instagram、Facebook、Google Ads など）',
        'tip_budget': '分かる場合は予算範囲を含めてください',
        'tip_goals': '目標を記載してください（ブランド認知度、リード生成、売上など）',
        'tip_timeline': 'タイムラインの希望を指定してください',
        'textarea_placeholder': '例：フィットネススタジオを経営しており、新しい会員を獲得するためのソーシャルメディアマーケティングのサポートが必要です。特に地域の25-40歳の若い専門職をターゲットにしたInstagramとFacebookキャンペーンに興味があります。予算は月額2,000-3,000ドル程度で、ブランド認知度の向上と体験会員のリード生成に焦点を当てたいと思っています。効果をテストするために2ヶ月のキャンペーンから始めたいと思います...',
        'textarea_help_text': 'マーケティングニーズについて詳細な情報を少なくとも50文字で提供してください。',
        'ecommerce_example': 'Eコマース例',
        'ecommerce_example_text': '"ミレニアル世代をターゲットにしたオンライン衣料品店を運営しています。Instagram広告、インフルエンサーパートナーシップ、メールキャンペーンを含む包括的なデジタルマーケティングが必要です。ホリデーセールスを促進するため、月額5,000ドルで3ヶ月間の予算です。"',
        'service_example': 'サービス業例',
        'service_example_text': '"LinkedInとGoogle Adsを通じて質の高いリードを生成したいファイナンシャルアドバイザーです。ターゲットオーディエンスは企業オーナーと高収入の専門職です。月額約3,000ドルの予算で、コンテンツ作成とリード育成キャンペーンが必要です。"',
        'use_this': 'これを使用',
        'ready_to_get_started': 'Ready to Get Started?',
        'join_platform_desc': 'Join our platform and connect with the right marketing professionals today.',
        'start_now': 'Start Now',
    }
}

def get_current_language():
    """Get the current language from session or default to English"""
    from flask import session, request
    
    # Check if language is set in session
    if 'language' in session:
        return session['language']
    
    # Check if language is in URL parameters
    if request.args.get('lang'):
        session['language'] = request.args.get('lang')
        return session['language']
    
    # Use browser's preferred language
    if hasattr(request, 'accept_languages'):
        return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'en'
    
    return 'en'

def _(key):
    """Get translated text for the given key"""
    lang = get_current_language()
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS['en'].get(key, key))

def get_languages():
    """Get available languages"""
    return app.config['LANGUAGES']