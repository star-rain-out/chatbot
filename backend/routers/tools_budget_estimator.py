from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json

router = APIRouter()

class BudgetQuery(BaseModel):
    destination: str
    duration_days: int
    travel_style: Optional[str] = "mid_range"  # budget, mid_range, luxury
    group_size: int = 1  # Number of travelers
    season: Optional[str] = "shoulder"  # shoulder, peak, off-peak
    include_flights: bool = False  # International flights
    accommodation_preference: Optional[str] = None  # budget, mid_range, luxury

# Budget categories with ranges (per person per day in USD)
BUDGET_CATEGORIES = {
    "budget": {"accommodation": 15, "food": 25, "transport": 10, "activities": 15, "shopping": 10, "misc": 5},
    "mid_range": {"accommodation": 50, "food": 40, "transport": 15, "activities": 30, "shopping": 20, "misc": 10},
    "luxury": {"accommodation": 120, "food": 80, "transport": 25, "activities": 60, "shopping": 40, "misc": 15}
}

# Season multipliers
SEASON_MULTIPLIERS = {
    "shoulder": 1.0,  # Apr-May, Sep-Oct
    "peak": 1.3,    # Jun-Aug, Dec-Feb (except Chinese New Year)
    "off_peak": 0.7  # Mar, early Nov
}

# Group size discounts
GROUP_DISCOUNTS = {
    1: 1.0,    # Solo traveler
    2: 0.8,    # 25% discount for 2 people
    3: 0.75,   # 25% discount for 3-4 people
    4: 0.7,    # 30% discount for 5+ people
    5: 0.65    # 35% discount for 6+ people
}

# Flight costs (round trip from major cities)
FLIGHT_COSTS = {
    "from_us": {"economy": 800, "business": 2000, "first_class": 4000},
    "from_uk": {"economy": 900, "business": 2500, "first_class": 4500},
    "from_singapore": {"economy": 500, "business": 1500, "first_class": 3000},
    "from_japan": {"economy": 600, "business": 1800, "first_class": 3500},
    "from_australia": {"economy": 1000, "business": 2500, "first_class": 4500},
    "from_europe": {"economy": 700, "business": 2000, "first_class": 3500}
}

# Major cities with additional costs
CITY_FACTORS = {
    "Beijing": {"accommodation": 1.2, "activities": 1.3, "food": 1.1},
    "Shanghai": {"accommodation": 1.3, "activities": 1.4, "food": 1.2},
    "Shenzhen": {"accommodation": 1.0, "activities": 1.0, "food": 1.0},
    "Guangzhou": {"accommodation": 0.9, "activities": 1.0, "food": 0.9},
    "Chengdu": {"accommodation": 0.7, "activities": 0.8, "food": 0.8},
    "Xian": {"accommodation": 0.7, "activities": 0.9, "food": 0.7},
    "Hangzhou": {"accommodation": 0.9, "activities": 1.0, "food": 1.1},
    "Kunming": {"accommodation": 0.6, "activities": 0.7, "food": 0.8},
    "Lhasa": {"accommodation": 0.8, "activities": 1.0, "food": 1.2},
    "Urumqi": {"accommodation": 0.6, "activities": 0.7, "food": 0.7}
}

