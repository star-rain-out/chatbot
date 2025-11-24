from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import httpx
import json
import os
from dotenv import load_dotenv
import base64
import io
from PIL import Image
import uuid
import tempfile
import random

# Load environment variables
load_dotenv()

router = APIRouter()

class LandmarkRecognitionRequest(BaseModel):
    image_description: str  # For text-based fallback

class LandmarkRecognitionResponse(BaseModel):
    result: str

# Enhanced landmark database with keywords for smart simulation
LANDMARK_DATABASE = {
    "great_wall": {
        "keywords": ["great_wall", "wall", "changcheng", "badaling", "mutianyu", "china_wall"],
        "name": "Great Wall of China",
        "confidence": 0.98,
        "description": "Ancient fortification system stretching across northern China, built to protect against invasions.",
        "location": "Northern China (accessible from Beijing)",
        "facts": [
            "Total length: 21,196 km (13,171 miles)",
            "Took over 2,000 years to build",
            "Visible from space is a myth",
            "8 million people visit annually",
            "Different sections built by different dynasties"
        ],
        "tips": [
            "Badaling section is most accessible but crowded",
            "Mutianyu offers better views and fewer crowds",
            "Jinshanling is best for hiking enthusiasts",
            "Bring water and wear comfortable shoes",
            "Spring and autumn are best seasons to visit"
        ]
    },
    "forbidden_city": {
        "keywords": ["forbidden", "palace", "gugong", "beijing_palace", "imperial"],
        "name": "The Forbidden City",
        "confidence": 0.96,
        "description": "The imperial palace complex in Beijing, home to 24 emperors during the Ming and Qing dynasties.",
        "location": "Beijing, China",
        "facts": [
            "World's largest imperial palace",
            "Contains 980 buildings and 8,700 rooms",
            "Built between 1406 and 1420",
            "UNESCO World Heritage Site",
            "Yellow roof tiles were exclusively for the Emperor"
        ],
        "tips": [
            "Book tickets online at least 7 days in advance",
            "Closed on Mondays",
            "Wear comfortable walking shoes",
            "Rent an audio guide for history details",
            "Visit Jingshan Park afterwards for a panoramic view"
        ]
    },
    "terracotta_warriors": {
        "keywords": ["terracotta", "warriors", "bingmayong", "xian", "army", "soldier"],
        "name": "Terracotta Warriors",
        "confidence": 0.97,
        "description": "A collection of terracotta sculptures depicting the armies of Qin Shi Huang, the first Emperor of China.",
        "location": "Xi'an, China",
        "facts": [
            "Discovered by local farmers in 1974",
            "Dating from approximately 210 BCE",
            "Figures vary in height according to their roles",
            "Includes warriors, chariots and horses",
            "Estimated to contain over 8,000 soldiers"
        ],
        "tips": [
            "Hire a guide to understand the history",
            "Pit 1 is the largest and most impressive",
            "Visit early morning to avoid crowds",
            "No flash photography allowed",
            "Buy souvenirs from the official shop"
        ]
    },
    "summer_palace": {
        "keywords": ["summer", "palace", "yiheyuan", "kunming", "lake"],
        "name": "Summer Palace",
        "confidence": 0.95,
        "description": "A vast ensemble of lakes, gardens and palaces in Beijing, serving as an imperial garden.",
        "location": "Beijing, China",
        "facts": [
            "Largest and best-preserved royal park in China",
            "Dominated by Longevity Hill and Kunming Lake",
            "Rebuilt in 1886 after destruction by war",
            "Favorite retreat of Empress Dowager Cixi",
            "UNESCO World Heritage Site"
        ],
        "tips": [
            "Take a boat ride on Kunming Lake",
            "Walk the Long Corridor to see painted scenes",
            "Climb Longevity Hill for views",
            "Allow at least half a day for visiting",
            "Combined ticket covers all attractions inside"
        ]
    },
    "oriental_pearl": {
        "keywords": ["oriental", "pearl", "tower", "shanghai", "tv_tower", "pudong"],
        "name": "Oriental Pearl Tower",
        "confidence": 0.99,
        "description": "A distinctively shaped TV tower in Shanghai, featuring 11 spheres.",
        "location": "Shanghai, China",
        "facts": [
            "468 meters (1,535 feet) tall",
            "Was the tallest structure in China from 1994-2007",
            "Features a revolving restaurant",
            "Has a glass-bottomed observation deck",
            "Design inspired by a Tang dynasty poem"
        ],
        "tips": [
            "Visit at night for the light show",
            "Glass floor deck is thrilling but safe",
            "History museum at the base is excellent",
            "Avoid weekends if possible",
            "Check visibility before going up"
        ]
    },
    "eiffel_tower": {
        "keywords": ["eiffel", "paris", "france", "tower"],
        "name": "Eiffel Tower",
        "confidence": 0.95,
        "description": "Iconic iron lattice tower located on the Champ de Mars in Paris, France",
        "location": "Paris, France",
        "facts": [
            "Built in 1889 as the entrance to the World's Fair",
            "Stands 330 meters (1,083 ft) tall",
            "Most-visited paid monument in the world",
            "Painted every 7 years to prevent rust",
            "Sways up to 6-7 cm in the wind"
        ],
        "tips": [
            "Book tickets online to avoid long queues",
            "Best views at sunset from Trocadéro",
            "Visit early morning or late evening for fewer crowds",
            "Champagne bar at the top is worth the visit",
            "Check lighting schedule for night photography"
        ]
    }
}

