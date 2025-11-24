from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import pytz
from datetime import datetime, timezone
import json
import re

router = APIRouter()

class TimeZoneRequest(BaseModel):
    query: Optional[str] = None  # Natural language query
    from_timezone: Optional[str] = None
    to_timezone: Optional[str] = None
    time_input: Optional[str] = None

# Comprehensive city-to-timezone mapping
CITY_TIMEZONES = {
    # North America
    "vancouver": "America/Vancouver",
    "seattle": "America/Los_Angeles",
    "los angeles": "America/Los_Angeles",
    "san francisco": "America/Los_Angeles",
    "las vegas": "America/Los_Angeles",
    "phoenix": "America/Phoenix",
    "denver": "America/Denver",
    "chicago": "America/Chicago",
    "houston": "America/Chicago",
    "dallas": "America/Chicago",
    "new york": "America/New_York",
    "boston": "America/New_York",
    "washington": "America/New_York",
    "miami": "America/New_York",
    "toronto": "America/Toronto",
    "montreal": "America/Montreal",
    "mexico city": "America/Mexico_City",
    
    # South America
    "sao paulo": "America/Sao_Paulo",
    "buenos aires": "America/Argentina/Buenos_Aires",
    "rio de janeiro": "America/Sao_Paulo",
    
    # Europe
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "rome": "Europe/Rome",
    "madrid": "Europe/Madrid",
    "amsterdam": "Europe/Amsterdam",
    "brussels": "Europe/Brussels",
    "moscow": "Europe/Moscow",
    "istanbul": "Europe/Istanbul",
    "athens": "Europe/Athens",
    "dublin": "Europe/Dublin",
    "lisbon": "Europe/Lisbon",
    
    # Asia
    "beijing": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "hong kong": "Asia/Hong_Kong",
    "tokyo": "Asia/Tokyo",
    "seoul": "Asia/Seoul",
    "singapore": "Asia/Singapore",
    "bangkok": "Asia/Bangkok",
    "mumbai": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
    "dubai": "Asia/Dubai",
    "jakarta": "Asia/Jakarta",
    "manila": "Asia/Manila",
    "taipei": "Asia/Taipei",
    "kuala lumpur": "Asia/Kuala_Lumpur",
    
    # Oceania
    "sydney": "Australia/Sydney",
    "melbourne": "Australia/Melbourne",
    "brisbane": "Australia/Brisbane",
    "auckland": "Pacific/Auckland",
    "perth": "Australia/Perth",
    
    # Africa
    "cairo": "Africa/Cairo",
    "johannesburg": "Africa/Johannesburg",
    "lagos": "Africa/Lagos",
    "nairobi": "Africa/Nairobi"
}

def parse_natural_query(query: str) -> dict:
    """
    Parse natural language queries like:
    - "Vancouver time to Beijing time"
    - "What time is it in Tokyo"
    - "Current time in London vs New York"
    """
    query_lower = query.lower().strip()
    
    # Pattern 1: "X time to Y time" or "X to Y"
    pattern1 = r"(?:time in |)([a-z\s]+?)\s+(?:time\s+)?(?:to|vs|versus|and)\s+(?:time in |)([a-z\s]+?)(?:\s+time|$)"
    match = re.search(pattern1, query_lower)
    
    if match:
        city1 = match.group(1).strip()
        city2 = match.group(2).strip()
        
        # Find timezone for cities
        tz1 = CITY_TIMEZONES.get(city1)
        tz2 = CITY_TIMEZONES.get(city2)
        
        if tz1 and tz2:
            return {
                "from_city": city1.title(),
                "to_city": city2.title(),
                "from_tz": tz1,
                "to_tz": tz2,
                "query_type": "comparison"
            }
    
    # Pattern 2: "What time is it in X" / "Current time in X"
    pattern2 = r"(?:what time is it in|current time in|time in)\s+([a-z\s]+?)(?:\s|$)"
    match = re.search(pattern2, query_lower)
    
    if match:
        city = match.group(1).strip()
        tz = CITY_TIMEZONES.get(city)
        
        if tz:
            return {
                "to_city": city.title(),
                "to_tz": tz,
                "query_type": "single"
            }
    
    # Pattern 3: Single city name
    for city, tz in CITY_TIMEZONES.items():
        if city in query_lower:
            return {
                "to_city": city.title(),
                "to_tz": tz,
                "query_type": "single"
            }
    
    return None

def get_current_time_in_zone(tz_name: str) -> dict:
    """Get current time in a timezone"""
    try:
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        
        # Calculate UTC offset
        offset = now.strftime('%z')
        offset_formatted = f"{offset[:3]}:{offset[3:]}" if offset else "+00:00"
        
        return {
            "time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "date": now.strftime("%A, %B %d, %Y"),
            "time_12h": now.strftime("%I:%M %p"),
            "timezone": tz_name,
            "offset": offset_formatted,
            "day_of_week": now.strftime("%A"),
            "datetime_obj": now
        }
    except Exception as e:
        return {"error": str(e)}