@router.post("/estimate")
async def estimate_budget(query: BudgetQuery):
    """
    Estimate travel budget for China
    """
    destination = query.destination.strip()
    duration = query.duration_days
    travel_style = query.travel_style or "mid_range"
    group_size = query.group_size
    season = query.season or "shoulder"
    include_flights = query.include_flights

    if not destination or duration <= 0:
        return {
            "bot_response": """💰 **China Travel Budget Estimator**

Plan your China trip budget with detailed cost breakdowns and personalized recommendations!

**🎯 What I Can Estimate:**
• **Accommodation** - Hotels, hostels, guesthouses by city
• **Food & Dining** - Local restaurants, street food, fine dining
• **Transportation** - Domestic travel within China
• **Activities & Attractions** - Tours, entrance fees, experiences
• **Shopping** - Souvenirs, gifts, personal items
• **Miscellaneous** - Insurance, visas, daily expenses
• **International Flights** - Round-trip airfare from your location

**💰 Budget Categories:**
• **Budget** ($40-80/day per person) - Hostels, local food, public transport
• **Mid-range** ($80-150/day per person) - 3-star hotels, mixed dining, some taxis
• **Luxury** ($150-300+/day per person) - 4-5 star hotels, fine dining, private transport

**👥 Group Size Benefits:**
• 1 person: Full price
• 2-3 people: 25% discount on shared costs
• 4-5 people: 30% discount on shared costs
• 6+ people: 35% discount on shared costs

**📅 Seasonal Pricing:**
• **Shoulder** (Apr-May, Sep-Oct): Standard rates
• **Peak** (Jun-Aug, Dec-Feb): 30% higher prices
• **Off-peak** (Mar, early Nov): 30% lower prices

**🌏 Featured Destinations:**
• Beijing, Shanghai, Guangzhou, Shenzhen
• Chengdu, Xian, Hangzhou, Kunming
• Major tourist cities with varied costs

Which destination would you like a budget estimate for? 🗺️""",
            "suggestions": [
                "Estimate budget for Beijing 7 days",
                "Shanghai luxury travel for 5 days",
                "Budget backpacking in Chengdu",
                "Xian cultural trip for 4 days",
                "Flights from USA to China included"
            ]
        }

    # Get base budget per day
    base_budget = BUDGET_CATEGORIES[travel_style]
    total_base = sum(base_budget.values())

    # Apply city factors
    city = destination.title()
    city_factor = CITY_FACTORS.get(city, {"accommodation": 1.0, "activities": 1.0, "food": 1.0})

    # Adjust for city cost of living
    adjusted_total = 0
    for category, base_amount in base_budget.items():
        factor = city_factor.get(category, 1.0)
        adjusted_total += base_amount * factor

    # Apply seasonal multiplier
    season_multiplier = SEASON_MULTIPLIERS.get(season, 1.0)
    adjusted_total *= season_multiplier

    # Calculate total for duration
    china_total = adjusted_total * duration

    # Apply group discount for shared costs
    group_discount = GROUP_DISCOUNTS.get(group_size, 1.0)
    # Accommodation, food, activities, transport, shopping get discount
    shared_categories = ["accommodation", "food", "activities", "transport", "shopping", "misc"]
    shared_total = sum([base_budget[cat] for cat in shared_categories]) * duration * season_multiplier

    # Solo traveler doesn't get accommodation discount
    if group_size == 1:
        shared_categories = ["food", "activities", "transport", "shopping", "misc"]
        shared_total = sum([base_budget[cat] for cat in shared_categories]) * duration * season_multiplier

    shared_total *= group_discount

    # Misc expenses (visa, insurance, etc.)
    misc_total = base_budget["misc"] * duration * season_multiplier
    if group_size == 1:
        misc_total *= 1.0
    else:
        misc_total *= group_discount

    china_total = shared_total + (base_budget["accommodation"] * duration * season_multiplier)

    # Calculate flight costs
    flight_cost = 0
    flight_info = ""
    if include_flights:
        # Default to US pricing for demonstration
        flight_data = FLIGHT_COSTS.get("from_us", FLIGHT_COSTS["from_us"])
        flight_cost = flight_data["economy"] * group_size
        flight_info = f"Economy class from US for {group_size} people"

    # Calculate total budget
    total_budget = china_total + flight_cost
    per_person_budget = total_budget / group_size

    # Build detailed breakdown
    result_text = f"""💰 **China Travel Budget Estimate**

**📍 Destination:** {destination}
**⏱️ Duration:** {duration} days
**🎭️ Travel Style:** {travel_style.title()}
**👥 Group Size:** {group_size} traveler(s)
**📅 Season:** {season.title()}
**✈️ International Flights:** {'Included' if include_flights else 'Not included'}

---

## 📊 **Budget Breakdown**

### 🏨 Accommodation (Per Day: ${base_budget['accommodation'] * city_factor.get('accommodation', 1.0) * season_multiplier:.1f})
Total: ${(base_budget['accommodation'] * city_factor.get('accommodation', 1.0) * season_multiplier * duration):.0f} USD

### 🍽️ Food & Dining (Per Day: ${base_budget['food'] * city_factor.get('food', 1.0) * season_multiplier:.1f})
Total: ${(base_budget['food'] * city_factor.get('food', 1.0) * season_multiplier * duration * (0.8 if group_size > 1 else 1.0)):.0f} USD

### 🚗 Transportation (Per Day: ${base_budget['transport'] * season_multiplier:.1f})
Total: ${(base_budget['transport'] * season_multiplier * duration * (0.8 if group_size > 1 else 1.0)):.0f} USD

### 🎭 Activities & Attractions (Per Day: ${base_budget['activities'] * city_factor.get('activities', 1.0) * season_multiplier:.1f})
Total: ${(base_budget['activities'] * city_factor.get('activities', 1.0) * season_multiplier * duration * (0.8 if group_size > 1 else 1.0)):.0f} USD

### 🛍️ Shopping (Per Day: ${base_budget['shopping'] * season_multiplier:.1f})
Total: ${(base_budget['shopping'] * season_multiplier * duration * (0.8 if group_size > 1 else 1.0)):.0f} USD

### 🌟 **Final Budget:**
• **Total Trip Cost:** ${total_budget:.0f} USD
• **Per Person:** ${per_person_budget:.0f} USD
• **Daily Average:** ${(total_budget / duration if duration > 0 else 0):.0f} USD/day

### 💡 **Money-Saving Tips:**
• **Book in advance** - Save 15-25% on hotels
• **Travel offseason** - Save 30% on peak season rates
• **Use public transport** - Cheaper than taxis in cities
• **Eat local street food** - Authentic and budget-friendly
• **Shop at local markets** - Better prices than tourist shops
• **Stay in hostels** - Great for budget travelers
• **Travel with friends** - Split accommodation costs

### 🎯 **Budget Categories:**
• **Budget Travel**: Under $100/day total
• **Mid-Range**: $100-200/day total
• **Luxury Travel**: $200+/day total

### 📈 **Seasonal Advice:**
• **Best Value**: March, September, October (shoulder season)
• **Most Expensive**: June-August, December-February (peak season)
• **Cheapest**: November, February (off-peak except Chinese New Year)

Would you like more detailed recommendations for your {destination} trip? 🚀"""

    return {
        "bot_response": result_text,
        "total_budget": total_budget,
        "per_person_budget": per_person_budget,
        "daily_average": total_budget / duration if duration > 0 else 0,
        "china_total": china_total,
        "flight_cost": flight_cost,
        "destination": destination,
        "duration": duration,
        "travel_style": travel_style,
        "group_size": group_size
    }

