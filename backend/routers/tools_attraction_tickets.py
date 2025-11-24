from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json

router = APIRouter()

class TicketQuery(BaseModel):
    attraction_name: str
    city: Optional[str] = None
    date: Optional[str] = None  # Visit date
    ticket_type: Optional[str] = "adult"  # adult, child, senior, student

# Mock Attraction Tickets Database
ATTRACTION_TICKETS = {
    "Forbidden City": {
        "city": "Beijing",
        "tickets": {
            "adult": {"price": 60, "description": "Adult Ticket"},
            "child": {"price": 20, "description": "Child Ticket (6-18 years)"},
            "senior": {"price": 0, "description": "Senior Ticket (60+ years free)"},
            "student": {"price": 20, "description": "Student Ticket"}
        },
        "tips": [
            "Advance online booking required",
            "Book 1 week in advance during peak season (Apr-Oct)",
            "Closed on Mondays (except public holidays)",
            "Bring ID/Passport for entry"
        ]
    },
    "Great Wall": {
        "city": "Beijing",
        "tickets": {
            "adult": {"price": 40, "description": "Adult Ticket"},
            "child": {"price": 20, "description": "Child Ticket"},
            "senior": {"price": 0, "description": "Senior Ticket Free"},
            "student": {"price": 20, "description": "Student Ticket"}
        },
        "tips": [
            "Badaling is most famous but crowded",
            "Mutianyu has beautiful scenery and fewer people",
            "Wear comfortable hiking shoes",
            "Best in Spring/Autumn, sun protection needed in Summer"
        ]
    },
    "Terracotta Army": {
        "city": "Xi'an",
        "tickets": {
            "adult": {"price": 120, "description": "Adult Ticket"},
            "child": {"price": 60, "description": "Child Ticket"},
            "senior": {"price": 0, "description": "Senior Ticket Free"},
            "student": {"price": 60, "description": "Student Ticket"}
        },
        "tips": [
            "Hiring a guide is recommended for history insights",
            "No flash photography allowed",
            "Visit takes about 3-4 hours",
            "Can be combined with Huaqing Pool"
        ]
    },
    "West Lake": {
        "city": "Hangzhou",
        "tickets": {
            "adult": {"price": 0, "description": "Free"},
            "child": {"price": 0, "description": "Free"},
            "senior": {"price": 0, "description": "Free"},
            "student": {"price": 0, "description": "Free"}
        },
        "tips": [
            "West Lake itself is free, some spots charge fees",
            "Cycling around the lake is recommended",
            "Spring for flowers, Autumn for osmanthus",
            "Musical fountain at night is beautiful"
        ]
    },
    "The Bund": {
        "city": "Shanghai",
        "tickets": {
            "adult": {"price": 0, "description": "Free"},
            "child": {"price": 0, "description": "Free"},
            "senior": {"price": 0, "description": "Free"},
            "student": {"price": 0, "description": "Free"}
        },
        "tips": [
            "Open all day for free",
            "Best night view time: 19:00-21:00",
            "Crowded on weekends, watch your step",
            "Take a cruise for Huangpu River night view"
        ]
    },
    "Zhangjiajie": {
        "city": "Hunan",
        "tickets": {
            "adult": {"price": 225, "description": "Adult Ticket (Valid for 4 days)"},
            "child": {"price": 120, "description": "Child Ticket"},
            "senior": {"price": 120, "description": "Senior Ticket"},
            "student": {"price": 120, "description": "Student Ticket"}
        },
        "tips": [
            "Ticket includes park eco-bus",
            "Glass Bridge and Tianmen Mountain charge separately",
            "2-3 days recommended",
            "Weather changes fast, bring rain gear"
        ]
    }
}

