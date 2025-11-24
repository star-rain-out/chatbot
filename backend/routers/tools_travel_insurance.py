from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json

router = APIRouter()

class InsuranceQuery(BaseModel):
    travel_type: Optional[str] = None  # leisure, business, adventure, senior
    duration: Optional[str] = None  # 1week, 2weeks, 1month, 3months
    destination: Optional[str] = None  # domestic, international
    coverage_type: Optional[str] = None  # medical, baggage, trip_cancel, comprehensive
    age_group: Optional[str] = None  # youth, adult, senior, family

# Insurance Company and Product Database
INSURANCE_COMPANIES = {
    "domestic": [
        {
            "company": "Ping An Insurance",
            "product": "Domestic Travel Insurance",
            "coverage_types": ["Accidental Medical", "Emergency Rescue", "Baggage Delay", "Trip Change"],
            "price_range": {"1week": "50-100", "2weeks": "80-150", "1month": "150-300"},
            "highlights": ["24h Global Rescue", "Full Medical Reimbursement", "Lost Baggage Compensation"],
            "contact": "95511",
            "online_purchase": True
        },
        {
            "company": "PICC",
            "product": "Peace of Mind Domestic Travel",
            "coverage_types": ["Accidental Injury", "Medical Coverage", "Personal Liability", "Rescue Service"],
            "price_range": {"1week": "40-80", "2weeks": "70-120", "1month": "120-250"},
            "highlights": ["State-owned Brand", "Fast Claims", "Wide Coverage"],
            "contact": "95518",
            "online_purchase": True
        },
        {
            "company": "CPIC",
            "product": "Joyful China Travel Insurance",
            "coverage_types": ["Comprehensive Accident", "Medical Rescue", "Trip Protection", "Personal Property"],
            "price_range": {"1week": "45-90", "2weeks": "75-130", "1month": "140-280"},
            "highlights": ["Comprehensive Liability", "Rich Value-added Services", "Reasonable Price"],
            "contact": "95500",
            "online_purchase": True
        }
    ],
    "international": [
        {
            "company": "Ping An Insurance",
            "product": "Global Travel Insurance",
            "coverage_types": ["Overseas Medical", "Emergency Rescue", "Flight Delay", "Trip Cancellation"],
            "price_range": {"1week": "150-300", "2weeks": "250-500", "1month": "400-800"},
            "highlights": ["Direct Billing Medical", "Multi-language Rescue", "Global Medical Network"],
            "contact": "95511",
            "online_purchase": True
        },
        {
            "company": "AIG",
            "product": "Travel Guard",
            "coverage_types": ["Medical Coverage", "Travel Inconvenience", "Personal Property", "Emergency Rescue"],
            "price_range": {"1week": "120-250", "2weeks": "200-400", "1month": "350-700"},
            "highlights": ["US Background", "Global Service Network", "Fast & Easy Claims"],
            "contact": "400-820-3588",
            "online_purchase": True
        },
        {
            "company": "Allianz",
            "product": "Allianz Global Travel",
            "coverage_types": ["Health Protection", "Travel Protection", "Property Protection", "Rescue Service"],
            "price_range": {"1week": "130-280", "2weeks": "220-450", "1month": "380-750"},
            "highlights": ["German Quality", "Global Rescue Network", "High-end Medical Service"],
            "contact": "400-800-1230",
            "online_purchase": True
        }
    ]
}

