from fastapi import APIRouter  
from pydantic import BaseModel  
  
router = APIRouter()  
  
class ChatRequest(BaseModel):  
    user_input: str  
    history: list = []  
  
@router.post("/ask")  
async def chat(request: ChatRequest):  
    # This is a simulated LLM response
    return {
        "response": f"This is a general Q&A mode response. You said: {request.user_input}"
    }  