@router.post("/convert")
async def convert_timezone_endpoint(request: TimeZoneRequest):
    """
    Convert time between timezones with natural language support
    """
    
    # Case 1: Natural language query
    if request.query:
        parsed = parse_natural_query(request.query)
        
        if not parsed:
            return {
                "bot_response": f"""🌍 **Time Zone Converter**

I couldn't understand: "{request.query}"

**Try these formats:**
• "Vancouver time to Beijing time"
• "What time is it in Tokyo"
• "London vs New York"
• "Current time in Paris"

**Supported cities:** Vancouver, New York, London, Tokyo, Beijing, Sydney, Paris, and 50+ more!""",
                "suggestions": [
                    "Vancouver time to Beijing time",
                    "What time is it in Tokyo",
                    "London vs New York"
                ]
            }
        
        # Handle comparison query
        if parsed["query_type"] == "comparison":
            time1 = get_current_time_in_zone(parsed["from_tz"])
            time2 = get_current_time_in_zone(parsed["to_tz"])
            
            if "error" in time1 or "error" in time2:
                return {
                    "bot_response": f"❌ Error getting timezone information",
                    "error": time1.get("error") or time2.get("error")
                }
            
            # Calculate time difference
            diff = (time2["datetime_obj"] - time1["datetime_obj"]).total_seconds() / 3600
            diff_hours = int(diff)
            diff_mins = int((diff - diff_hours) * 60)
            
            if diff_hours > 0:
                diff_str = f"+{diff_hours}h {diff_mins}min" if diff_mins > 0 else f"+{diff_hours}h"
            elif diff_hours < 0:
                diff_str = f"{diff_hours}h {diff_mins}min" if diff_mins < 0 else f"{diff_hours}h"
            else:
                diff_str = "Same time" if diff_mins == 0 else f"{diff_mins}min"
            
            response_text = f"""🌍 **Time Zone Comparison**

📍 **{parsed["from_city"]}**
🕐 {time1["time_12h"]}
📅 {time1["date"]}
🌐 {time1["timezone"]} (UTC{time1["offset"]})

📍 **{parsed["to_city"]}**
🕐 {time2["time_12h"]}
📅 {time2["date"]}
🌐 {time2["timezone"]} (UTC{time2["offset"]})

⏰ **Time Difference**: {diff_str}

💡 When it's {time1["time_12h"]} in {parsed["from_city"]}, it's {time2["time_12h"]} in {parsed["to_city"]}."""

            return {
                "bot_response": response_text,
                "from_city": parsed["from_city"],
                "to_city": parsed["to_city"],
                "from_time": time1,
                "to_time": time2,
                "difference": diff_str
            }
        
        # Handle single city query
        else:
            time_info = get_current_time_in_zone(parsed["to_tz"])
            
            if "error" in time_info:
                return {
                    "bot_response": f"❌ Error: {time_info['error']}"
                }
            
            response_text = f"""🌍 **Current Time**

📍 **{parsed["to_city"]}**
🕐 {time_info["time_12h"]}
📅 {time_info["date"]}
🌐 {time_info["timezone"]} (UTC{time_info["offset"]})

✨ Current local time in {parsed["to_city"]}"""

            return {
                "bot_response": response_text,
                "city": parsed["to_city"],
                "time_info": time_info
            }
    
    # Case 2: No query provided - show help
    else:
        return {
            "bot_response": """🌍 **Time Zone Converter**

Convert times between cities worldwide!

**Usage:**
• "Vancouver time to Beijing time"
• "What time is it in Tokyo?"
• "London vs New York"
• "Current time in Paris"

**Popular Cities:**
• **Americas**: Vancouver, New York, Toronto, Los Angeles
• **Europe**: London, Paris, Berlin, Moscow
• **Asia**: Beijing, Tokyo, Singapore, Dubai
• **Oceania**: Sydney, Melbourne, Auckland

Ask about any major city to get started! 🕐""",
            "suggestions": [
                "Vancouver time to Beijing time",
                "What time is it in Tokyo",
                "London vs New York",
                "Current time in Sydney"
            ]
        }

@router.get("/info")
async def get_timezone_info_endpoint():
    """
    Get timezone converter information
    """
    current_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    return {
        "bot_response": f"""🌍 **Time Zone Converter**

Convert times between cities worldwide with natural language!

**Features:**
• Natural language queries
• 60+ major cities supported
• Real-time conversion
• Time difference calculation

**Examples:**
• "Vancouver time to Beijing time"
• "What time is it in Tokyo?"
• "London vs New York time"

**Current UTC**: {current_utc}

Perfect for global coordination! 🌐""",
        "total_cities": len(CITY_TIMEZONES),
        "supported_cities": sorted(CITY_TIMEZONES.keys()),
        "current_utc": current_utc
    }