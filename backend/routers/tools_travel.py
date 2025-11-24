from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
import json
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

router = APIRouter()

class TravelQARequest(BaseModel):
    user_input: str  # User's travel-related question
    text: str = ""  # Alternative field
    question: str = ""  # Original field
    history: list = []  # Chat history for context

class TravelQAResponse(BaseModel):
    answer: str
    confidence: Optional[float] = None
    sources: Optional[list] = None

# Local Knowledge Base for Fallback
KNOWLEDGE_BASE = {
    "beijing": {
        "intro": "Beijing, China's capital, is a blend of ancient history and modern marvels. It's home to 7 UNESCO World Heritage Sites.",
        "attractions": [
            "**The Great Wall (Mutianyu or Badaling)**: A must-visit ancient fortification.",
            "**The Forbidden City**: The imperial palace for 24 emperors.",
            "**Temple of Heaven**: An imperial complex of religious buildings.",
            "**Summer Palace**: A vast ensemble of lakes, gardens, and palaces."
        ],
        "food": "Peking Duck (try Quanjude or Da Dong), Zhajiangmian (noodles with soybean paste), and various dumplings.",
        "transport": "Beijing has an extensive subway system (cheap and efficient). Taxis and Didi (ride-hailing) are also widely available."
    },
    "shanghai": {
        "intro": "Shanghai is China's biggest city and a global financial hub, famous for its Lujiazui skyline and colonial-era Bund.",
        "attractions": [
            "**The Bund**: Famous waterfront area with colonial buildings.",
            "**Yu Garden**: A classical Chinese garden in the Old City.",
            "**Shanghai Tower**: The tallest building in China.",
            "**Disney Resort**: A popular theme park."
        ],
        "food": "Xiao Long Bao (soup dumplings), Shengjian Bao (pan-fried buns), and sweet-savory Shanghainese dishes.",
        "transport": "The Maglev train connects Pudong Airport to the city at 430km/h. The metro system is the world's largest."
    },
    "xian": {
        "intro": "Xi'an is the starting point of the Silk Road and home to the Terracotta Warriors.",
        "attractions": [
            "**Terracotta Warriors**: Thousands of life-size soldiers buried with the first emperor.",
            "**Ancient City Wall**: You can cycle on top of this well-preserved wall.",
            "**Muslim Quarter**: Famous for its street food and vibrant atmosphere.",
            "**Big Wild Goose Pagoda**: A Buddhist pagoda built in 652 AD."
        ],
        "food": "Roujiamo (Chinese hamburger), Biangbiang noodles, and Yangrou Paomo (bread in mutton soup).",
        "transport": "Metro and buses are convenient. It's a major high-speed rail hub."
    },
    "chengdu": {
        "intro": "Chengdu is the capital of Sichuan province, famous for pandas and spicy hotpot.",
        "attractions": [
            "**Giant Panda Breeding Research Base**: See pandas up close.",
            "**Jinli Ancient Street**: Traditional architecture and snacks.",
            "**Leshan Giant Buddha**: A massive stone statue carved into a cliff (short train ride away)."
        ],
        "food": "Sichuan Hotpot (very spicy!), Mapo Tofu, Kung Pao Chicken.",
        "transport": "Two international airports and a growing metro system."
    },
    "guilin": {
        "intro": "Guilin is renowned for its dramatic karst landscape and the Li River.",
        "attractions": [
            "**Li River Cruise**: From Guilin to Yangshuo, offering breathtaking views.",
            "**Elephant Trunk Hill**: The symbol of Guilin.",
            "**Longji Rice Terraces**: Stunning terraced fields."
        ],
        "food": "Guilin Rice Noodles are the local staple.",
        "transport": "Boats to Yangshuo, trains, and buses."
    },
    "hong kong": {
        "intro": "Hong Kong is a vibrant metropolis where East meets West.",
        "attractions": [
            "**Victoria Peak**: Panoramic views of the skyline.",
            "**Star Ferry**: A scenic ride across Victoria Harbour.",
            "**Tian Tan Buddha**: A massive bronze Buddha statue."
        ],
        "food": "Dim Sum, Roast Goose, Egg Tarts, and Milk Tea.",
        "transport": "MTR is world-class. Trams and ferries are iconic."
    },
    "visa": {
        "intro": "Most travelers need a visa for China. However, there are exceptions:",
        "details": [
            "**144-hour Visa-Free Transit**: Available in Beijing, Shanghai, and other major cities for transit passengers from 53 countries.",
            "**Visa-Free Entry**: Citizens of Singapore, Malaysia, Thailand, and some European countries (check latest policy) may enter visa-free for short stays.",
            "**L Visa (Tourist)**: The standard tourist visa requires flight/hotel bookings."
        ]
    },
    "transport": {
        "intro": "Getting around China is generally easy and modern.",
        "details": [
            "**High-Speed Rail (Gaotie)**: Fast, punctual, and connects almost all major cities. Often better than flying for trips under 5 hours.",
            "**Metro**: Available in most large cities. Signs are in English.",
            "**Didi Chuxing**: The Chinese Uber. The app has an English version.",
            "**Flights**: Good for long distances (e.g., Beijing to Hong Kong)."
        ]
    },
    "payment": {
        "intro": "China is a cashless society.",
        "details": [
            "**Alipay & WeChat Pay**: You can now link foreign credit cards to these apps.",
            "**Cash**: Still accepted but less common. Keep small change.",
            "**Credit Cards**: Accepted at major hotels and high-end restaurants, but not at local shops."
        ]
    }
}

