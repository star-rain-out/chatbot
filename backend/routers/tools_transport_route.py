from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json

router = APIRouter()

class RouteQuery(BaseModel):
    from_city: str
    to_city: str
    transport_type: Optional[str] = None  # flight, train, bus, car
    budget: Optional[str] = None  # economy, business, luxury
    travel_time: Optional[str] = None  # morning, afternoon, evening, night

# Mock Transport Route Database
TRANSPORT_ROUTES = {
    "Beijing-Shanghai": {
        "distance": 1200,
        "options": {
            "flight": {
                "economy": {"price": 800, "duration": "2 hours", "frequency": "Every 30 mins"},
                "business": {"price": 2000, "duration": "2 hours", "frequency": "Every 30 mins"}
            },
            "train": {
                "economy": {"price": 550, "duration": "4.5-6 hours", "frequency": "Every 30 mins"},
                "business": {"price": 900, "duration": "4.5-6 hours", "frequency": "Every 30 mins"}
            },
            "bus": {
                "economy": {"price": 200, "duration": "12-14 hours", "frequency": "Every 1 hour"}
            },
            "car": {
                "luxury": {"price": 800, "duration": "10-12 hours", "frequency": "Anytime"}
            }
        },
        "tips": [
            "Flight is fastest, High-speed rail has best value",
            "Book early for holidays, prices rise",
            "High-speed rail seats are more comfortable, high punctuality",
            "Self-drive allows sightseeing but consider fatigue"
        ]
    },
    "Beijing-Xi'an": {
        "distance": 1100,
        "options": {
            "flight": {
                "economy": {"price": 600, "duration": "1.5 hours", "frequency": "Every hour"},
                "business": {"price": 1500, "duration": "1.5 hours", "frequency": "Every hour"}
            },
            "train": {
                "economy": {"price": 400, "duration": "4-5 hours", "frequency": "Every 30 mins"},
                "business": {"price": 650, "duration": "4-5 hours", "frequency": "Every 30 mins"}
            },
            "bus": {
                "economy": {"price": 180, "duration": "10-12 hours", "frequency": "Every 2 hours"}
            },
            "car": {
                "luxury": {"price": 700, "duration": "8-10 hours", "frequency": "Anytime"}
            }
        },
        "tips": [
            "High-speed rail is frequent and flexible",
            "Can visit Luoyang, Zhengzhou along the way",
            "Xi'an airport to city is about 1 hour drive",
            "Beautiful scenery for self-drive in Spring/Autumn"
        ]
    },
    "Shanghai-Hangzhou": {
        "distance": 180,
        "options": {
            "flight": {
                "economy": {"price": 400, "duration": "1 hour", "frequency": "Every 2 hours"}
            },
            "train": {
                "economy": {"price": 70, "duration": "1 hour", "frequency": "Every 15 mins"},
                "business": {"price": 120, "duration": "1 hour", "frequency": "Every 15 mins"}
            },
            "bus": {
                "economy": {"price": 50, "duration": "2 hours", "frequency": "Every 30 mins"}
            },
            "car": {
                "luxury": {"price": 150, "duration": "1.5 hours", "frequency": "Anytime"}
            }
        },
        "tips": [
            "High-speed rail is most convenient, frequent",
            "Self-drive can visit Wuzhen, Xitang water towns",
            "Hangzhou metro connected with Shanghai metro",
            "Avoid peak hours on weekends"
        ]
    },
    "Chengdu-Chongqing": {
        "distance": 300,
        "options": {
            "flight": {
                "economy": {"price": 300, "duration": "1 hour", "frequency": "Every hour"}
            },
            "train": {
                "economy": {"price": 100, "duration": "1-1.5 hours", "frequency": "Every 30 mins"},
                "business": {"price": 160, "duration": "1-1.5 hours", "frequency": "Every 30 mins"}
            },
            "bus": {
                "economy": {"price": 80, "duration": "3-4 hours", "frequency": "Every 1 hour"}
            },
            "car": {
                "luxury": {"price": 200, "duration": "2.5 hours", "frequency": "Anytime"}
            }
        },
        "tips": [
            "Chengdu-Chongqing HSR is very convenient, best choice",
            "Can visit Leshan, Zigong along the way",
            "Chongqing is hilly, plan accordingly",
            "Both cities have rich food culture, worth deep exploration"
        ]
    },
    "Guangzhou-Shenzhen": {
        "distance": 120,
        "options": {
            "train": {
                "economy": {"price": 75, "duration": "30-40 mins", "frequency": "Every 10 mins"},
                "business": {"price": 120, "duration": "30-40 mins", "frequency": "Every 10 mins"}
            },
            "bus": {
                "economy": {"price": 40, "duration": "1.5 hours", "frequency": "Every 15 mins"}
            },
            "car": {
                "luxury": {"price": 100, "duration": "1 hour", "frequency": "Anytime"}
            }
        },
        "tips": [
            "High-speed rail is fastest, frequent",
            "Guangzhou-Shenzhen highway often congested, HSR recommended",
            "Convenient transport allows inter-city living",
            "Shenzhen Bay Port connects directly to Hong Kong"
        ]
    }
}

