from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json

router = APIRouter()

class ChinaExperienceQuery(BaseModel):
    query_type: Optional[str] = None  # food, culture, festivals, all
    city: Optional[str] = None
    region: Optional[str] = None
    season: Optional[str] = None

# China Food Database
CHINA_FOOD_DATABASE = {
    "Beijing": {
        "specialties": [
            {
                "name": "Peking Duck",
                "description": "Roast duck with crispy skin and tender meat",
                "avg_price": "$20-40",
                "famous_restaurants": ["Quanjude", "Bianyifang", "Dadong"],
                "tips": "Best served with thin pancakes, scallions, and sweet bean sauce"
            },
            {
                "name": "Zhajiangmian",
                "description": "Traditional Beijing noodles with fermented soybean paste",
                "avg_price": "$3-8",
                "famous_restaurants": ["Haiwanju", "Old Beijing Zhajiangmian"],
                "tips": "Classic Beijing comfort food, great for breakfast or lunch"
            }
        ],
        "street_food": [
            {"name": "Tanghulu", "description": "Candied hawthorn berries", "price": "$2"},
            {"name": "Jianbing", "description": "Chinese crepe with egg and scallions", "price": "$3"}
        ]
    },
    "Shanghai": {
        "specialties": [
            {
                "name": "Xiaolongbao",
                "description": "Soup-filled dumplings with delicate skin",
                "avg_price": "$5-10",
                "famous_restaurants": ["Nanxiang Mantou", "Din Tai Fung", "Jiajia"],
                "tips": "Bite a small hole first to let the steam escape, then sip the soup"
            },
            {
                "name": "Shengjianbao",
                "description": "Pan-fried pork buns with crispy bottom",
                "avg_price": "$3-6",
                "famous_restaurants": ["Xiaoyang Shengjian", "Dahuchun"],
                "tips": "Best when hot, dipped in vinegar"
            }
        ]
    },
    "Sichuan": {
        "specialties": [
            {
                "name": "Hot Pot",
                "description": "Spicy broth with various ingredients",
                "avg_price": "$15-30",
                "famous_restaurants": ["Haidilao", "Xiaolongkan", "Shujiuxiang"],
                "tips": "Start with mild spicy if you're new to Sichuan cuisine"
            },
            {
                "name": "Mapo Tofu",
                "description": "Spicy tofu with minced pork",
                "avg_price": "$5-10",
                "famous_restaurants": ["Chen Mapo Tofu", "Sichuan restaurants"],
                "tips": "Classic Sichuan dish, numbing and spicy flavors"
            }
        ]
    }
}

# Chinese Culture Database
CHINESE_CULTURE = {
    "festivals": [
        {
            "name": "Spring Festival",
            "english_name": "Chinese New Year",
            "date": "First day of first lunar month",
            "traditions": ["Family reunion dinner", "Red envelopes", "Fireworks", "Lion/dragon dances"],
            "foods": ["Dumplings", "Fish", "Sweet rice balls"],
            "significance": "Most important traditional festival marking new lunar year"
        },
        {
            "name": "Mid-Autumn Festival",
            "english_name": "Moon Festival",
            "date": "15th day of 8th lunar month",
            "traditions": ["Moon viewing", "Lantern lighting", "Mooncake sharing"],
            "foods": ["Mooncakes", "Pomelo", "Osmanthus wine"],
            "significance": "Celebrates harvest and family reunion"
        },
        {
            "name": "Dragon Boat Festival",
            "english_name": "Duanwu Festival",
            "date": "5th day of 5th lunar month",
            "traditions": ["Dragon boat racing", "Zongzi eating", "Hanging mugwort"],
            "foods": ["Zongzi (rice dumplings)", "Realgar wine"],
            "significance": "Commemorates poet Qu Yuan"
        }
    ],
    "traditions": [
        {
            "name": "Tea Culture",
            "description": "Traditional tea ceremony and various tea types",
            "regions": ["Hangzhou (Longjing)", "Sichuan (Biluochun)", "Yunnan (Pu'er)"],
            "practices": ["Gongfu tea ceremony", "Tea tasting", "Tea house culture"]
        },
        {
            "name": "Kung Fu",
            "description": "Traditional Chinese martial arts",
            "styles": ["Shaolin", "Tai Chi", "Wing Chun"],
            "significance": "Physical discipline, mental cultivation"
        }
    ]
}

# City Mapping for Normalization
CITY_MAPPING = {
    "beijing": "Beijing", "peking": "Beijing", "北京": "Beijing",
    "shanghai": "Shanghai", "上海": "Shanghai",
    "sichuan": "Sichuan", "szechuan": "Sichuan", "四川": "Sichuan",
    "guangdong": "Guangdong", "canton": "Guangdong", "广东": "Guangdong"
}