async def call_vision_api(image_data: bytes) -> Dict[str, Any]:
    """
    Call computer vision API for landmark recognition
    """
    api_key = os.getenv("AZURE_VISION_KEY") or os.getenv("GOOGLE_VISION_API_KEY")

    if not api_key:
        # No API key found, return None to trigger smart simulation
        return None

    try:
        # Google Vision API implementation
        if os.getenv("GOOGLE_VISION_API_KEY"):
            return await call_google_vision(image_data)

        # Azure Computer Vision implementation
        elif os.getenv("AZURE_VISION_KEY"):
            # Placeholder for Azure implementation
            return None

    except Exception as e:
        print(f"API Error: {e}")
        return None

async def smart_simulate_landmark_recognition(filename: str) -> Dict[str, Any]:
    """
    Smart simulation based on filename matching
    """
    filename_lower = filename.lower()
    
    # Check for keyword matches in filename
    for key, data in LANDMARK_DATABASE.items():
        for keyword in data.get("keywords", []):
            if keyword in filename_lower:
                return {
                    "landmark": key,
                    "confidence": data["confidence"],
                    "simulated": True
                }
    
    # Fallback to random if no keyword match
    landmarks = list(LANDMARK_DATABASE.keys())
    detected_landmark = random.choice(landmarks)
    
    return {
        "landmark": detected_landmark,
        "confidence": random.uniform(0.7, 0.85),
        "simulated": True,
        "is_random": True
    }

async def call_google_vision(image_data: bytes) -> Dict[str, Any]:
    """
    Call Google Cloud Vision API for landmark detection
    """
    api_key = os.getenv("GOOGLE_VISION_API_KEY")
    if not api_key:
        return None

    # Convert image to base64
    image_b64 = base64.b64encode(image_data).decode()

    request_data = {
        "requests": [
            {
                "image": {
                    "content": image_b64
                },
                "features": [
                    {
                        "type": "LANDMARK_DETECTION",
                        "maxResults": 3
                    }
                ]
            }
        ]
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"https://vision.googleapis.com/v1/images:annotate?key={api_key}",
            json=request_data
        )
        response.raise_for_status()
        result = response.json()

        if result.get("responses") and result["responses"][0].get("landmarkAnnotations"):
            landmark = result["responses"][0]["landmarkAnnotations"][0]
            return {
                "landmark": landmark.get("description", "").lower().replace(" ", "_"),
                "confidence": landmark.get("score", 0.5),
                "simulated": False
            }

    return None

def preprocess_image(image_data: bytes) -> bytes:
    """
    Preprocess image for better recognition
    """
    try:
        # Open and optimize image
        image = Image.open(io.BytesIO(image_data))

        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Resize if too large (max 1080p)
        max_size = (1920, 1080)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save optimized image
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        return buffer.getvalue()

    except Exception as e:
        # Return original if preprocessing fails
        return image_data