@router.post("/plan")
async def plan_route(query: RouteQuery):
    """
    Plan Transport Route
    """
    from_city = query.from_city.strip()
    to_city = query.to_city.strip()

    if not from_city or not to_city:
        return {
            "bot_response": """🛣️ Transport Route Planning Assistant

I can help you plan the best transportation routes within China, offering multiple travel options and detailed suggestions!

**🚀 Transportation Methods:**
• ✈️ **Flight** - Fastest speed, suitable for long-distance travel
• 🚄 **High-speed Rail** - Balance of speed and comfort, great value
• 🚌 **Bus** - Economical choice, suitable for budget travel
• 🚗 **Self-drive** - Flexible freedom, can stop for sightseeing

**💰 Price Types:**
• **Economy** - Money-saving practical choice
• **Business** - Balance of comfort and price
• **Luxury** - Best travel experience

**⏰ Travel Times:**
• Morning, afternoon, evening, night shifts

Please tell me your departure and destination! 🗺️""",
            "suggestions": [
                "Beijing to Shanghai route",
                "How to get from Guangzhou to Shenzhen",
                "Chengdu to Chongqing high-speed rail query",
                "Shanghai to Hangzhou transportation options"
            ]
        }

    # Find route
    route_key_1 = f"{from_city}-{to_city}"
    route_key_2 = f"{to_city}-{from_city}"

    # Try exact match first, then fuzzy match
    route_info = None
    matched_key = None
    
    if route_key_1 in TRANSPORT_ROUTES:
        route_info = TRANSPORT_ROUTES[route_key_1]
        matched_key = route_key_1
    elif route_key_2 in TRANSPORT_ROUTES:
        route_info = TRANSPORT_ROUTES[route_key_2]
        matched_key = route_key_2
    else:
        # Fuzzy search
        for key, info in TRANSPORT_ROUTES.items():
            cities = key.split("-")
            if (from_city.lower() in cities[0].lower() and to_city.lower() in cities[1].lower()) or \
               (from_city.lower() in cities[1].lower() and to_city.lower() in cities[0].lower()):
                route_info = info
                matched_key = key
                break

    if not route_info:
        return {
            "bot_response": f"""🛣️ Route Planning Results

❌ **No detailed info found for this route**

**Route:** {from_city} → {to_city}

**Possible Reasons:**
• Route not in database yet
• City names might need adjustment

**🌟 Popular Routes:**
• Beijing ↔ Shanghai (1200km)
• Beijing ↔ Xi'an (1100km)
• Shanghai ↔ Hangzhou (180km)
• Chengdu ↔ Chongqing (300km)
• Guangzhou ↔ Shenzhen (120km)

**💡 Suggestions:**
• Use standard city names
• Try popular routes above
• Ask about specific transport methods

Need help with other routes? 🔄""",
            "available_routes": list(TRANSPORT_ROUTES.keys())
        }

    # Build result
    result_text = f"""🛣️ **{from_city} → {to_city} Transport Route Plan**

**📏 Distance:** {route_info['distance']} km
**⏱️ Recommended Options:**\n"""

    options = route_info["options"]

    # Filter transport type
    if query.transport_type:
        if query.transport_type in options:
            transport_options = {query.transport_type: options[query.transport_type]}
        else:
            return {
                "bot_response": f"""🛣️ Route Planning Results

❌ **Selected transport type not available for this route**

**Route:** {from_city} → {to_city}
**Selected Type:** {query.transport_type}

**Available Types:**
• {' • '.join(options.keys())}

Please choose another transport type 🔄"""
            }
    else:
        transport_options = options

    for transport_type, options_data in transport_options.items():
        transport_icons = {
            "flight": "✈️",
            "train": "🚄",
            "bus": "🚌",
            "car": "🚗"
        }

        icon = transport_icons.get(transport_type, "🚀")
        transport_names = {
            "flight": "Flight",
            "train": "High-speed Rail",
            "bus": "Bus",
            "car": "Self-drive"
        }
        name = transport_names.get(transport_type, transport_type.title())

        result_text += f"\n### {icon} **{name}**"

        for budget_type, info in options_data.items():
            if query.budget and query.budget != budget_type:
                continue

            budget_names = {
                "economy": "Economy",
                "business": "Business",
                "luxury": "Luxury"
            }
            budget_name = budget_names.get(budget_type, budget_type.title())

            result_text += f"""
  • **{budget_name} Class:** ¥{info['price']}
  • ⏱️ Duration: {info['duration']}
  • 🕒 Frequency: {info['frequency']}"""

    result_text += f"""

**💡 Route Tips:**"""
    for tip in route_info["tips"]:
        result_text += f"\n  • {tip}"

    result_text += f"""

**📅 Your Trip Info:**
{f"🚗 Transport: {query.transport_type}" if query.transport_type else ""}
{f"💰 Budget: {query.budget}" if query.budget else ""}
{f"⏰ Time: {query.travel_time}" if query.travel_time else ""}

**🎯 Practical Reminders:**
• Book tickets early for holidays
• Arrive 30 mins early for High-speed rail
• Arrive 2 hours early for flights
• Rest well if self-driving

Have a safe trip! 🌟"""

    return {
        "bot_response": result_text,
        "from_city": from_city,
        "to_city": to_city,
        "distance": route_info["distance"]
    }