@router.post("/compare")
async def compare_budget_options(query: BudgetQuery):
    """
    Compare budget options for the same trip
    """
    # Generate estimates for different budget levels
    results = []
    budget_styles = ["budget", "mid_range", "luxury"]

    for style in budget_styles:
        temp_query = BudgetQuery(
            destination=query.destination,
            duration=query.duration_days,
            travel_style=style,
            group_size=query.group_size,
            season=query.season,
            include_flights=query.include_flights
        )
        try:
            result = await estimate_budget(temp_query)
            if isinstance(result, dict) and 'bot_response' in result:
                results.append({
                    "style": style,
                    "total": result.get('total_budget', 0),
                    "per_person": result.get('per_person_budget', 0),
                    "response": result['bot_response']
                })
        except:
            continue

    if not results:
        return {
            "bot_response": """❌ **Budget Comparison Error**

Unable to compare budget options. Please check your destination and try again.""",
            "error": True
        }

    # Sort by total budget
    results.sort(key=lambda x: x['total'])

    comparison_text = f"""💰 **Budget Comparison for {query.destination}**

**📋 Trip Details:**
• Duration: {query.duration_days} days
• Group Size: {query.group_size} people
• Season: {query.season.title()}
• Flights: {'Included' if query.include_flights else 'Not included'}

---

## 💰 **Budget Options Comparison**

"""

    for result in results:
        style = result["style"].title()
        total = result["total"]
        per_person = result["per_person"]
        daily_avg = result.get("daily_average", 0)

        # Extract summary from response
        response_text = result["response"]
        # Find the total budget line
        import re
        total_match = re.search(r'\*\*Final Budget:\*\*\n•.*Total Trip Cost: \$(\d+)\.?\d+', response_text)
        if total_match:
            total_amount = total_match.group(1)
        else:
            total_amount = total

        comparison_text += f"""
### **{style} Style**
• **Total Trip Cost:** ${total:.2f} USD
• **Per Person:** ${per_person:.2f} USD
• **Daily Average:** ${daily_avg:.1f} USD

"""

    comparison_text += f"""
---

## 🎯 **Recommendations**

### 💰 **For Budget Travelers:**
• Choose hostels and guesthouses
• Use public transportation (trains, buses)
• Eat local street food and restaurants
• Visit free attractions and parks
• Consider off-peak season travel

### 💎 **For Mid-Range Travelers:**
• Stay in 3-star hotels or boutique accommodations
• Mix of public transport and occasional taxis
• Try both street food and mid-range restaurants
• Include some paid attractions and tours
• Shop at local markets for souvenirs

### 🌟 **For Luxury Travelers:**
• Book 4-5 star hotels with premium amenities
• Use private drivers or high-speed trains
• Experience fine dining and specialty restaurants
• Include premium tours and exclusive experiences
• Shop at department stores and luxury boutiques
• Consider travel insurance and premium services

## 💡 **Smart Tips to Save Money:**
• **Book accommodations 2-3 months in advance**
• **Consider shoulder season travel (April-May, September-October)**
• **Travel with friends to split costs**
• **Use discount apps and group tour packages**
• **Compare flight prices across different airlines**
• **Look for flight and hotel bundle deals**

Choose the option that best fits your budget and travel style! 🚀"""

    return {
        "bot_response": comparison_text,
        "comparisons": results,
        "destination": query.destination,
        "duration": query.duration_days,
        "group_size": query.group_size
    }