def get_mock_response(question: str) -> str:
    """
    Generate a response based on keywords in the question using the local knowledge base.
    """
    question_lower = question.lower()
    
    # Check for specific cities
    for city, data in KNOWLEDGE_BASE.items():
        if city in question_lower and "intro" in data:
            response = f"### 🏙️ Guide to {city.title()}\n\n{data['intro']}\n\n**🔥 Top Attractions:**\n"
            for attr in data['attractions']:
                response += f"- {attr}\n"
            
            if "food" in data:
                response += f"\n**🍜 Food Recommendations:**\n{data['food']}\n"
            
            if "transport" in data:
                response += f"\n**🚇 Transportation:**\n{data['transport']}"
                
            return response

    # Check for topics
    if "visa" in question_lower or "entry" in question_lower:
        data = KNOWLEDGE_BASE["visa"]
        response = f"### 🛂 China Visa Information\n\n{data['intro']}\n\n"
        for detail in data['details']:
            response += f"- {detail}\n"
        return response

    if "transport" in question_lower or "train" in question_lower or "taxi" in question_lower:
        data = KNOWLEDGE_BASE["transport"]
        response = f"### 🚄 Transportation in China\n\n{data['intro']}\n\n"
        for detail in data['details']:
            response += f"- {detail}\n"
        return response

    if "pay" in question_lower or "money" in question_lower or "cash" in question_lower or "card" in question_lower:
        data = KNOWLEDGE_BASE["payment"]
        response = f"### 💳 Payment in China\n\n{data['intro']}\n\n"
        for detail in data['details']:
            response += f"- {detail}\n"
        return response
        
    if "food" in question_lower or "eat" in question_lower:
        return "### 🥢 Chinese Cuisine\n\nChina has 8 major culinary traditions! \n\n- **Sichuan**: Spicy and numbing (Hotpot, Kung Pao Chicken)\n- **Cantonese**: Fresh and mild (Dim Sum, Roast meats)\n- **Jiangsu/Zhejiang**: Sweet and savory (Braised Pork Belly)\n- **Northern**: Salty and wheat-based (Peking Duck, Dumplings)\n\n**Tip:** Don't be afraid to try street food, but look for busy stalls!"

    # General fallback
    return """I can help you plan your trip to China! 🇨🇳

I have detailed information about:
- **Cities**: Beijing, Shanghai, Xi'an, Chengdu, Guilin, Hong Kong
- **Logistics**: Visas, Transportation (High-speed trains), Payments (Alipay/WeChat)
- **Culture**: Food, History, Customs

Try asking something like:
- "What should I do in Beijing?"
- "How do I pay for things in China?"
- "Do I need a visa?"
- "Tell me about Xi'an food"
"""

