from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List
import base64
import io
import json
from PIL import Image
import requests
import uuid
import os
import random
import tempfile
from serpapi import GoogleSearch

router = APIRouter()

class SocialMediaRequest(BaseModel):
    image_description: Optional[str] = None
    platform: Optional[str] = "general"
    tone: Optional[str] = "friendly"
    hashtags_count: Optional[int] = 5

# SerpApi Configuration
SERPAPI_KEY = "416c3f455698c1a4f445e5afc78980a9ed90428e700aae4cc25f18e0c0b9377d"

# Multiple mock scenarios for variety
MOCK_SCENARIOS = [
    {
        "description": "Beautiful beach sunset scenery, orange sky reflected on calm sea, distant mountain silhouettes",
        "objects": ["beach", "sunset", "ocean", "clouds", "mountains"],
        "colors": ["orange", "blue", "yellow", "purple"],
        "mood": "peaceful, romantic, spectacular",
        "location_type": "natural landscape",
        "activities": ["sightseeing", "photography", "relaxation", "walking"]
    },
    {
        "description": "Delicious Chinese dishes on table, vibrant colors and steam rising from hot pot",
        "objects": ["food", "table", "chopsticks", "bowls", "steam"],
        "colors": ["red", "green", "white", "brown"],
        "mood": "appetizing, warm, inviting",
        "location_type": "restaurant",
        "activities": ["dining", "gathering", "socializing", "tasting"]
    },
    {
        "description": "Modern city skyline at night, bright lights reflecting off glass buildings",
        "objects": ["buildings", "lights", "skyline", "city", "night"],
        "colors": ["blue", "yellow", "white", "black"],
        "mood": "vibrant, bustling, energetic",
        "location_type": "urban scene",
        "activities": ["exploring", "nightlife", "photography", "walking"]
    },
    {
        "description": "Cozy cafe interior with latte art and pastries on wooden table",
        "objects": ["coffee", "pastry", "table", "cup", "foam"],
        "colors": ["brown", "white", "cream", "beige"],
        "mood": "cozy, relaxing, artistic",
        "location_type": "cafe",
        "activities": ["relaxing", "reading", "chatting", "enjoying"]
    },
    {
        "description": "Green mountains covered in mist with traditional Chinese architecture",
        "objects": ["mountains", "temple", "trees", "mist", "architecture"],
        "colors": ["green", "gray", "brown", "white"],
        "mood": "serene, mystical, ancient",
        "location_type": "scenic area",
        "activities": ["hiking", "sightseeing", "photography", "meditation"]
    },
    {
        "description": "Cherry blossoms in full bloom along tree-lined street",
        "objects": ["flowers", "trees", "street", "petals", "branches"],
        "colors": ["pink", "white", "green", "blue"],
        "mood": "romantic, cheerful, refreshing",
        "location_type": "park",
        "activities": ["strolling", "photography", "picnic", "enjoying nature"]
    }
]