@router.get("/info")
async def get_budget_info():
    """Get budget estimator information"""
    return {
        "bot_response": """💰 **China Travel Budget Estimator**

Your comprehensive budget planning tool for China travel expenses!

**🎯 Core Features:**
• **Detailed Cost Breakdown** - Accommodation, food, transport, activities
• **Multi-Destination Support** - Covering all major Chinese cities
• **Flexible Pricing** - Budget, mid-range, luxury options
• **Group Size Benefits** - Discount calculations for groups
• **Seasonal Adjustments** - Peak, shoulder, off-peak pricing
• **Flight Cost Inclusion** - International airfare estimation

**💰 Budget Categories:**
• **Budget** ($40-80/day) - Hostels, local food, public transport
• **Mid-range** ($80-150/day) - 3-star hotels, mixed dining
• **Luxury** ($150-300+/day) - 4-5 star hotels, premium experiences

**🌟 Coverage Areas:**
• **Accommodation**: Hotels, hostels, guesthouses, apartments
• **Food & Dining**: Restaurants, street food, local specialties
• **Transportation**: Flights, trains, buses, taxis, private drivers
• **Activities**: Tours, attractions, experiences, cultural shows
• **Shopping**: Souvenirs, gifts, clothing, electronics
• **Miscellaneous**: Visa fees, insurance, daily expenses

**📊 Advanced Features:**
• **City-Specific Pricing** - Adjusted for cost of living differences
• **Seasonal Multipliers** - Peak vs. off-peak rate changes
• **Group Size Discounts** - Shared cost calculations
• **Flight Integration** - International airfare estimates
• **Budget Comparison** - Side-by-side option analysis
• **Money-Saving Tips** - Expert advice for cost reduction

**🎯 Popular Destinations:**
• **Beijing** - Higher accommodation costs (capital city)
• **Shanghai** - Premium dining and shopping costs
• **Chengdu** - Budget-friendly with great value
• **Xian** - Affordable with rich cultural experiences
• **Guangzhou** - Moderate costs with business advantages
• **Kunming** - Budget-friendly with pleasant weather
• **Lhasa** - Unique experiences with moderate costs

**💡 Planning Benefits:**
• Set realistic budget expectations
• Compare different travel styles
• Identify cost-saving opportunities
• Plan for group travel discounts
• Optimize travel timing
• Track expenses during trip

Plan your perfect China trip with accurate budget estimates! 🇨🇳""",
        "features": [
            "Detailed cost breakdown",
            "Multi-destination support",
            "Flexible pricing options",
            "Group size calculations",
            "Seasonal adjustments",
            "Flight cost estimates",
            "Budget comparison tool"
        ],
        "budget_ranges": {
            "budget": {"min": 40, "max": 80, "description": "Hostels, local food, public transport"},
            "mid_range": {"min": 80, "max": 150, "description": "3-star hotels, mixed dining, some taxis"},
            "luxury": {"min": 150, "max": 300, "description": "4-5 star hotels, fine dining, private transport"}
        },
        "covered_cities": list(CITY_FACTORS.keys())
    }
