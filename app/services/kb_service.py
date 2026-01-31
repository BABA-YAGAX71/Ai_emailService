from app.config import settings
from app.services.ai_service import AIService

class KBService:
    def __init__(self):
        if not settings.PINECONE_API_KEY:
            raise RuntimeError('PINECONE_API_KEY not set in env')
        try:
            from pinecone import Pinecone
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.index_name = settings.PINECONE_KB_INDEX
            self.index = self.pc.Index(self.index_name)
        except Exception as e:
            print(f"Warning: Pinecone initialization failed: {e}")
            self.index = None
        self.ai = AIService()

    def upsert_document(self, doc_id: str, text: str, metadata: dict = None):
        if not self.index:
            raise RuntimeError(f'Index {self.index_name} not found')
        vec = self.ai.embed(text)
        meta = metadata or {}
        meta.update({'text': text})
        self.index.upsert([(doc_id, vec, meta)])

    def search(self, query, k=5):
        if not self.index:
            raise RuntimeError(f'Index {self.index_name} not found')
        vector = self.ai.embed(query)
        res = self.index.query(vector=vector, top_k=k, include_metadata=True)
        chunks = []
        for m in res.get('matches', []):
            meta = m.get('metadata',{})
            chunks.append(meta.get('text',''))
        return chunks