@router.post("/query")
async def query_attraction_tickets(query: TicketQuery):
    """
    Query Attraction Tickets Information
    """
    attraction_name = query.attraction_name.strip()

    if not attraction_name:
        return {
            "bot_response": """🎫 Attraction Tickets Query System

Please enter the name of the attraction you want to inquire about, I can provide you with:
- Various ticket price information
- Ticket purchasing tips
- Best visiting time suggestions
- Practical visitor tips

**Popular Attractions Examples:**
• Forbidden City (Beijing)
• Great Wall (Beijing)
• Terracotta Army (Xi'an)
• West Lake (Hangzhou)
• The Bund (Shanghai)
• Zhangjiajie (Hunan)

Please tell me which attraction's ticket information you'd like to know? 🏛️""",
            "suggestions": [
                "Query Forbidden City ticket prices",
                "How much are Great Wall tickets",
                "Terracotta Army purchasing guide",
                "West Lake visiting fees"
            ]
        }

    # Find attraction info
    found_attractions = []

    # Exact match
    if attraction_name in ATTRACTION_TICKETS:
        found_attractions.append((attraction_name, ATTRACTION_TICKETS[attraction_name]))
    else:
        # Fuzzy match
        for name, info in ATTRACTION_TICKETS.items():
            if attraction_name.lower() in name.lower() or name.lower() in attraction_name.lower():
                found_attractions.append((name, info))

    # City filter
    if query.city and found_attractions:
        filtered = []
        for name, info in found_attractions:
            if query.city.lower() in info["city"].lower() or info["city"].lower() in query.city.lower():
                filtered.append((name, info))
        if filtered:
            found_attractions = filtered

    if not found_attractions:
        return {
            "bot_response": f"""🎫 Attraction Tickets Query

❌ **No relevant attraction information found**

**Search Keyword:** {attraction_name}
{f"**Specified City:** {query.city}" if query.city else ""}

**Possible Reasons:**
• Attraction name is inaccurate
• Attraction is not in the database yet
• City name mismatch

**Search Suggestions:**
• Use official attraction names (e.g., "Forbidden City")
• Try simpler names
• Provide both attraction and city names

**Popular Recommendations:**
• Beijing: Forbidden City, Great Wall, Temple of Heaven
• Xi'an: Terracotta Army, Big Wild Goose Pagoda
• Hangzhou: West Lake, Lingyin Temple
• Shanghai: The Bund, Oriental Pearl Tower

Please try again with different keywords 🔄""",
            "available_attractions": list(ATTRACTION_TICKETS.keys())
        }

    # Build response
    result_text = f"""🎫 **Attraction Ticket Query Results**

Found **{len(found_attractions)}** relevant attraction(s):\n"""

    for i, (name, info) in enumerate(found_attractions, 1):
        ticket_info = info["tickets"].get(query.ticket_type, info["tickets"]["adult"])
        result_text += f"""
## {i}. {name} 🏛️
**📍 City:** {info["city"]}
**💰 {ticket_info['description']}:** ¥{ticket_info['price']}

**📋 All Ticket Prices:**"""

        for ticket_type, details in info["tickets"].items():
            result_text += f"\n  • {details['description']}: ¥{details['price']}"

        result_text += "\n\n**💡 Practical Tips:**"
        for tip in info["tips"]:
            result_text += f"\n  • {tip}"

        result_text += "\n" + "-" * 50

    result_text += f"""

**🎯 Booking Reminders:**
• Prices may vary by season, refer to official announcements
• Advance booking recommended for popular attractions
• Students/Seniors please bring relevant IDs
• Check official websites for latest info

{f"📅 **Your Visit Date:** {query.date}" if query.date else ""}

Feel free to ask about other attractions! 🚀"""

    return {
        "bot_response": result_text,
        "found_attractions": len(found_attractions),
        "search_query": attraction_name,
        "filter_city": query.city
    }

@router.get("/popular")
async def get_popular_attractions():
    """
    Get Popular Attractions List
    """
    attractions_list = []
    for name, info in ATTRACTION_TICKETS.items():
        adult_price = info["tickets"]["adult"]["price"]
        attractions_list.append({
            "name": name,
            "city": info["city"],
            "price": adult_price,
            "free": adult_price == 0
        })

    return {
        "bot_response": """🎫 **Popular China Attraction Tickets Guide**

Here are the most popular attractions in our database. You can query detailed ticket info for any of them:

**🆓 Free Attractions:**
• The Bund (Shanghai) - Open free all year
• West Lake (Hangzhou) - Lake area free, some spots charge

**🏛️ Paid Attractions:**
• Forbidden City (Beijing) - Adult ¥60
• Great Wall (Beijing) - Adult ¥40
• Terracotta Army (Xi'an) - Adult ¥120
• Zhangjiajie (Hunan) - Adult ¥225 (4 days)

Enter attraction name to get detailed prices and tips! 🎯""",
        "attractions": sorted(attractions_list, key=lambda x: x["price"])
    }

@router.get("/info")
async def get_ticket_info():
    """
    Get Ticket Query Feature Introduction
    """
    return {
        "bot_response": """🎫 **Attraction Tickets Query Assistant**

Your China travel ticket expert, providing latest prices and practical visiting advice for popular attractions nationwide!

**🎯 Features:**
• **Real-time Price Query** - Get accurate ticket price info
• **Multi-ticket Types** - Adult, Child, Student, Senior tickets
• **City Matching** - Filter attractions by city
• **Practical Tips** - Professional visiting advice and notes

**📊 Data Coverage:**
• **Tier 1 Cities**: Beijing, Shanghai, Guangzhou, Shenzhen
• **Ancient Capitals**: Xi'an, Nanjing, Luoyang
• **Scenic Cities**: Hangzhou, Suzhou, Guilin
• **Natural Wonders**: Zhangjiajie, Jiuzhaigou, Huangshan

**🎫 Ticket Info Includes:**
• Detailed price list
• Discount policy explanation
• Booking channel suggestions
• Best visiting times
• Essential notes

**💡 Usage Tips:**
1. Enter attraction name directly
2. Provide city name for more precise results
3. Choose ticket type for specific price
4. Check practical tips to optimize your trip

Make your China trip easier and more budget-friendly! 🚀""",
        "supported_features": [
            "Ticket Price Query",
            "Multi-ticket Support",
            "City Filter",
            "Visiting Tips",
            "Booking Suggestions"
        ],
        "coverage": [
            "Major Cities Nationwide",
            "5A Scenic Spots",
            "Historical Sites",
            "Natural Scenery"
        ]
    }