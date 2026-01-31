from groq import Groq
from app.config import settings
import json

# Initialize client only if API key is available
client = None
if settings.GROQ_API_KEY and settings.GROQ_API_KEY != 'your-groq-api-key':
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
    except Exception as e:
        print(f"Warning: Groq client initialization failed: {e}")

class AIService:
    def embed(self, text: str):
        # For embeddings, we'll use a simple hash-based approach since Groq doesn't have embeddings
        # In production, you'd use a separate embedding service like sentence-transformers
        import hashlib
        hash_obj = hashlib.sha256(text.encode())
        # Create a 1536-dimensional embedding from the hash
        hash_bytes = hash_obj.digest()
        embedding = []
        for i in range(1536):
            byte_val = hash_bytes[i % len(hash_bytes)]
            embedding.append((byte_val - 128) / 128.0)
        return embedding

    def summarize(self, email):
        if not client:
            return f"Mock summary: {email.get('subject', 'Email')} - {email.get('body', '')[:100]}"
        prompt = f"Summarize this email:\n{email.get('body','')}"
        message = client.messages.create(
            model=settings.GROQ_CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return message.choices[0].message.content.strip()

    def generate_kb_reply(self, email, kb_chunks, tone="neutral"):
        if not client:
            return f"Mock {tone} reply to: {email.get('subject', '')}"
        context = "\n\n".join(kb_chunks)
        prompt = f"""You are an AI Email Assistant. You MUST answer based ONLY on the knowledge below.

EMAIL:
Subject: {email.get('subject','')}
Body: {email.get('body','')}

KNOWLEDGE:
{context}

Write a {tone} reply grounded ONLY in the knowledge base. If the KB doesn't contain necessary info, state that you don't know.
"""
        message = client.messages.create(
            model=settings.GROQ_CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return message.choices[0].message.content.strip()

    def compose(self, instruction):
        if not client:
            return f"Mock Subject: {instruction}", f"Mock body for: {instruction}"
        prompt = f"Write an email: {instruction}. Respond in JSON with keys 'subject' and 'body'."
        message = client.messages.create(
            model=settings.GROQ_CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=350
        )
        text = message.choices[0].message.content.strip()
        try:
            data = json.loads(text)
            return data.get("subject",""), data.get("body","")
        except Exception:
            # fallback
            lines = text.splitlines()
            subject = lines[0] if lines else "Generated Subject"
            body = "\n".join(lines[1:]) if len(lines)>1 else text
            return subject, body
