from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json

router = APIRouter()

class HotelQuery(BaseModel):
    city: str
    check_in: Optional[str] = None  # Check-in date
    check_out: Optional[str] = None  # Check-out date
    price_range: Optional[str] = None  # budget, mid-range, luxury
    room_type: Optional[str] = None  # single, double, suite
    rating: Optional[int] = None  # 1-5 stars

# Mock Hotel Recommendation Database
HOTEL_RECOMMENDATIONS = {
    "Beijing": [
        {
            "name": "Hilton Beijing Wangfujing",
            "rating": 5,
            "price_range": "luxury",
            "starting_price": 800,
            "location": "Wangfujing Street, Dongcheng District",
            "highlights": ["Prime Wangfujing location", "Luxury amenities", "Chinese & Western restaurants", "Fitness center"],
            "booking_tips": "Book early for best rates",
            "recommendation_reason": "Best choice for luxury shopping and dining in Beijing's commercial center",
            "best_for": ["Luxury travelers", "Shopping enthusiasts", "First-time visitors"]
        },
        {
            "name": "Home Inn Qianmen",
            "rating": 3,
            "price_range": "budget",
            "starting_price": 200,
            "location": "Qianmen Street, Xicheng District",
            "highlights": ["Convenient location", "Great value", "Clean and comfortable", "Metro accessible"],
            "booking_tips": "Popular budget choice, fills up fast",
            "recommendation_reason": "Excellent budget option with easy access to historic attractions",
            "best_for": ["Budget travelers", "History enthusiasts", "Backpackers"]
        },
        {
            "name": "Grand Hyatt Beijing",
            "rating": 5,
            "price_range": "luxury",
            "starting_price": 1000,
            "location": "Jianguomenwai Avenue, Chaoyang District",
            "highlights": ["CBD core location", "Premium service", "Indoor pool", "Michelin restaurant"],
            "booking_tips": "Great for business trips",
            "recommendation_reason": "Top choice for business travelers with excellent facilities",
            "best_for": ["Business travelers", "Luxury seekers", "Extended stays"]
        }
    ],
    "Shanghai": [
        {
            "name": "Waldorf Astoria Shanghai on the Bund",
            "rating": 5,
            "price_range": "luxury",
            "starting_price": 1500,
            "location": "Zhongshan East Road, Huangpu District",
            "highlights": ["Bund skyline views", "Historic architecture", "Luxury service", "Fine dining"],
            "booking_tips": "River view rooms sell out fast",
            "recommendation_reason": "Ultimate luxury experience with iconic Shanghai views",
            "best_for": ["Luxury travelers", "Couples", "Special occasions"]
        },
        {
            "name": "Hanting Express Nanjing Road",
            "rating": 3,
            "price_range": "budget",
            "starting_price": 250,
            "location": "Nanjing Road Pedestrian Street, Huangpu District",
            "highlights": ["Pedestrian street core", "Great transport links", "Chain reliability", "Good value"],
            "booking_tips": "Noisy area, bring earplugs",
            "recommendation_reason": "Perfect location for exploring Shanghai on foot",
            "best_for": ["Budget travelers", "Shoppers", "Short stays"]
        },
        {
            "name": "The Ritz-Carlton Shanghai, Pudong",
            "rating": 5,
            "price_range": "luxury",
            "starting_price": 1200,
            "location": "Lujiazui Financial District, Pudong New Area",
            "highlights": ["Lujiazui financial center", "Oriental Pearl Tower views", "Luxury facilities", "Professional service"],
            "booking_tips": "High floor bar is a must-visit",
            "recommendation_reason": "Premium choice in Shanghai's financial district",
            "best_for": ["Business travelers", "Luxury seekers", "Skyline lovers"]
        }
    ],
    "Xi'an": [
        {
            "name": "The Westin Xian",
            "rating": 5,
            "price_range": "luxury",
            "starting_price": 600,
            "location": "South Street, Beilin District",
            "highlights": ["Near Bell Tower", "Ancient city views", "Modern amenities", "Chinese & Western dining"],
            "booking_tips": "Walking distance to Muslim Quarter",
            "recommendation_reason": "Perfect blend of traditional charm and modern comfort",
            "best_for": ["Cultural tourists", "History lovers", "Comfort seekers"]
        },
        {
            "name": "7 Days Inn Xian Railway Station",
            "rating": 3,
            "price_range": "budget",
            "starting_price": 150,
            "location": "Jiefang Road, Xincheng District",
            "highlights": ["Near railway station", "Convenient transport", "Economical", "Clean facilities"],
            "booking_tips": "Basic amenities only",
            "recommendation_reason": "Budget-friendly option for transit travelers",
            "best_for": ["Transit passengers", "Budget travelers", "Short stays"]
        },
        {
            "name": "Grand Hyatt Xian",
            "rating": 5,
            "price_range": "luxury",
            "starting_price": 700,
            "location": "Qujiang New District, Yanta District",
            "highlights": ["Near Tang Paradise", "Luxury facilities", "Garden views", "Rich cultural atmosphere"],
            "booking_tips": "Great for families",
            "recommendation_reason": "Best for those wanting to experience Xian's cultural heritage",
            "best_for": ["Cultural tourists", "Luxury travelers", "Extended cultural stays"]
        }
    ]
}

