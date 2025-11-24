from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json

router = APIRouter()

class VisaQuery(BaseModel):
    nationality: str
    visa_type: Optional[str] = None  # tourist, business, student, work
    duration: Optional[str] = None  # 30days, 90days, 1year

@router.post("/query")
async def query_visa_info(query: VisaQuery):
    """Query Visa Information"""
    nationality = query.nationality.strip()

    if not nationality:
        return {
            "bot_response": """🛂 **China Visa Information Query**

Providing you with the latest China visa policies and application guidelines!

**🎭 Visa Types:**
• **Tourist Visa (L)** - Sightseeing, visiting family/friends
• **Business Visa (M)** - Commercial trade activities
• **Student Visa (X)** - Long/Short term study
• **Work Visa (Z)** - Working in China

**📋 Application Materials:**
• Valid Passport
• Visa Application Form
• Photo Requirements
• Invitation Letter or Itinerary

**⏰ Processing Time:**
• Regular Service: 4-6 working days
• Express Service: 2-3 working days

Please enter your nationality to query specific requirements! 🌍""",
            "suggestions": [
                "US Citizen Tourist Visa",
                "Japan Business Visa Application",
                "Korea Student Visa Requirements",
                "Visa Documents Checklist"
            ]
        }

    # Basic visa info response
    result_text = f"""🛂 **China Visa Information - {nationality}**

**📋 Visa Type:** {query.visa_type or 'Tourist Visa'}
**⏰ Duration of Stay:** {query.duration or '30 Days'}

## 📝 Application Materials Checklist
1. **Original Passport** (Valid for at least 6 months)
2. **Visa Application Form** (Completed and signed)
3. **Photo** (2-inch color photo with white background)
4. **Round-trip Flight Booking**
5. **Hotel Reservation**
6. **Travel Itinerary**
7. **Proof of Funds** (Bank statements)

## 💰 Visa Fees
• **Visa Fee**: Varies by nationality (approx. $30-$140)
• **Service Fee**: Approx. $20-$30
• **Express Fee**: Approx. $30 (if applicable)

## ⏱️ Processing Time
• **Regular Processing**: 4-6 working days
• **Express Processing**: 2-3 working days

## 📝 Application Process
1. Prepare application materials
2. Complete online application form
3. Make an appointment for submission
4. Submit materials at the Visa Center
5. Wait for review results
6. Collect passport and visa

## ⚠️ Important Notes
• Application materials must be authentic and valid
• Arrive on time for your appointment
• Visa validity is subject to approval
• Cooperate with border inspection upon entry

Wishing you a smooth application! ✈️"""

    return {
        "bot_response": result_text,
        "nationality": nationality,
        "visa_type": query.visa_type
    }

@router.get("/info")
async def get_visa_info():
    """Get Visa Query Feature Introduction"""
    return {
        "bot_response": """🛂 **China Visa Information Assistant**

Your professional consultant for visa applications, providing the latest and most accurate China visa information!

**🎯 Services:**
• Visa requirements for citizens of various countries
• Detailed checklist of application materials
• Visa fees and processing times
• Application process guidance
• Latest policy updates

**📋 Visa Types:**
• L Visa (Tourist)
• M Visa (Business)
• X Visa (Student)
• Z Visa (Work)

Start your China journey with a smooth visa application! 🌟"""
    }
