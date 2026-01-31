class GraphService:
    def __init__(self, ai, kb, supabase):
        self.ai = ai
        self.kb = kb
        self.supabase = supabase

    def reply_graph(self, email, tone='neutral'):
        # 1) retrieve KB chunks relevant to the email body
        chunks = self.kb.search(email.get('body',''), k=5)
        # 2) generate KB-grounded reply
        return self.ai.generate_kb_reply(email, chunks, tone)