# Use English keys for consistency
HOTEL_DATABASE = HOTEL_RECOMMENDATIONS

PRICE_RANGE_MAP = {
    "budget": {"min": 0, "max": 300, "label": "Budget"},
    "mid-range": {"min": 301, "max": 800, "label": "Mid-range"},
    "luxury": {"min": 801, "max": 9999, "label": "Luxury"}
}

@router.post("/recommend")
async def recommend_hotels(query: HotelQuery):
    """
    Recommend Hotels
    """
    city = query.city.strip()

    if not city:
        return {
            "bot_response": """🏨 **Hotel Recommendations for China**

Get personalized hotel recommendations for your China journey! I'll help you find the perfect accommodation based on your preferences.

**🎯 What I Can Recommend:**
• Hotels by city and location
• Different price ranges and styles
• Star ratings and amenities
• Best options for different traveler types

**💰 Budget Categories:**
• **Budget** ($20-50/night) - Clean, basic, great value
• **Mid-range** ($50-120/night) - Comfortable, good amenities
• **Luxury** ($120+/night) - Premium facilities and service

**🌟 Featured Cities:**
• **Beijing** - Historic capital with diverse options
• **Shanghai** - Modern metropolis with luxury hotels
• **Xi'an** - Cultural city with traditional charm
• **Guangzhou** - Southern hub with business hotels
• **Chengdu** - Cultural city with unique accommodations

**👥 Traveler Types:**
• Budget travelers seeking value
• Luxury travelers wanting premium service
• Business travelers needing convenience
• Cultural tourists wanting local experiences
• Families needing space and amenities

Which city would you like hotel recommendations for? 🏙️""",
            "suggestions": [
                "Recommend hotels in Beijing",
                "Shanghai luxury hotel recommendations",
                "Budget hotels in Xi'an",
                "Best hotels for business travelers in Shanghai"
            ]
        }

    # Find city hotel recommendations
    hotels = HOTEL_RECOMMENDATIONS.get(city, [])

    if not hotels:
        # Fuzzy match
        for db_city, db_hotels in HOTEL_RECOMMENDATIONS.items():
            if city.lower() in db_city.lower() or db_city.lower() in city.lower():
                hotels = db_hotels
                city = db_city
                break

    if not hotels:
        return {
            "bot_response": f"""🏨 **Hotel Recommendations**

❌ **No hotel recommendations found**

**Searched city:** {city}

**Possible reasons:**
• This city is not in our database yet
• City name might need adjustment

**Available cities:**
• **Beijing** - Historic capital with diverse options
• **Shanghai** - Modern metropolis with luxury hotels
• **Xi'an** - Cultural city with traditional charm
• **Guangzhou** - Southern hub with business hotels

**Suggestions:**
• Use standard English city names
• Try major tourist cities
• Ask for general China hotel advice

Would you like me to recommend hotels for a different city? 🔄""",
            "available_cities": list(HOTEL_RECOMMENDATIONS.keys())
        }

    # Apply filters
    filtered_hotels = hotels

    if query.price_range:
        range_info = PRICE_RANGE_MAP.get(query.price_range)
        if range_info:
            filtered_hotels = [
                h for h in filtered_hotels
                if range_info["min"] <= h["starting_price"] <= range_info["max"]
            ]

    if query.rating:
        filtered_hotels = [h for h in filtered_hotels if h["rating"] >= query.rating]

    if not filtered_hotels:
        return {
            "bot_response": f"""🏨 Hotel Search Results

📍 **City:** {city}
❌ **No hotels found matching your criteria**

**Your Criteria:**
{f"💰 Price Range: {PRICE_RANGE_MAP.get(query.price_range, {}).get('label', query.price_range)}" if query.price_range else ""}
{f"🌟 Min Rating: {query.rating} Stars" if query.rating else ""}

**Suggestions:**
• Relax price or rating requirements
• Reduce filter conditions
• Choose off-peak season for more options

Would you like to see all hotels in this city? 🤔""",
            "city": city,
            "search_criteria": {
                "price_range": query.price_range,
                "rating": query.rating
            }
        }

    # Build result
    result_text = f"""🏨 **{city} Hotel Recommendations**

Found **{len(filtered_hotels)}** hotels matching your criteria:\n"""

    for i, hotel in enumerate(filtered_hotels, 1):
        stars = "⭐" * hotel["rating"]
        price_info = f"¥{hotel['starting_price']}"

        result_text += f"""
## {i}. {hotel['name']} {stars}

**💰 Starting Price:** {price_info}/night
**📍 Location:** {hotel['location']}
**🏷️ Type:** {PRICE_RANGE_MAP[hotel['price_range']]['label']}

**✨ Highlights:**"""
        for highlight in hotel['highlights']:
            result_text += f"\n  • {highlight}"

        result_text += f"\n\n**💡 Booking Tips:** {hotel['booking_tips']}"
        result_text += "\n" + "-" * 50

    result_text += f"""

**📅 Your Stay Info:**
{f"🔑 Check-in: {query.check_in}" if query.check_in else ""}
{f"🚪 Check-out: {query.check_out}" if query.check_out else ""}

**🎯 Booking Reminders:**
• Prices are for reference only, actual rates may vary
• Book 1-2 weeks in advance for popular hotels
• Prices usually rise during holidays
• Compare prices across platforms for best deals

Let me know if you need more help or other city recommendations! 🛎️"""

    return {
        "bot_response": result_text,
        "city": city,
        "found_hotels": len(filtered_hotels),
        "search_criteria": {
            "price_range": query.price_range,
            "rating": query.rating
        }
    }