@router.post("/recognize", response_model=LandmarkRecognitionResponse)
async def recognize_landmark(image: UploadFile = File(...)):
    """
    Landmark Recognition API - Independent API for identifying landmarks from images
    """
    # Validate image file
    if not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image (JPEG, PNG, etc.)"
        )

    try:
        # Read and preprocess image
        image_data = await image.read()
        processed_image = preprocess_image(image_data)

        # Try to call real Vision API first
        recognition_result = await call_vision_api(processed_image)

        # If API failed or no key, use smart simulation
        if not recognition_result:
            recognition_result = await smart_simulate_landmark_recognition(image.filename)

        landmark_key = recognition_result.get("landmark", "")
        confidence = recognition_result.get("confidence", 0.0)
        is_simulated = recognition_result.get("simulated", False)
        is_random = recognition_result.get("is_random", False)

        # Get landmark information from database
        # Try exact match first, then fuzzy match
        landmark_info = LANDMARK_DATABASE.get(landmark_key)
        
        if not landmark_info:
            # Try to find by name if key doesn't match
            for key, data in LANDMARK_DATABASE.items():
                if key in landmark_key or landmark_key in key:
                    landmark_info = data
                    break

        if not landmark_info:
            return {
                "result": """❓ **Landmark Not Recognized**

I couldn't identify this landmark with confidence. Please try with:

📸 **Better Photo Tips:**
• Ensure the landmark is clearly visible and centered
• Good lighting helps with recognition
• Try different angles if the first attempt fails
• Famous landmarks are more likely to be recognized

💡 **Alternative:** You can describe the landmark in text instead!

🌍 Try uploading photos of famous landmarks like:
• Eiffel Tower • Great Wall • Statue of Liberty
• Taj Mahal • Colosseum • Big Ben • Sydney Opera House"""
            }

        # Format response with travel styling
        simulation_note = ""
        if is_simulated:
            if is_random:
                simulation_note = "\n\n*(Note: Running in demo mode. Random landmark selected because no API key was found and filename didn't match known landmarks.)*"
            else:
                simulation_note = "\n\n*(Note: Identified based on filename in demo mode. Add Google Vision API key for AI recognition.)*"

        formatted_response = f"""🏛️ **{landmark_info["name"]}**

📍 **Location:** {landmark_info["location"]}

📖 **Description:** {landmark_info["description"]}

🎯 **Confidence:** {confidence:.1%}

📚 **Interesting Facts:**
{chr(10).join(f"• {fact}" for fact in landmark_info["facts"])}

💡 **Travel Tips:**
{chr(10).join(f"• {tip}" for tip in landmark_info["tips"])}{simulation_note}

---
🌟 **Want to know more?** Ask me about:
• Best time to visit
• Nearby attractions
• Transportation options
• Local cuisine
• Photography spots"""

        return {
            "result": formatted_response
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

@router.post("/describe")
async def describe_landmark_text(request: LandmarkRecognitionRequest):
    """
    Fallback endpoint for text-based landmark description
    """
    description = request.image_description.lower()

    # Simple keyword matching for demo
    matched_landmark = None
    for key, landmark in LANDMARK_DATABASE.items():
        # Check keywords
        if any(keyword in description for keyword in landmark.get("keywords", [])):
            matched_landmark = landmark
            break
        # Check key name
        if any(word in description for word in key.split("_")):
            matched_landmark = landmark
            break

    if not matched_landmark:
        return {
            "result": """🔍 **Landmark Not Found**

Please describe a famous landmark like:

🌍 **Famous Landmarks You Can Ask About:**
• Eiffel Tower (Paris) • Great Wall (China)
• Statue of Liberty (USA) • Taj Mahal (India)
• Colosseum (Rome) • Big Ben (London)
• Sydney Opera House • Machu Picchu

💡 **Tips for Better Description:**
• Mention the city or country
• Describe distinctive features
• Include what it's famous for

Example: "tall iron tower in Paris with observation decks"
"""
        }

    # Format response for matched landmark
    formatted_response = f"""🏛️ **{matched_landmark["name"]}**

📍 **Location:** {matched_landmark["location"]}

📖 **Description:** {matched_landmark["description"]}

📚 **Interesting Facts:**
{chr(10).join(f"• {fact}" for fact in matched_landmark["facts"])}

💡 **Travel Tips:**
{chr(10).join(f"• {tip}" for tip in matched_landmark["tips"])}

---
🌟 **Want to know more?** Ask me about:
• Best time to visit
• Nearby attractions
• Transportation options
• Local cuisine"""

    return {
        "result": formatted_response
    }

@router.get("/health")
async def health_check():
    """
    Health check for landmark recognition API
    """
    return {
        "status": "healthy",
        "service": "Landmark Recognition API",
        "features": ["Image upload support", "AI-powered recognition", "Travel information", "Simulated fallback"]
    }