@router.post("/explore")
async def explore_china_experience(query: ChinaExperienceQuery):
    """Explore Chinese food, culture, and festivals"""
    
    # Normalize query if it matches a city
    if query.query_type:
        normalized_query = query.query_type.lower().strip()
        if normalized_query in CITY_MAPPING:
            query.city = CITY_MAPPING[normalized_query]
            query.query_type = "all"
    
    if not query.query_type:
        return {
            "bot_response": """🍜🏮🎊 **China Experience Explorer**

Discover the rich culture, delicious cuisine, and vibrant festivals of China!

**🎯 What I Can Help You Explore:**

**🍜 Chinese Food Culture**
• Regional specialties and famous dishes
• Street food and local delicacies
• Dining customs and etiquette
• Best restaurants and food recommendations

**🏮 Traditional Culture**
• Ancient customs and traditions
• Cultural practices and ceremonies
• Historical significance and modern adaptations
• Cultural sites and heritage locations

**🎊 Festivals & Celebrations**
• Traditional festivals and their meanings
• Modern celebrations and events
• Festival foods and activities
• Best times and places to experience

**🌍 Popular Regions to Explore:**
• **Beijing** - Imperial cuisine and traditional customs
• **Shanghai** - Fusion dishes and modern celebrations
• **Sichuan** - Spicy cuisine and cultural diversity
• **Guangdong** - Cantonese food and southern traditions

**💡 How to Ask:**
• "Tell me about Beijing food"
• "What are Chinese New Year traditions?"
• "Recommend Sichuan dishes"
• "Explain Mid-Autumn Festival"

Choose your interest and let's explore China together! 🌟""",
            "suggestions": [
                "Tell me about Beijing food specialties",
                "What are Chinese New Year traditions?",
                "Recommend famous Chinese dishes",
                "Explain Chinese tea culture",
                "When is the Mid-Autumn Festival?",
                "What are traditional Chinese customs?"
            ]
        }

    result_text = f"""🍜🏮🎊 **China Experience Explorer**"""

    if query.query_type == "food" or query.query_type == "all":
        result_text += f"""

## 🍜 Chinese Food Culture"""

        if query.city:
            if query.city in CHINA_FOOD_DATABASE:
                city_food = CHINA_FOOD_DATABASE[query.city]
                result_text += f"""

**📍 {query.city} Specialties:**"""
                for food in city_food.get("specialties", []):
                    result_text += f"""
• **{food['name']}** - {food['description']}
  💰 Average: {food['avg_price']}
  🏪 Famous: {', '.join(food['famous_restaurants'])}
  💡 Tip: {food['tips']}"""

                if "street_food" in city_food:
                    result_text += f"""

**Street Food:**
• **{city_food['street_food'][0]['name']}** - {city_food['street_food'][0]['description']} (${city_food['street_food'][0]['price']})"""
            else:
                result_text += f"\n\nFood information for {query.city} is not available. Available cities: {', '.join(CHINA_FOOD_DATABASE.keys())}"
        else:
            result_text += f"""

**Regional Highlights:**
• **Beijing** - Peking Duck, Zhajiangmian
• **Shanghai** - Xiaolongbao, Shengjianbao
• **Sichuan** - Hot Pot, Mapo Tofu
• **Guangdong** - Dim Sum, Roast Goose

Which region interests you most?"""

    if query.query_type == "culture" or query.query_type == "all":
        result_text += f"""

## 🏮 Traditional Chinese Culture"""

        traditions = CHINESE_CULTURE["traditions"]
        for tradition in traditions:
            result_text += f"""
• **{tradition['name']}** - {tradition['description']}"""
            if 'regions' in tradition:
                result_text += f"\n  🌍 Famous in: {', '.join(tradition['regions'])}"

    if query.query_type == "festivals" or query.query_type == "all":
        result_text += f"""

## 🎊 Chinese Festivals & Celebrations"""

        festivals = CHINESE_CULTURE["festivals"]
        for festival in festivals:
            result_text += f"""
• **{festival['name']}** ({festival['english_name']})
  📅 Date: {festival['date']}
  🎭 Traditions: {', '.join(festival['traditions'])}
  🍜 Foods: {', '.join(festival['foods'])}
  ✨ Significance: {festival['significance']}"""

    result_text += f"""

**💡 Travel Tips:**
• Ask about specific cities for detailed food recommendations
• Learn basic dining etiquette for authentic experiences
• Visit during festivals for cultural immersion
• Try street food for local flavors

Would you like to know more about any specific aspect of Chinese culture? 🌟"""

    return {
        "bot_response": result_text,
        "query_type": query.query_type,
        "city": query.city
    }

@router.get("/info")
async def get_china_experience_info():
    """Get China experience explorer information"""
    return {
        "bot_response": """🍜🏮🎊 **China Experience Explorer**

Your comprehensive guide to Chinese food, culture, and festivals!

**🎯 Core Features:**
• **Food Guide** - Authentic Chinese cuisine by region
• **Culture Explorer** - Traditional customs and practices
• **Festival Calendar** - Traditional celebrations and events
• **Regional Specialties** - Local dishes and cultural highlights
• **Practical Tips** - Etiquette and travel recommendations

**🍜 What We Cover:**
• Regional specialties and famous restaurants
• Street food and local delicacies
• Traditional dining customs
• Cooking techniques and ingredients

**🏮 Cultural Elements:**
• Traditional festivals and celebrations
• Ancient customs and modern practices
• Cultural sites and heritage locations
• Traditional arts and crafts

**🎊 Festival Information:**
• Major traditional festivals
• Festival foods and activities
• Best times and places to celebrate
• Cultural significance and meanings

**🌟 Why Choose This Service:**
• Comprehensive coverage of Chinese culture
• Authentic local recommendations
• Practical travel advice
• Cultural context and history
• Food safety and etiquette tips

Experience the authentic culture and flavors of China! 🌟""",
        "features": [
            "Food recommendations by region",
            "Cultural traditions and customs",
            "Festival calendar and celebrations",
            "Restaurant and dining guides",
            "Travel tips and etiquette"
        ],
        "categories": ["food", "culture", "festivals"],
        "covered_regions": list(CHINA_FOOD_DATABASE.keys())
    }
