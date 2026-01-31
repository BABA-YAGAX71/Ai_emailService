# Placeholder for LangGraph reply graph (RAG)
def reply_graph(email, ai, kb, tone='neutral'):
    chunks = kb.search(email.get('body',''), k=5)
    return ai.generate_kb_reply(email, chunks, tone)
