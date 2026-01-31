import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_CHAT_MODEL = os.getenv('GROQ_CHAT_MODEL', 'mixtral-8x7b-32768')

    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_ENV = os.getenv('PINECONE_ENV')
    PINECONE_EMAIL_INDEX = os.getenv('PINECONE_EMAIL_INDEX', 'email-index')
    PINECONE_KB_INDEX = os.getenv('PINECONE_KB_INDEX', 'kb-index')

    EMBED_DIM = int(os.getenv('EMBED_DIM', '1536'))

settings = Settings()
