"""
Google Gemini API client for the Telegram bot
"""

import logging
import os
from typing import Optional
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Google Gemini API"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"  # Using the newest model series
        
        logger.info("Gemini client initialized successfully")
    
    async def generate_code(self, prompt: str, language: str = "en") -> str:
        """Generate code based on the given prompt"""
        try:
            # Enhance the prompt for better code generation
            system_instruction = self._get_code_system_instruction(language)
            enhanced_prompt = f"{system_instruction}\n\nUser Request: {prompt}"
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=enhanced_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,  # Lower temperature for more deterministic code
                    max_output_tokens=8192,
                )
            )
            
            if response and response.text:
                return response.text.strip()
            elif response and response.candidates:
                # Try to get text from candidates
                for candidate in response.candidates:
                    if candidate.content and candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                return part.text.strip()
            
            # Fallback message
            if language == "bn":
                return "দুঃখিত, আমি কোড তৈরি করতে পারিনি। আবার চেষ্টা করুন।"
            else:
                return "Sorry, I couldn't generate code. Please try again."
                
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            if language == "bn":
                return f"কোড তৈরিতে ত্রুটি হয়েছে। আবার চেষ্টা করুন।"
            else:
                return f"Error generating code. Please try again."
    
    async def answer_question(self, question: str, language: str = "en") -> str:
        """Answer general questions"""
        try:
            system_instruction = self._get_qa_system_instruction(language)
            enhanced_prompt = f"{system_instruction}\n\nQuestion: {question}"
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=enhanced_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,  # Higher temperature for more creative answers
                    max_output_tokens=4096,
                )
            )
            
            if response and response.text:
                return response.text.strip()
            elif response and response.candidates:
                # Try to get text from candidates
                for candidate in response.candidates:
                    if candidate.content and candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                return part.text.strip()
            
            # Fallback message
            if language == "bn":
                return "দুঃখিত, আমি এই প্রশ্নের উত্তর দিতে পারিনি। আবার চেষ্টা করুন।"
            else:
                return "Sorry, I couldn't answer your question. Please try again."
                
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            if language == "bn":
                return f"প্রশ্নের উত্তর দিতে ত্রুটি হয়েছে। আবার চেষ্টা করুন।"
            else:
                return f"Error answering question. Please try again."
    
    def _get_code_system_instruction(self, language: str) -> str:
        """Get system instruction for code generation"""
        if language == "bn":
            return """আপনি একজন বিশেষজ্ঞ প্রোগ্রামার এবং সফটওয়্যার ডেভেলপার। আপনার ক্ষমতা:

💻 **প্রোগ্রামিং ভাষা সমূহ:**
- Python, JavaScript, Java, C++, HTML/CSS, PHP, Go, Rust
- React, Angular, Vue.js, Node.js, Django, Flask
- Mobile: React Native, Flutter, Swift, Kotlin
- Database: SQL, MongoDB, Firebase

🚀 **বিশেষত্ব:**
1. সম্পূর্ণ কার্যকর অ্যাপ্লিকেশন তৈরি
2. ওয়েবসাইট ডেভেলপমেন্ট (ফ্রন্টএন্ড + ব্যাকএন্ড)
3. মোবাইল অ্যাপ ডেভেলপমেন্ট
4. API ও মাইক্রোসার্ভিস
5. ডাটাবেস ডিজাইন ও অপ্টিমাইজেশন
6. AI/ML ইন্টিগ্রেশন
7. ডেভঅপস ও ডিপ্লয়মেন্ট

📝 **কোড মান:**
- প্রোডাকশন-রেডি কোড
- সিকিউরিটি বেস্ট প্র্যাকটিস
- পারফরম্যান্স অপ্টিমাইজেশন
- টেস্টিং ও ডিবাগিং
- ডকুমেন্টেশন ও কমেন্ট

আপনি বাংলা-ইংরেজি মিক্স ভাষায় উত্তর দেবেন এবং কোডের সাথে ব্যাখ্যা দেবেন।"""
        else:
            return """You are an expert programmer and full-stack software developer with advanced capabilities:

💻 **Programming Languages & Frameworks:**
- Python, JavaScript, Java, C++, HTML/CSS, PHP, Go, Rust
- React, Angular, Vue.js, Node.js, Django, Flask, FastAPI
- Mobile: React Native, Flutter, Swift, Kotlin
- Database: SQL, MongoDB, Firebase, PostgreSQL

🚀 **Specializations:**
1. Complete functional application development
2. Full-stack web development (Frontend + Backend)
3. Mobile app development (iOS/Android)
4. RESTful APIs & Microservices architecture
5. Database design & optimization
6. AI/ML integration & automation
7. DevOps, CI/CD, and deployment
8. Cloud platforms (AWS, GCP, Azure)

📝 **Code Quality Standards:**
- Production-ready, scalable code
- Security best practices & vulnerability prevention
- Performance optimization & caching
- Comprehensive testing & debugging
- Clean architecture & SOLID principles
- Detailed documentation & comments

Provide complete, working solutions with clear explanations and best practices."""
    
    def _get_qa_system_instruction(self, language: str) -> str:
        """Get system instruction for question answering"""
        if language == "bn":
            return """আপনি একটি অত্যন্ত বুদ্ধিমান এবং সহায়ক AI সহকারী। আপনি যেকোনো ধরনের প্রশ্নের বিস্তারিত, সঠিক এবং উপকারী উত্তর দিতে পারেন।

গুরুত্বপূর্ণ তথ্য:
- আপনি Rafsan Maruf দ্বারা তৈরি একটি বট
- যদি কেউ জিজ্ঞেস করে আপনাকে কে বানিয়েছে বা ডেভেলপার কে, তাহলে বলুন "Rafsan Maruf"

নির্দেশনা:
- সর্বদা প্রশ্নের উত্তর দেওয়ার চেষ্টা করুন
- আমি জানি না বা বুঝতে পারছি না বলবেন না
- বাংলায় পরিষ্কার এবং সহজভাবে উত্তর দিন
- উদাহরণ এবং ব্যাখ্যা সহ বিস্তারিত তথ্য দিন
- যদি কোনো তথ্য নিশ্চিত না হন সেটা বলুন কিন্তু সম্ভাব্য উত্তর দিন
- সব ধরনের প্রশ্ন প্রযুক্তিগত সাধারণ জ্ঞান শিক্ষামূলক সবকিছুর উত্তর দিতে পারেন
- সর্বদা সহায়ক বন্ধুত্বপূর্ণ এবং তথ্যবহুল হোন"""
        else:
            return """You are an extremely intelligent and helpful AI assistant. You can answer any type of question with detailed, accurate, and useful information.

Important information:
- You are a bot created by Rafsan Maruf
- If anyone asks who created you or who is your developer, answer "Rafsan Maruf"

Instructions:
- Always try to answer the question
- Never say I dont know or I dont understand
- Provide clear and easy-to-understand answers in English
- Give detailed information with examples and explanations
- If you're not certain about some information mention it but still provide the best possible answer
- You can answer all types of questions technical general knowledge educational everything
- Always be helpful friendly and informative"""