@router.post("/recommend")
async def recommend_insurance(query: InsuranceQuery):
    """Recommend Travel Insurance"""
    if not query.travel_type and not query.destination and not query.duration:
        return {
            "bot_response": """🛡️ China Travel Insurance Guide

Providing comprehensive insurance protection advice for your China trip!

**🎯 Insurance Types:**
• **Leisure** - Sightseeing, family trips
• **Business** - Business meetings, events
• **Adventure** - Outdoor exploration, extreme sports
• **Senior** - Exclusive protection for seniors

**🌍 Coverage Scope:**
• **Domestic** - Mainland China
• **International** - Overseas travel

**⏱️ Trip Duration:**
• **Short-term** - 1-2 weeks
• **Mid-term** - 1 month
• **Long-term** - 3 months+

**🛡️ Coverage Content:**
• **Accidental Medical** - Sickness, accidental injury medical expenses
• **Emergency Rescue** - 24h global rescue
• **Trip Protection** - Flight delay, trip cancellation
• **Property Protection** - Lost baggage, damaged belongings
• **Personal Liability** - Third-party liability compensation

**🔍 High-risk Activities:**
• Hiking, skiing, diving etc. require extra coverage

Please tell us your travel plan for professional insurance advice! ✈️""",
            "suggestions": [
                "Family travel insurance recommendation",
                "Senior travel insurance plan",
                "Outdoor sports insurance consultation",
                "International travel insurance comparison"
            ]
        }

    # Get recommended insurance
    companies = INSURANCE_COMPANIES.get(query.destination, INSURANCE_COMPANIES["domestic"])
    duration = query.duration or "1week"

    # Build recommendation result
    result_text = f"""🛡️ **Travel Insurance Recommendations**

**🎯 Your Trip Info:**
• Type: {query.travel_type or 'Leisure'}
• Destination: {query.destination or 'Domestic'}
• Duration: {query.duration or '1 Week'}

## 📋 Recommended Products"""

    for i, company in enumerate(companies[:3], 1):
        price_range = company["price_range"].get(duration, "TBD")

        result_text += f"""

### {i}. {company['company']} - {company['product']}

💰 **Premium Range:** ¥{price_range}
📞 **Hotline:** {company['contact']}
🌐 **Online Purchase:** {'✅ Supported' if company['online_purchase'] else '❌ Not Supported'}

🛡️ **Key Coverage:**"""
        for coverage in company['coverage_types']:
            result_text += f"\n  • {coverage}"

        result_text += f"\n\n✨ **Highlights:**"
        for highlight in company['highlights']:
            result_text += f"\n  • {highlight}"

    result_text += f"""

## 📊 Estimated Cost

Based on your {duration} trip, estimated insurance cost:
• **Basic**: ¥100-200
• **Standard**: ¥200-400
• **Comprehensive**: ¥300-600

## 🎯 Special Reminders

**Extra Coverage for High-risk Sports:**
• 🏔️ Hiking, Climbing (Altitude 3500m+)
• 🎿 Skiing, Skating
• 🤿 Diving, Bungee Jumping
• 🪂 Skydiving, Paragliding

**Senior Insurance Notes:**
• Age limit usually 70-80 years
• Health declaration required
• Higher premiums
• Lower coverage limits

**Family Trip Suggestions:**
• Buy family package
• Discounts for children
• Unified management

## 🛒 Purchase Channels

**Official Channels:**
• Insurance company websites
• Official Apps
• Customer service hotlines

**Third-party Platforms:**
• Alipay - Insurance
• WeChat - Insurance Services
• Trip.com, Qunar etc.
• Insurance agencies

## 📝 Booking Tips

1. **Read Terms Carefully** - Understand coverage and exclusions
2. **Declare Honestly** - Health status, travel plans etc.
3. **Keep Documents** - Policy, invoices, claim documents
4. **Emergency Contacts** - Save in phone
5. **Know Claim Process** - How to apply after incident

## 🆘 Emergency Handling

**In Case of Emergency:**
1. Call rescue number immediately
2. Contact insurance customer service
3. Keep relevant evidence and receipts
4. Seek medical help and keep records
5. Apply for claim as guided

Choose the right insurance for a worry-free China trip! 🌟"""

    return {
        "bot_response": result_text,
        "travel_type": query.travel_type,
        "destination": query.destination,
        "duration": query.duration
    }

@router.post("/compare")
async def compare_insurance():
    """Insurance Product Comparison"""
    return {
        "bot_response": """🛡️ **Travel Insurance Comparison**

## Domestic Travel Insurance

| Company | Product | 1 Week Premium | Key Features | Hotline |
|---------|---------|----------------|--------------|---------|
| Ping An | Domestic Travel | ¥50-100 | 24h Global Rescue | 95511 |
| PICC | Peace of Mind | ¥40-80 | State-owned Brand | 95518 |
| CPIC | Joyful China | ¥45-90 | Rich Value-added | 95500 |

## International Travel Insurance

| Company | Product | 1 Week Premium | Key Features | Hotline |
|---------|---------|----------------|--------------|---------|
| Ping An | Global Travel | ¥150-300 | Direct Billing | 95511 |
| AIG | Travel Guard | ¥120-250 | US Background | 400-820-3588 |
| Allianz | Global Travel | ¥130-280 | German Quality | 400-800-1230 |

Choose the best product for your needs! 🎯"""
    }

@router.get("/info")
async def get_insurance_info():
    """Get Insurance Guide Feature Introduction"""
    return {
        "bot_response": """🛡️ **China Travel Insurance Guide**

Your travel safety expert, providing comprehensive insurance advice!

**🎯 Core Features:**
• **Smart Recommendation** - Best insurance based on itinerary
• **Product Comparison** - Detailed comparison of major companies
• **Cost Analysis** - Detailed premium estimates
• **Risk Assessment** - Identify potential travel risks
• **Claim Guidance** - Post-incident claim process guide

**🛡️ Coverage Types:**
• **Accidental Medical** - Sickness, accidental injury expenses
• **Emergency Rescue** - 24h global medical rescue
• **Trip Delay** - Flight delay, lost baggage
• **Personal Liability** - Third-party injury/property damage
• **High-risk Sports** - Special coverage for outdoor adventures

**🌟 Service Highlights:**
• Professional consultant advice
• Multi-company product comparison
• Transparent price and terms
• Detailed claim process guide
• Risk assessment and prevention tips

Travel worry-free in China! ✈️🛡️"""
    }
