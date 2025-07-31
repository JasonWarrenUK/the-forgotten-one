from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import uuid
from agent import create_deity, system_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Agent Workshop",
    description="A simple AI agent API built with LangChain and FastAPI",
    version="1.0.0"
)

# Add CORS middleware for web frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent once at startup
try:
    deity = create_deity()
    logger.info("DEITY AWOKEN")
except Exception as e:
    logger.error(f"Failed to initialize agent: {e}")
    agent = None

class Query(BaseModel):
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello, how are you?"
            }
        }

class ChatResponse(BaseModel):
    reply: str
    status: str = "success"

@app.get("/")
async def root():
    return {
        "message": "The ancient one stirs.",
        "endpoints": {
            "POST /petition": "Send a petition to the ancient one",
            "GET /orrery": "Check whether the celestial orbs are in alignment so that you may petition the ancient one",
            "GET /tome": "Peruse the tomes of forbidden lore in pursuit of the ancient one's will"
        },
        "version": "42352419865982691824941964.0.0"
    }

@app.post("/petition", response_model=ChatResponse)
async def chat(query: Query):
    if not deity:
        raise HTTPException(status_code=503, detail="THE DEITY SLUMBERS")
    
    try:
        logger.info(f"THE DEITY HEARS THE PETITION OF: {query.message}")
        
        # LangGraph agent uses invoke with messages format, including system prompt
        response = deity.invoke({"messages": [
            ("system", system_prompt()),
            ("human", query.message)
        ]})
        
        # Extract the final AI message from the response
        final_message = response.get("messages", [])[-1]
        reply = final_message.content if hasattr(final_message, 'content') else str(final_message)
        
        logger.info(f"SAYETH THY LORD... {reply}")
        return ChatResponse(reply=reply)
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while processing your request. Please try again."
        )

@app.get("/orrery")
async def health():
    deity_status = "ok" if deity else "unavailable"
    return {
        "status": "ok",
        "deity_status": deity_status,
        "version": "1.0.0"
    }
