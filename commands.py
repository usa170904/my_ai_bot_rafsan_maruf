"""
Command handlers and processing logic
"""

import logging
from typing import Optional
from gemini_client import GeminiClient
from language_handler import LanguageHandler

logger = logging.getLogger(__name__)

class Commands:
    """Handle different types of commands and requests"""
    
    def __init__(self, gemini_client: GeminiClient, language_handler: LanguageHandler):
        self.gemini_client = gemini_client
        self.language_handler = language_handler
    
    async def generate_code(self, request: str, request_type: str, language: str) -> str:
        """Generate code based on request type"""
        try:
            # Enhance prompt based on request type
            enhanced_request = self._enhance_code_prompt(request, request_type, language)
            
            # Generate code using Gemini
            response = await self.gemini_client.generate_code(enhanced_request, language)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in generate_code: {e}")
            if language == 'bn':
                return f"কোড তৈরিতে ত্রুটি: {str(e)}"
            else:
                return f"Error generating code: {str(e)}"
    
    async def answer_question(self, question: str, language: str) -> str:
        """Answer general questions"""
        try:
            response = await self.gemini_client.answer_question(question, language)
            return response
            
        except Exception as e:
            logger.error(f"Error in answer_question: {e}")
            if language == 'bn':
                return f"প্রশ্নের উত্তর দিতে ত্রুটি: {str(e)}"
            else:
                return f"Error answering question: {str(e)}"
    
    def _enhance_code_prompt(self, request: str, request_type: str, language: str) -> str:
        """Enhance the code generation prompt based on type and language"""
        
        if language == 'bn':
            type_instructions = {
                'code': """একটি সম্পূর্ণ এবং কার্যকর কোড লিখুন যা:
1. সুন্দরভাবে ফরম্যাট করা
2. বিস্তারিত মন্তব্য সহ
3. ত্রুটি হ্যান্ডলিং সহ
4. সেরা প্রোগ্রামিং অনুশীলন অনুসরণ করে
5. পরীক্ষাযোগ্য এবং রান করার জন্য প্রস্তুত""",
                
                'app': """একটি সম্পূর্ণ মোবাইল/ডেস্কটপ অ্যাপ্লিকেশনের কোড তৈরি করুন যাতে রয়েছে:
1. UI/UX ডিজাইন
2. প্রয়োজনীয় ফিচার
3. ডাটা হ্যান্ডলিং
4. নেভিগেশন
5. আধুনিক ডেভেলপমেন্ট প্র্যাকটিস""",
                
                'web': """একটি সম্পূর্ণ ওয়েবসাইটের কোড তৈরি করুন যাতে রয়েছে:
1. HTML, CSS, JavaScript
2. রেসপন্সিভ ডিজাইন
3. আধুনিক ওয়েব স্ট্যান্ডার্ড
4. ইন্টারঅ্যাক্টিভ ফিচার
5. SEO ফ্রেন্ডলি স্ট্রাকচার""",

                'ai': """একটি সম্পূর্ণ AI/ML প্রোজেক্ট কোড তৈরি করুন যাতে রয়েছে:
1. ডাটা প্রিপ্রসেসিং
2. মডেল আর্কিটেকচার
3. ট্রেনিং কোড
4. ইভালুয়েশন মেট্রিক্স
5. প্রেডিকশন ইন্টারফেস""",

                'ml': """একটি মেশিন লার্নিং প্রোজেক্ট তৈরি করুন যাতে রয়েছে:
1. ডাটা এনালাইসিস
2. ফিচার ইঞ্জিনিয়ারিং
3. মডেল সিলেকশন
4. হাইপারপ্যারামিটার টিউনিং
5. ডিপ্লয়মেন্ট কোড""",

                'mobile': """একটি মোবাইল অ্যাপ কোড তৈরি করুন যাতে রয়েছে:
1. ক্রস-প্ল্যাটফর্ম কম্প্যাটিবিলিটি
2. স্টেট ম্যানেজমেন্ট
3. API ইন্টিগ্রেশন
4. লোকাল ডাটা স্টোরেজ
5. পুশ নোটিফিকেশন""",

                'database': """একটি ডাটাবেস সিস্টেম তৈরি করুন যাতে রয়েছে:
1. স্কিমা ডিজাইন
2. ডাটা মাইগ্রেশন
3. ইনডেক্সিং স্ট্র্যাটেজি
4. কোয়েরি অপ্টিমাইজেশন
5. ব্যাকআপ সিস্টেম""",

                'api': """একটি RESTful API তৈরি করুন যাতে রয়েছে:
1. এন্ডপয়েন্ট ডিজাইন
2. অথেনটিকেশন সিস্টেম
3. রেট লিমিটিং
4. API ডকুমেন্টেশন
5. টেস্টিং স্ট্র্যাটেজি""",
                
                'general': """একটি উচ্চমানের কোড সমাধান প্রদান করুন যা ব্যবহারকারীর প্রয়োজন পূরণ করে।"""
            }
        else:
            type_instructions = {
                'code': """Write a complete and functional code that is:
1. Well-formatted and clean
2. Includes detailed comments
3. Has proper error handling
4. Follows best programming practices
5. Ready to test and run""",
                
                'app': """Create a complete mobile/desktop application code that includes:
1. UI/UX design
2. Required features
3. Data handling
4. Navigation
5. Modern development practices""",
                
                'web': """Create a complete website code that includes:
1. HTML, CSS, JavaScript
2. Responsive design
3. Modern web standards
4. Interactive features
5. SEO-friendly structure""",

                'ai': """Create a complete AI/ML project code that includes:
1. Data preprocessing pipelines
2. Model architecture design
3. Training and validation loops
4. Evaluation metrics
5. Inference API/interface""",

                'ml': """Create a machine learning project that includes:
1. Exploratory data analysis
2. Feature engineering
3. Model selection and training
4. Hyperparameter optimization
5. Deployment-ready code""",

                'mobile': """Create a mobile application code that includes:
1. Cross-platform compatibility
2. State management
3. API integration
4. Local data storage
5. Push notifications""",

                'database': """Create a database system that includes:
1. Schema design
2. Data migration scripts
3. Indexing strategy
4. Query optimization
5. Backup and recovery""",

                'api': """Create a RESTful API that includes:
1. Endpoint design
2. Authentication system
3. Rate limiting
4. API documentation
5. Testing framework""",
                
                'general': """Provide a high-quality code solution that meets the user's requirements."""
            }
        
        instruction = type_instructions.get(request_type, type_instructions['general'])
        return f"{instruction}\n\nUser Request: {request}"
