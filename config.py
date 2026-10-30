import os
from dotenv import load_dotenv

load_dotenv()

# مفاتيح التشغيل الأساسية (تُقرأ بأمان من Variables and secrets في Hugging Face)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

# مفاتيح المشروع الأول: مسابقة Nebius x NVIDIA Global AI Hackathon ($50,000)
# عنوان النهاية الرسمي لـ Nebius Token Factory (متوافق مع بروتوكول OpenAI)
NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY", "").strip()
NEBIUS_BASE_URL = os.getenv(
    "NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1"
).strip()

# مفتاح Tavily API (للمنافسة على جائزة Best Use of Tavily الإضافية بقيمة 3,000$)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "").strip()

# مفتاح Meta Model API (محفوظ في الوضع القياسي المحمي Standard Mode لمنع تدريب النماذج على الكود)
META_MODEL_API_KEY = os.getenv("META_MODEL_API_KEY", "").strip()
META_BASE_URL = os.getenv("META_BASE_URL", "https://api.meta.ai/v1").strip()

# مسارات ملفات Google APIs (اختياري)
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
GOOGLE_TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")

# قاعدة البيانات المحلية للذاكرة المستمرة والمهارات المسجلة
DB_PATH = os.getenv("DB_PATH", "agent_memory.db")
SKILLS_DIR = os.getenv("SKILLS_DIR", "recorded_skills")
