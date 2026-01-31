from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Lazy initialization of services
supabase = None
kb = None
ai = None
graph = None

def _init_services():
    global supabase, kb, ai, graph
    if supabase is None:
        from app.services.supabase_service import SupabaseService
        from app.services.kb_service import KBService
        from app.services.ai_service import AIService
        from app.services.graph_service import GraphService
        supabase = SupabaseService()
        kb = KBService()
        ai = AIService()
        graph = GraphService(ai=ai, kb=kb, supabase=supabase)

class SummarizeRequest(BaseModel):
    email_id: str

class ReplyRequest(BaseModel):
    email_id: str
    tone: str = "neutral"

class ComposeRequest(BaseModel):
    prompt: str

class MockEmailRequest(BaseModel):
    subject: str = "Test Email"
    body: str = "This is a test email body"

@router.post("/summarize")
def summarize(req: SummarizeRequest):
    try:
        _init_services()
        email = supabase.get_email(req.email_id)
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        return {"summary": ai.summarize(email)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/reply")
def reply(req: ReplyRequest):
    try:
        _init_services()
        email = supabase.get_email(req.email_id)
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        reply_text = graph.reply_graph(email, req.tone)
        return {"reply": reply_text}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/compose")
def compose(req: ComposeRequest):
    try:
        _init_services()
        subject, body = ai.compose(req.prompt)
        return {"subject": subject, "body": body}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Mock/Test endpoints - no external dependencies
@router.post("/compose-mock")
def compose_mock(req: ComposeRequest):
    """Test endpoint - generates email without Groq (uses mock data)"""
    return {
        "subject": f"Re: {req.prompt}",
        "body": f"This is a mock reply to: {req.prompt}"
    }

@router.post("/summarize-mock")
def summarize_mock(req: MockEmailRequest):
    """Test endpoint - summarizes email without Groq (uses mock data)"""
    return {
        "summary": f"Mock summary of email with subject '{req.subject}': {req.body[:50]}..."
    }

@router.post("/reply-mock")
def reply_mock(req: MockEmailRequest):
    """Test endpoint - generates reply without Groq (uses mock data)"""
    return {
        "reply": f"Thank you for your email with subject '{req.subject}'. We will respond shortly."
    }
