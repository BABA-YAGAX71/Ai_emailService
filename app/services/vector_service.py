from app.config import settings
from app.services.ai_service import AIService

class VectorService:
    def __init__(self):
        if not settings.PINECONE_API_KEY:
            raise RuntimeError('PINECONE_API_KEY not set in env')
        try:
            from pinecone import Pinecone
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.index_name = settings.PINECONE_EMAIL_INDEX
            self.index = self.pc.Index(self.index_name)
        except Exception as e:
            print(f"Warning: Pinecone initialization failed: {e}")
            self.index = None
        self.ai = AIService()

    def search(self, text, k=5):
        if not self.index:
            raise RuntimeError(f'Index {self.index_name} not found')
        vector = self.ai.embed(text)
        res = self.index.query(vector=vector, top_k=k, include_metadata=True)
        # normalize results
        matches = []
        for m in res.get('matches', []):
            matches.append({'id': m['id'], 'score': m['score'], 'metadata': m.get('metadata')})
        return matches