@router.get("/popular")
async def get_popular_cities():
    """
    Get Popular Cities and Hotels
    """
    popular_cities = []
    for city, hotels in HOTEL_DATABASE.items():
        city_info = {
            "name": city,
            "hotel_count": len(hotels),
            "min_price": min(h["starting_price"] for h in hotels),
            "max_price": max(h["starting_price"] for h in hotels),
            "has_luxury": any(h["rating"] == 5 for h in hotels)
        }
        popular_cities.append(city_info)

    return {
        "bot_response": """🏨 **Popular City Hotel Guide**

Top hotel recommendations for major Chinese tourist cities:

**🏛️ Historical & Cultural Cities:**
• **Beijing** - Ancient capital charm, rich hotel choices
• **Xi'an** - 13 dynasties capital, high value

**🌃 Modern International Metropolises:**
• **Shanghai** - International hub, luxury hotels galore

**🐼 Unique Tourist Cities:**
• **Chengdu** - Land of Abundance, surrounded by food
• **Hangzhou** - Paradise on Earth, lake and mountain views

**💰 Price Range Coverage:**
• Budget: ¥150-300/night
• Mid-range: ¥300-800/night
• Luxury: ¥600-1500/night

Enter city name to view detailed hotel info and booking advice! 🎯""",
        "cities": popular_cities
    }

@router.get("/info")
async def get_hotel_info():
    """
    Get Hotel Booking Feature Introduction
    """
    return {
        "bot_response": """🏨 **Hotel Booking Assistant**

Your China accommodation expert, recommending the best hotel choices for you!

**🎯 Service Features:**
• **City Coverage** - Comprehensive coverage of major tourist cities
• **Multi-tier Pricing** - Budget to luxury to meet all needs
• **Star Rating Filter** - 1-5 star precise matching
• **Location Recommendation** - Hotels near transport and attractions
• **Practical Tips** - Professional booking and stay advice

**📊 Data Advantages:**
• **Transparent Pricing** - Real-time reference prices, clear budget
• **Detailed Location** - Precise addresses for easy planning
• **Complete Facilities** - Hotel features and amenities listed
• **Booking Advice** - Professional timing and tips

**🏙️ Covered Cities:**
• **Beijing** - Wangfujing, CBD, Historic Areas
• **Shanghai** - The Bund, Lujiazui, Nanjing Road
• **Xi'an** - Bell Tower, Big Wild Goose Pagoda, Qujiang
• **Chengdu** - Chunxi Road, Kuanzhai Alley, Jinjiang
• **Hangzhou** - West Lake Area, Qianjiang New City

**💡 User Guide:**
1. Enter city name to start search
2. Set price range and star rating
3. View hotel details and booking advice
4. Choose the best fit for your needs

Have a comfortable stay on your China trip! 🛏️""",
        "features": [
            "City Hotel Search",
            "Price Range Filter",
            "Star Rating Match",
            "Detailed Location Info",
            "Booking Advice"
        ],
        "price_ranges": ["Budget", "Mid-range", "Luxury"],
        "covered_cities": list(HOTEL_DATABASE.keys())
    }