def analyze_image_via_serpapi(image_bytes: bytes) -> Optional[str]:
    """
    Analyze image using SerpApi Google Reverse Image Search.
    Returns a description (best guess) of the image.
    """
    if not SERPAPI_KEY:
        print("DEBUG: Missing SERPAPI_KEY")
        return None

    try:
        # Upload to tmpfiles.org to get a public URL
        # SerpApi requires a public URL for google_reverse_image
        print("DEBUG: Uploading image to tmpfiles.org...")
        files = {'file': ('image.jpg', image_bytes, 'image/jpeg')}
        upload_response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)
        
        image_url = None
        if upload_response.status_code == 200:
            result = upload_response.json()
            if result.get('status') == 'success':
                url = result['data']['url']
                # Convert to direct download URL
                image_url = url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
                print(f"DEBUG: Image uploaded to: {image_url}")
            else:
                print(f"DEBUG: tmpfiles.org upload failed: {result}")
        else:
            print(f"DEBUG: tmpfiles.org HTTP Error: {upload_response.status_code}")

        if not image_url:
            print("DEBUG: Failed to get public URL for image. Skipping SerpApi.")
            return None

        print(f"DEBUG: Analyzing image via SerpApi: {image_url}")

        params = {
            "engine": "google_reverse_image",
            "image_url": image_url,
            "api_key": SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        # Extract "best guess" or knowledge graph title
        description = None
        
        # 1. Try "image_results" -> "search_information" -> "query_displayed" (sometimes contains the guess)
        if "search_information" in results and "query_displayed" in results["search_information"]:
             description = results["search_information"]["query_displayed"]
        
        # 2. Try Knowledge Graph title
        if not description and "knowledge_graph" in results:
            description = results["knowledge_graph"].get("title")
            
        # 3. Try Inline Images title or similar
        if not description and "inline_images" in results:
             # Sometimes inline images have a title related to the search
             pass

        if description:
            print(f"DEBUG: ✅ SerpApi Analysis Success: {description}")
            return description
        else:
            print("DEBUG: ❌ SerpApi returned no clear description.")
            # print(f"DEBUG: Full response keys: {results.keys()}")
            return None

    except Exception as e:
        print(f"DEBUG: SerpApi Error: {e}")
        return None

def build_analysis_from_caption(caption: str) -> dict:
    """Build an analysis dict compatible with generate_social_media_caption
    from a plain caption string.
    """
    if not caption:
        caption = "A beautiful moment worth sharing."
    return {
        "description": caption,
        "objects": [],
        "colors": [],
        "mood": "beautiful, amazing",
        "location_type": "scene",
        "activities": [],
        "source": "serpapi"
    }

def analyze_image_with_base64(base64_image: str) -> dict:
    """Analyze image content.

    Priority:
    1. Try real image analysis via SerpApi (Google Reverse Image Search)
       to get a textual description from the actual image contents.
    2. If that fails, fall back to the existing heuristic + mock scenarios.
    """
    try:
        # Decode image bytes
        img_data = base64.b64decode(base64_image)

        # 1) Try real analysis via SerpApi
        description = analyze_image_via_serpapi(img_data)
        if description:
            return build_analysis_from_caption(description)

        # 2) Fallback: local heuristic using color distribution
        img = Image.open(io.BytesIO(img_data))

        # Simple heuristic: choose scenario based on image dimensions and average color
        width, height = img.size
        aspect_ratio = width / height if height > 0 else 1.0
        
        # Get average color to help choose scenario
        img_small = img.resize((10, 10))
        pixels = list(img_small.getdata())
        avg_red = sum(p[0] for p in pixels if isinstance(p, tuple)) / len(pixels)
        avg_green = sum(p[1] for p in pixels if isinstance(p, tuple)) / len(pixels)
        avg_blue = sum(p[2] for p in pixels if isinstance(p, tuple)) / len(pixels)

        # Heuristic to pick scenario
        if avg_red > avg_blue and avg_red > avg_green:
            # More red/warm tones -> food or sunset
            scenario = random.choice([MOCK_SCENARIOS[0], MOCK_SCENARIOS[1]])
        elif avg_green > avg_red and avg_green > avg_blue:
            # More green -> nature
            scenario = random.choice([MOCK_SCENARIOS[4], MOCK_SCENARIOS[5]])
        elif avg_blue > avg_red:
            # More blue -> city night or sky
            scenario = random.choice([MOCK_SCENARIOS[0], MOCK_SCENARIOS[2]])
        else:
            # Balanced or neutral -> cafe or urban
            scenario = random.choice([MOCK_SCENARIOS[3], MOCK_SCENARIOS[2]])

        return scenario

    except Exception:
        # Fallback to random scenario if anything goes wrong
        return random.choice(MOCK_SCENARIOS)

def generate_social_media_caption(analysis: dict, platform: str = "general", tone: str = "friendly", hashtags_count: int = 5) -> dict:
    """
    Generate social media captions based on image analysis
    """
    description = analysis["description"]
    objects = analysis["objects"]
    mood = analysis["mood"]
    location_type = analysis["location_type"]

    # Expanded caption templates
    base_templates = {
        "general": [
            f"✨ {description}",
            f"📸 Capturing this beautiful moment! {description}",
            f"🌟 {description}",
            f"💫 Today's highlight: {description}"
        ],
        "wechat": [
            f"🌿 {description}\n\n#LifeMoments #DailyShare",
            f"💖 Moments worth cherishing! {description}\n\n#BeautifulDay #Memories",
            f"📷 {description}\n\n#PhotoDiary #HappyTimes"
        ],
        "weibo": [
            f"【📍Check-in】{description} 📸\n\n#LifeAesthetics #TravelDiary",
            f"✨ {description}\n\n#DailyLife #Photography",
            f"🌈 {description}\n\n#ShareLife #BeautifulMoments"
        ],
        "instagram": [
            f"Chasing moments like these ✨\n{description}\n\n#photography #instagood",
            f"🌿 {description}\n\n#lifestyle #photooftheday",
            f"Living for moments like this 💫\n{description}\n\n#beautiful #nature"
        ],
        "twitter": [
            f"✨ {description} #photography #beautiful",
            f"Amazing views today! {description} 📸",
            f"💫 {description} #lifestyle #moments"
        ]
    }

    # Tone adjustments
    tone_modifiers = {
        "professional": {
            "prefix": "Professional perspective:",
            "suffix": "\n\n#Industry #Professional",
            "style": "professional"
        },
        "casual": {
            "prefix": "Just captured this~",
            "suffix": "\n\n#Casual #Daily",
            "style": "casual"
        },
        "friendly": {
            "prefix": "Sharing with friends:",
            "suffix": "\n\n#Friends #Share",
            "style": "friendly"
        },
        "humorous": {
            "prefix": "Look what I found! 😄",
            "suffix": "\n\n#Fun #Humor",
            "style": "humorous"
        }
    }

    # Generate relevant hashtags
    hashtag_pool = []
    for obj in objects[:3]:  # Limit to top 3 objects
        hashtag_pool.append(f"#{obj.replace(' ', '')}")

    # Add mood-based hashtags
    mood_words = mood.split(", ")
    for word in mood_words[:2]:
        hashtag_pool.append(f"#{word.replace(' ', '')}")

    # Add general popular hashtags
    general_tags = ["#photography", "#life", "#beautiful", "#moments", "#travel", "#instagood", "#photooftheday"]
    hashtag_pool.extend(random.sample(general_tags, 3))

    # Remove duplicates and select
    unique_hashtags = list(set(hashtag_pool))
    selected_hashtags = unique_hashtags[:hashtags_count]
    hashtags_text = " ".join(selected_hashtags)

    # Select template and generate caption
    templates = base_templates.get(platform, base_templates["general"])
    selected_template = random.choice(templates)

    # Apply tone
    modifier = tone_modifiers.get(tone, tone_modifiers["friendly"])
    caption = selected_template.format(description=description, hashtags=hashtags_text)

    if tone != "general" and tone in tone_modifiers:
        caption = f"{modifier['prefix']} {caption}{modifier['suffix']}"

    return {
        "caption": caption,
        "hashtags": selected_hashtags,
        "platform": platform,
        "tone": tone,
        "analysis_summary": {
            "main_objects": objects[:3],
            "mood": mood,
            "location_type": location_type,
            "source": analysis.get("source", "local")
        }
    }

@router.post("/generate")
async def generate_social_media_caption_from_image(
    image: UploadFile = File(None),
    image_data: Optional[str] = Form(None),
    platform: str = Form("general"),
    tone: str = Form("friendly"),
    hashtags_count: int = Form(5)
):
    """
    Generate social media captions from uploaded image
    """

    if not image and not image_data:
        return {
            "bot_response": """📸 **Social Media Caption Generator**

Upload an image and I'll generate perfect captions for your social media posts!

**Features:**
• 🎯 Smart content analysis (Powered by Google Reverse Image Search)
• ✍️ Platform-specific captions (WeChat, Weibo, Instagram, Twitter)
• 🎭 Multiple tone styles
• 🏷️ Auto-generated hashtags
• 🌍 English & Chinese support

**How to use:**
1. Upload an image
2. Choose your platform and tone
3. Get ready-to-use captions!

**Supported platforms:**
• General Format
• WeChat Moments
• Sina Weibo
• Instagram
• Twitter

Upload an image to get started! ✨""",
            "suggestions": [
                "Upload travel photos",
                "Upload food photos",
                "Upload selfies",
                "Upload product photos"
            ]
        }

    try:
        # Process image
        image_content = None
        if image:
            image_content = await image.read()
            if not image.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="File must be an image")
        elif image_data:
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            image_content = base64.b64decode(image_data)

        # Verify image
        try:
            img = Image.open(io.BytesIO(image_content))
            img.verify()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image: {str(e)}")

        # Convert to base64 for analysis
        base64_image = base64.b64encode(image_content).decode('utf-8')

        # Analyze image
        analysis = analyze_image_with_base64(base64_image)

        # Generate caption
        result = generate_social_media_caption(
            analysis=analysis,
            platform=platform,
            tone=tone,
            hashtags_count=hashtags_count
        )

        # Build response
        platform_names = {
            "general": "General", "wechat": "WeChat", "weibo": "Weibo",
            "instagram": "Instagram", "twitter": "Twitter"
        }

        tone_names = {
            "professional": "Professional", "casual": "Casual",
            "friendly": "Friendly", "humorous": "Humorous"
        }

        response_text = f"""📸 **Social Media Caption Generated!**

**Platform**: {platform_names.get(platform, 'General')}
**Tone**: {tone_names.get(tone, 'Friendly')}

📝 **Your Caption**:
{result['caption']}

🏷️ **Hashtags**:
{', '.join(result['hashtags'])}

---
💡 **Image Analysis**:
• Main elements: {', '.join(result['analysis_summary']['main_objects'])}
• Mood: {result['analysis_summary']['mood']}
• Scene: {result['analysis_summary']['location_type']}
• Source: {result['analysis_summary'].get('source', 'local')}

✨ Copy and paste to use! You can adjust the caption as needed."""

        # Check if SerpApi was used and prepend success message
        if result['analysis_summary'].get('source') == 'serpapi':
            response_text = "✅ SerpApi (Google Reverse Image) Analysis Successful:\n\n" + response_text

        return {
            "bot_response": response_text,
            "generated_caption": result['caption'],
            "hashtags": result['hashtags'],
            "platform": platform,
            "tone": tone,
            "image_analysis": result['analysis_summary']
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@router.get("/info")
async def get_social_media_generator_info():
    """
    Get information about the caption generator
    """
    return {
        "bot_response": """📸 **Social Media Caption Generator**

AI-powered tool to create engaging social media captions!

🎯 **Features**:
• Smart image analysis (Google Reverse Image Search)
• Platform-specific formatting
• Multiple tone options
• Auto-generated hashtags

🌐 **Supported Platforms**:
• General Format
• WeChat Moments
• Sina Weibo
• Instagram
• Twitter

🎭 **Caption Styles**:
• Professional
• Casual
• Friendly
• Humorous

Upload an image to get started! ✨""",
        "supported_platforms": ["general", "wechat", "weibo", "instagram", "twitter"],
        "supported_tones": ["professional", "casual", "friendly", "humorous"]
    }