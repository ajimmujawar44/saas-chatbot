from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini_service import generate_chat_response
import markdown
app = FastAPI(
    title="GenAI Chatbot SaaS API created by AZIM MUJAWAR",
    description="FastAPI Backend for Gemini Integration",
    version="1.0.0"
)

# Enable CORS so your frontend can connect seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to your specific Vercel frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what the incoming data from the frontend should look like
class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(payload: ChatRequest):
    user_message = payload.message.strip()
    
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    # Call our Gemini service to fetch the AI generation
    bot_reply = generate_chat_response(user_message)

    html_reply = markdown.markdown(bot_reply, extensions=['extra'])
    
    return {"reply": html_reply}

# Vercel relies on this root route mapping to understand serverless lifespan hooks
@app.get("/")
async def root():
    return {"status": "healthy", "service": "FastAPI Chatbot Backend"}