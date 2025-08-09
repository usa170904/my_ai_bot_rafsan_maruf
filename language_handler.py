"""
Language detection and handling for multilingual support
"""

import logging
from typing import Optional
import re

logger = logging.getLogger(__name__)

class LanguageHandler:
    """Handle language detection and multilingual messages"""
    
    def __init__(self):
        # Bengali Unicode character ranges
        self.bengali_pattern = re.compile(r'[\u0980-\u09FF]+')
        
        # Code-related keywords in both languages
        self.code_keywords = {
            'en': [
                'code', 'program', 'function', 'class', 'variable', 'algorithm',
                'python', 'javascript', 'java', 'html', 'css', 'react', 'node',
                'app', 'website', 'database', 'api', 'framework', 'library',
                'build', 'develop', 'write', 'generate', 'make',
                'flutter', 'android', 'ios', 'machine learning', 'ai', 'ml',
                'django', 'flask', 'fastapi', 'express', 'vue', 'angular',
                'mongodb', 'postgresql', 'mysql', 'firebase', 'aws', 'docker',
                'kubernetes', 'microservice', 'blockchain', 'web3', 'smart contract'
            ],
            'bn': [
                'কোড', 'প্রোগ্রাম', 'ফাংশন', 'ক্লাস', 'ভেরিয়েবল', 'অ্যালগরিদম',
                'পাইথন', 'জাভাস্ক্রিপ্ট', 'জাভা', 'এইচটিএমএল', 'সিএসএস',
                'অ্যাপ', 'ওয়েবসাইট', 'ডাটাবেস', 'এপিআই', 'ফ্রেমওয়ার্ক',
                'বানাও', 'লিখ', 'করো', 'বানানো', 'লেখা', 'ডেভেলপ',
                'ফ্লাটার', 'অ্যান্ড্রয়েড', 'আইওএস', 'মেশিন লার্নিং', 'এআই',
                'জ্যাঙ্গো', 'ফ্লাস্ক', 'এক্সপ্রেস', 'ভিউ', 'অ্যাঙ্গুলার',
                'মঙ্গোডিবি', 'পোস্টগ্রেস', 'মাইএসকিউএল', 'ফায়ারবেস',
                'ডকার', 'কুবারনেটিস', 'মাইক্রোসার্ভিস', 'ব্লকচেইন'
            ]
        }
        
        # Predefined messages in both languages
        self.messages = {
            'welcome': {
                'en': """🤖 *Welcome to Multilingual AI Bot!*

I'm your advanced AI assistant powered by Google Gemini! I can help you with:

🔧 *Code Generation*
• Any programming language
• App development
• Website creation
• Problem solving

💡 *Question Answering*
• Technical questions
• General knowledge
• Educational content
• Programming help

🌐 *Languages Supported*
• English
• বাংলা (Bengali)

*Commands:*
/code - Generate code
/app - Create app code
/web - Create website code
/ask - Ask any question
/help - Show this help
/lang - Language info
/status - Bot status

Just type your question or request in any language!""",
                
                'bn': """🤖 *বহুভাষিক AI বট এ স্বাগতম!*

আমি Google Gemini দ্বারা চালিত আপনার উন্নত AI সহায়ক! আমি আপনাকে সাহায্য করতে পারি:

🔧 *কোড তৈরি*
• যেকোনো প্রোগ্রামিং ভাষা
• অ্যাপ ডেভেলপমেন্ট
• ওয়েবসাইট তৈরি
• সমস্যা সমাধান

💡 *প্রশ্নের উত্তর*
• প্রযুক্তিগত প্রশ্ন
• সাধারণ জ্ঞান
• শিক্ষামূলক বিষয়
• প্রোগ্রামিং সাহায্য

🌐 *সমর্থিত ভাষা*
• English
• বাংলা

*কমান্ড সমূহ:*
/code - কোড তৈরি করুন
/app - অ্যাপ কোড তৈরি করুন
/web - ওয়েবসাইট কোড তৈরি করুন
/ask - যেকোনো প্রশ্ন করুন
/help - এই সাহায্য দেখুন
/lang - ভাষার তথ্য
/status - বট স্ট্যাটাস

যেকোনো ভাষায় আপনার প্রশ্ন বা অনুরোধ টাইপ করুন!"""
            },
            
            'help': {
                'en': """🔧 *Bot Commands & Usage*

*Code Generation:*
• `/code <description>` - Generate any code
• `/app <app idea>` - Create mobile/desktop app code
• `/web <website idea>` - Create website code

*Question Answering:*
• `/ask <question>` - Ask any question
• Just type your question directly

*Other Commands:*
• `/lang` - Language information
• `/status` - Check bot status
• `/help` - Show this help

*Examples:*
• `/code create a calculator in python`
• `/app todo list app in react native`
• `/web responsive portfolio website`
• `/ask what is machine learning?`

*Tips:*
• Be specific in your requests
• You can mix Bengali and English
• The bot understands context
• Free tier limits apply""",
                
                'bn': """🔧 *বট কমান্ড ও ব্যবহার*

*কোড তৈরি:*
• `/code <বর্ণনা>` - যেকোনো কোড তৈরি করুন
• `/app <অ্যাপ আইডিয়া>` - মোবাইল/ডেস্কটপ অ্যাপ কোড
• `/web <ওয়েবসাইট আইডিয়া>` - ওয়েবসাইট কোড তৈরি

*প্রশ্নের উত্তর:*
• `/ask <প্রশ্ন>` - যেকোনো প্রশ্ন করুন
• সরাসরি প্রশ্ন টাইপ করুন

*অন্যান্য কমান্ড:*
• `/lang` - ভাষার তথ্য
• `/status` - বট স্ট্যাটাস দেখুন
• `/help` - এই সাহায্য দেখুন

*উদাহরণ:*
• `/code পাইথনে ক্যালকুলেটর বানাও`
• `/app রিঅ্যাক্ট নেটিভে টুডু লিস্ট অ্যাপ`
• `/web রেসপন্সিভ পোর্টফোলিও ওয়েবসাইট`
• `/ask মেশিন লার্নিং কি?`

*টিপস:*
• আপনার অনুরোধে সুনির্দিষ্ট হন
• বাংলা ও ইংরেজি মিশিয়ে লিখতে পারেন
• বট প্রসঙ্গ বুঝতে পারে
• ফ্রি টিয়ার সীমা প্রযোজ্য"""
            },
            
            'code_usage': {
                'en': "📝 Usage: `/code <your code request>`\n\nExample: `/code create a python function to sort a list`",
                'bn': "📝 ব্যবহার: `/code <আপনার কোড অনুরোধ>`\n\nউদাহরণ: `/code পাইথনে লিস্ট সর্ট করার ফাংশন বানাও`"
            },
            
            'app_usage': {
                'en': "📱 Usage: `/app <your app idea>`\n\nExample: `/app create a todo list app in React Native`",
                'bn': "📱 ব্যবহার: `/app <আপনার অ্যাপ আইডিয়া>`\n\nউদাহরণ: `/app রিঅ্যাক্ট নেটিভে টুডু লিস্ট অ্যাপ বানাও`"
            },
            
            'web_usage': {
                'en': "🌐 Usage: `/web <your website idea>`\n\nExample: `/web create a responsive portfolio website`",
                'bn': "🌐 ব্যবহার: `/web <আপনার ওয়েবসাইট আইডিয়া>`\n\nউদাহরণ: `/web রেসপন্সিভ পোর্টফোলিও ওয়েবসাইট বানাও`"
            },
            
            'ask_usage': {
                'en': "❓ Usage: `/ask <your question>`\n\nExample: `/ask what is artificial intelligence?`",
                'bn': "❓ ব্যবহার: `/ask <আপনার প্রশ্ন>`\n\nউদাহরণ: `/ask কৃত্রিম বুদ্ধিমত্তা কি?`"
            },
            
            'language_info': {
                'en': """🌐 *Language Support*

*Supported Languages:*
• English
• বাংলা (Bengali)

*Features:*
• Automatic language detection
• Mixed language support
• Context-aware responses
• Cultural adaptation

*Tips:*
• You can mix Bengali and English in the same message
• The bot will respond in the appropriate language
• Technical terms are explained in both languages""",
                
                'bn': """🌐 *ভাষা সাপোর্ট*

*সমর্থিত ভাষা:*
• English
• বাংলা

*বৈশিষ্ট্য:*
• স্বয়ংক্রিয় ভাষা শনাক্তকরণ
• মিশ্র ভাষা সাপোর্ট
• প্রসঙ্গ-সচেতন উত্তর
• সাংস্কৃতিক অভিযোজন

*টিপস:*
• একই বার্তায় বাংলা ও ইংরেজি মিশিয়ে লিখতে পারেন
• বট উপযুক্ত ভাষায় উত্তর দেবে
• প্রযুক্তিগত শব্দ দুই ভাষায় ব্যাখ্যা করা হয়"""
            },
            
            'status': {
                'en': """✅ *Bot Status*

🤖 *AI Model:* Google Gemini 2.5 Flash
🌐 *Languages:* English, Bengali
🔧 *Features:* Code Generation, Q&A, App Development
⚡ *Status:* Online and Ready
🆓 *Tier:* Free (Rate Limited)
🔒 *Security:* End-to-end processing
👨‍💻 *Created by:* Rafsan Maruf

*Capabilities:*
• Multi-language code generation
• Advanced question answering
• App and website development
• Technical problem solving""",
                
                'bn': """✅ *বট স্ট্যাটাস*

🤖 *AI মডেল:* Google Gemini 2.5 Flash
🌐 *ভাষা:* ইংরেজি, বাংলা
🔧 *বৈশিষ্ট্য:* কোড তৈরি, প্রশ্নোত্তর, অ্যাপ ডেভেলপমেন্ট
⚡ *স্ট্যাটাস:* অনলাইন এবং প্রস্তুত
🆓 *টিয়ার:* ফ্রি (রেট লিমিটেড)
🔒 *নিরাপত্তা:* এন্ড-টু-এন্ড প্রসেসিং
👨‍💻 *তৈরি করেছেন:* Rafsan Maruf

*সক্ষমতা:*
• বহুভাষিক কোড তৈরি
• উন্নত প্রশ্নোত্তর
• অ্যাপ এবং ওয়েবসাইট ডেভেলপমেন্ত
• প্রযুক্তিগত সমস্যা সমাধান"""
            },
            
            'rate_limit': {
                'en': "⏰ You're sending requests too quickly. Please wait a moment and try again.",
                'bn': "⏰ আপনি খুব তাড়াতাড়ি অনুরোধ পাঠাচ্ছেন। একটু অপেক্ষা করে আবার চেষ্টা করুন।"
            },
            
            'error': {
                'en': "❌ Sorry, there was an error processing your request. Please try again later.",
                'bn': "❌ দুঃখিত, আপনার অনুরোধ প্রক্রিয়া করতে ত্রুটি হয়েছে। পরে আবার চেষ্টা করুন।"
            }
        }
    
    def detect_user_language(self, user_lang_code: Optional[str]) -> str:
        """Detect user language from Telegram language code"""
        if user_lang_code and user_lang_code.startswith('bn'):
            return 'bn'
        return 'en'
    
    def detect_message_language(self, text: str) -> str:
        """Detect language of a message"""
        if self.bengali_pattern.search(text):
            return 'bn'
        return 'en'
    
    def is_code_request(self, text: str) -> bool:
        """Check if the message is a code-related request"""
        text_lower = text.lower()
        
        # Programming patterns that strongly indicate code requests
        programming_patterns = [
            'def ', 'function ', 'class ', 'import ', 'from ', 'return ',
            'if(', 'else:', 'for(', 'while(', 'try:', 'except:', 'with ',
            '{', '}', '()', '[]', '==', '!=', '&&', '||', '//', '/**',
            '<html>', '<div>', '<script>', 'public class', 'private ',
            'const ', 'let ', 'var ', 'async ', 'await ', 'promise'
        ]
        
        # First check for clear programming patterns
        for pattern in programming_patterns:
            if pattern in text_lower:
                return True
        
        # Check English keywords
        for keyword in self.code_keywords['en']:
            if keyword in text_lower:
                return True
        
        # Check Bengali keywords
        for keyword in self.code_keywords['bn']:
            if keyword in text:
                return True
        
        # Special cases - questions about bot creator/developer should NOT be code requests
        creator_questions = [
            'কে তৈরি', 'কে বানিয়েছে', 'কে ডেভেলপ', 'কে বানায়', 'তৈরি করেছে', 'তৈরি করছে',
            'who created', 'who developed', 'who made', 'who built', 'created by', 'developed by'
        ]
        
        for creator_q in creator_questions:
            if creator_q in text_lower or creator_q in text:
                return False
        
        # Special cases - if asking about concepts but not requesting code
        non_code_questions = [
            'what is', 'কি', 'কাকে বলে', 'explain', 'বুঝিয়ে', 'meaning',
            'definition', 'সংজ্ঞা', 'why', 'কেন', 'how does', 'কিভাবে কাজ করে',
            'difference', 'পার্থক্য', 'compare', 'তুলনা'
        ]
        
        # If it's a concept question without clear code request, treat as general question
        for question_type in non_code_questions:
            if question_type in text_lower or question_type in text:
                # But if it also has strong programming keywords, still consider it code
                strong_code_keywords = ['function', 'algorithm', 'program', 'script', 'ফাংশন', 'অ্যালগরিদম']
                has_strong_code = any(keyword in text_lower or keyword in text for keyword in strong_code_keywords)
                if not has_strong_code:
                    return False
        
        return False
    
    def get_message(self, key: str, language: str) -> str:
        """Get predefined message in specified language"""
        if key in self.messages and language in self.messages[key]:
            return self.messages[key][language]
        
        # Fallback to English if Bengali is not available
        if key in self.messages and 'en' in self.messages[key]:
            return self.messages[key]['en']
        
        return "Message not found"