async def call_openai_api(question: str, context: str = "") -> Dict[str, Any]:
    """
    Call OpenAI API for travel Q&A responses
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Use local knowledge base instead of error message
        return {
            "answer": get_mock_response(question),
            "confidence": 1.0
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = """You are a knowledgeable and helpful travel assistant. Provide accurate, practical, and detailed travel advice.
    Focus on:
    - Travel destinations and attractions
    - Transportation options
    - Accommodation recommendations
    - Local customs and culture
    - Travel tips and safety advice
    - Food and dining recommendations
    - Weather and packing suggestions

    Always provide helpful, actionable advice. If you don't know something, admit it and suggest alternatives.
    Keep responses conversational but informative."""

    user_prompt = f"Travel Question: {question}"
    if context:
        user_prompt = f"Previous Context: {context}\n\nTravel Question: {question}"

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()

            return {
                "answer": result["choices"][0]["message"]["content"],
                "confidence": 0.85
            }

    except Exception as e:
        # Fallback to local knowledge base on error
        return {
            "answer": get_mock_response(question),
            "confidence": 1.0
        }

async def call_anthropic_api(question: str, context: str = "") -> Dict[str, Any]:
    """
    Call Anthropic Claude API as alternative
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return await call_openai_api(question, context)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }

    system_prompt = """You are a knowledgeable and helpful travel assistant. Provide accurate, practical, and detailed travel advice."""
    user_prompt = f"Travel Question: {question}"
    if context:
        user_prompt = f"Previous Context: {context}\n\nTravel Question: {question}"

    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 500,
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
        "system": system_prompt
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()

            return {
                "answer": result["content"][0]["text"],
                "confidence": 0.85
            }

    except Exception as e:
        return await call_openai_api(question, context)

@router.post("/ask")
async def travel_qa(request: TravelQARequest):
    """
    Travel Q&A API - Independent API for travel-related questions
    """
    # Support multiple field names for flexibility
    question = ""
    if request.user_input:
        question = request.user_input.strip()
    elif request.text:
        question = request.text.strip()
    elif request.question:
        question = request.question.strip()

    if not question:
        return {
            "bot_response": """🌍 **Travel Assistant**

I'm here to help with your travel questions! Please ask me about:

• 🏛️ Tourist attractions and landmarks
• ✈️ Transportation and getting around
• 🏨 Hotels and accommodation
• 🍜 Local food and restaurants
• 🎭 Culture and customs
• 🌤️ Weather and best times to visit
• 📋 Travel tips and safety advice
• 📄 Visa and entry requirements

What would you like to know about your travel plans?"""
        }

    # Build context from chat history
    context = ""
    if request.history and len(request.history) > 0:
        # Take last 3 messages for context
        recent_history = request.history[-3:]
        context_items = []
        for msg in recent_history:
            if msg.get("sender") == "user":
                context_items.append(f"Previous question: {msg.get('text', '')}")
            elif msg.get("sender") == "bot":
                context_items.append(f"Previous answer: {msg.get('text', '')}")
        context = " | ".join(context_items)

    # Try Anthropic first, fallback to OpenAI (which falls back to local KB)
    try:
        result = await call_anthropic_api(question, context)
    except Exception as e:
        result = await call_openai_api(question, context)

    # Format response with travel-specific styling
    formatted_answer = f"""🌍 **Travel Assistant**

{result['answer']}

---
💡 **Need more specific advice?** Feel free to ask follow-up questions about:
• Budget recommendations
• Detailed itineraries
• Local guides and tours
• Emergency contacts
• Cultural etiquette

🔄 Continue asking about your travel destination!"""

    return {
        "bot_response": formatted_answer
    }

@router.get("/health")
async def health_check():
    """
    Health check for travel API
    """
    return {
        "status": "healthy",
        "service": "Travel Q&A API",
        "features": ["AI-powered travel advice", "Multi-LLM support", "Context awareness"]
    }