@router.get("/popular")
async def get_popular_routes():
    """
    Get Popular Routes
    """
    routes_info = []
    for route_key, info in TRANSPORT_ROUTES.items():
        cities = route_key.split("-")
        routes_info.append({
            "from": cities[0],
            "to": cities[1],
            "distance": info["distance"],
            "min_price": min(
                min(options["economy"]["price"] if "economy" in options else float('inf')
                    for options in info["options"].values())
            )
        })

    return {
        "bot_response": """🛣️ **Popular Transport Routes**

Selected popular travel routes within China:

**🌟 Top Routes:**
• **Beijing ↔ Shanghai** - North-East connection, most convenient
• **Beijing ↔ Xi'an** - Ancient capitals tour, rich history
• **Shanghai ↔ Hangzhou** - Yangtze Delta core, short trip choice

**🚄 HSR Selections:**
• **Chengdu ↔ Chongqing** - West China hub, 30-min circle
• **Guangzhou ↔ Shenzhen** - Pearl River Delta core, city-link

**💡 Route Features:**
• **Cross-region**: Beijing-Shanghai, 1200km
• **History Tour**: Beijing-Xi'an, cultural richness
• **City Circle**: Shanghai-Hangzhou, 1-hour circle
• **Economic Belt**: Chengdu-Chongqing, western passage

Enter departure and destination to see detailed plans! 🗺️""",
        "routes": sorted(routes_info, key=lambda x: x["distance"])
    }

@router.get("/info")
async def get_transport_info():
    """
    Get Transport Planning Feature Introduction
    """
    return {
        "bot_response": """🛣️ **Transport Route Planning Assistant**

Your China travel expert, providing the best transportation route planning and travel suggestions!

**🎯 Core Features:**
• **Multi-modal Options** - Comprehensive coverage of flights, high-speed rail, buses, self-driving
• **Price Comparison** - Transparent comparison of different price tiers
• **Time Optimization** - Fastest travel times and frequency information
• **Practical Advice** - Professional travel tips and important notes

**🚊 Transportation Details:**
• **✈️ Flight** - Best for 1000km+ long distances, fastest speed
• **🚄 High-speed Rail** - Best choice for 300-1200km, king of value
• **🚌 Bus** - Economic choice for short distances, covers small and medium cities
• **🚗 Self-drive** - Flexible freedom, suitable for in-depth travel and sightseeing

**📊 Data Coverage:**
• **Major Cities**: Beijing, Shanghai, Guangzhou, Shenzhen, Chengdu, Xi'an, Hangzhou
• **Popular Routes**: Inter-provincial lines, city group connections, tourist routes
• **Real-time Info**: Reference prices, travel times, frequency information
• **Professional Advice**: Booking tips, travel timing, important considerations

**💡 Usage Tips:**
1. Enter departure and destination
2. Choose preferred transportation method
3. Set budget tier requirements
4. View detailed travel suggestions

Let your China journey be smoother and more convenient! 🚀""",
        "features": [
            "Multi-modal transport planning",
            "Price and time comparison",
            "Schedule information query",
            "Travel advice provision",
            "Popular route recommendations"
        ],
        "transport_types": ["Flight", "High-speed Rail", "Bus", "Self-driving"],
        "popular_routes": list(TRANSPORT_ROUTES.keys())
    }
