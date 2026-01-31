from supabase import create_client
from app.config import settings

class SupabaseService:
    def __init__(self):
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise RuntimeError('Supabase not configured in env')
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    def get_email(self, email_id: str):
        res = self.client.table('emails').select('*').eq('id', email_id).limit(1).execute()
        data = res.data
        return data[0] if data and len(data)>0 else None

    def list_all_emails(self):
        res = self.client.table('emails').select('*').execute()
        return res.data or []
