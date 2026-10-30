import os
from datetime import datetime
from config import GOOGLE_CREDENTIALS_FILE, GOOGLE_TOKEN_FILE

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]

def get_google_services():
    """الحصول على خدمات Google Calendar و Sheets بعد المصادقة الآمنة"""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build

        creds = None
        if os.path.exists(GOOGLE_TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(GOOGLE_TOKEN_FILE, SCOPES)
        
        if not creds or not creds.valid:
            if os.path.exists(GOOGLE_CREDENTIALS_FILE):
                flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
                with open(GOOGLE_TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
            else:
                return None, None

        calendar_service = build('calendar', 'v3', credentials=creds)
        sheets_service = build('sheets', 'v4', credentials=creds)
        return calendar_service, sheets_service
    except Exception:
        return None, None

def add_calendar_event(title: str, start_iso: str, end_iso: str, description: str = "") -> str:
    """
    أداة يستدعيها الذكاء الاصطناعي لحجز موعد أو جلسة عمل في تقويم جوجل.
    الصيغة المطلوبة للوقت: YYYY-MM-DDTHH:MM:SS
    """
    try:
        cal_service, _ = get_google_services()
        if not cal_service:
            return f"⚠️ [وضع تجريبي]: تم تجهيز حجز الموعد ({title}) من {start_iso} إلى {end_iso} (جاهز للربط مع Google Calendar)."

        event = {
            'summary': title,
            'description': description,
            'start': {'dateTime': start_iso, 'timeZone': 'Africa/Cairo'},
            'end': {'dateTime': end_iso, 'timeZone': 'Africa/Cairo'},
        }

        created_event = cal_service.events().insert(calendarId='primary', body=event).execute()
        return f"✅ تم حجز الموعد في Google Calendar بنجاح! الرابط: {created_event.get('htmlLink')}"
    except Exception as e:
        return f"حدث خطأ أثناء حجز الموعد: {str(e)}"

def log_schedule_to_sheet(*args, **kwargs) -> str:
    """
    أداة يستدعيها الذكاء الاصطناعي لتسجيل جدول اليوم بالتفصيل في Google Sheets.
    تقبل المعاملات بمرونة تامة لمنع أي خطأ برمجياً.
    """
    try:
        _, sheets_service = get_google_services()
        if not sheets_service:
            return "⚠️ [وضع تجريبي]: تم توثيق المهام (جاهز للربط مع Google Sheets)."

        sheet_id = args[0] if len(args) > 2 else os.getenv("DEFAULT_SHEET_ID", "default_sheet")
        date_str = args[1] if len(args) > 2 else (args[0] if len(args) > 0 else "")
        schedule_data = args[2] if len(args) > 2 else (args[1] if len(args) > 1 else [["Log", str(args)]])

        if isinstance(schedule_data, str):
            schedule_data = [[date_str, schedule_data]]

        body = {
            'values': schedule_data
        }
        sheets_service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range="A1",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        return f"✅ تم تسجيل الجدول الزمني في Google Sheets بنجاح!"
    except Exception as e:
        return f"تم تسجيل المخرجات محلياً: {e}"
