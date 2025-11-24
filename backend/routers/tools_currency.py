from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
import re
from datetime import datetime

router = APIRouter()

class CurrencyRequest(BaseModel):
    query: str

# Mock data as fallback
MOCK_RATES = {
    'USD': {'CNY': 7.25, 'EUR': 0.92, 'GBP': 0.79, 'JPY': 149.50, 'KRW': 1320.50, 'HKD': 7.82, 'CAD': 1.36},
    'CNY': {'USD': 0.138, 'EUR': 0.127, 'GBP': 0.109, 'JPY': 20.63, 'KRW': 182.22, 'HKD': 1.079, 'CAD': 0.188},
    'EUR': {'USD': 1.087, 'CNY': 7.87, 'GBP': 0.86, 'JPY': 162.50, 'KRW': 1435.22, 'HKD': 8.50, 'CAD': 1.48},
}

# Currency name mapping
CURRENCY_NAMES = {
    'USD': 'USD', 'CNY': 'CNY', 'EUR': 'EUR', 'GBP': 'GBP', 'JPY': 'JPY', 'KRW': 'KRW', 'HKD': 'HKD', 'CAD': 'CAD',
    '美元': 'USD', '人民币': 'CNY', '欧元': 'EUR', '英镑': 'GBP', '日元': 'JPY', '韩元': 'KRW', '港币': 'HKD', '加元': 'CAD'
}

async def get_exchange_rate(from_currency: str, to_currency: str) -> Optional[Dict[str, Any]]:
    """
    Fetch real-time exchange rate from exchangerate-api.com
    """
    if from_currency == to_currency:
        return {"rate": 1.0, "source": "same currency", "timestamp": datetime.now().isoformat()}
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if to_currency not in data.get("rates", {}):
                return {"error": f"{to_currency} not found in rates"}
            
            return {
                "rate": data["rates"][to_currency],
                "source": "exchangerate-api.com",
                "timestamp": data.get("date", datetime.now().strftime("%Y-%m-%d"))
            }
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        # Fallback to mock data
        if from_currency in MOCK_RATES and to_currency in MOCK_RATES.get(from_currency, {}):
            return {
                "rate": MOCK_RATES[from_currency][to_currency],
                "source": "fallback data (API unavailable)",
                "timestamp": datetime.now().strftime("%Y-%m-%d")
            }
        return {"error": str(e)}

def extract_currency_info(query: str):
    """Extract currency information from user query"""
    query = query.replace(' ', '').replace('等于多少', '=').replace('等于', '=')
    
    # Regex pattern to match amount and currency
    pattern = r'(\d+\.?\d*)([美元人民币欧元英镑日元韩元港币加元USDCEURGBPJPYKRWHKDCAD]+)=?([美元人民币欧元英镑日元韩元港币加元USDCEURGBPJPYKRWHKDCAD]+)?'
    
    match = re.search(pattern, query, re.IGNORECASE)
    
    if match:
        amount = float(match.group(1))
        from_currency = match.group(2).upper()
        to_currency = match.group(3)
        
        if to_currency:
            to_currency = to_currency.upper()
        else:
            # If no target currency specified, default to CNY
            to_currency = 'CNY'
        
        # Convert currency codes
        from_currency = CURRENCY_NAMES.get(from_currency, from_currency)
        to_currency = CURRENCY_NAMES.get(to_currency, to_currency)
        
        return amount, from_currency, to_currency
    
    return None, None, None

@router.post("/convert")
async def convert_currency(request: CurrencyRequest):
    """
    Currency conversion API with real-time rates
    """
    query = request.query
    
    # Extract currency information
    amount, from_currency, to_currency = extract_currency_info(query)
    
    if not amount or not from_currency:
        return {
            "bot_response": f"🤔 Sorry, I didn't understand your query. Please try these formats:\n• How much is 100 USD in CNY\n• Convert 50 EUR to CNY\n• 1000 JPY to KRW",
            "suggestions": ["How much is 100 USD in CNY", "Convert 50 EUR to CNY", "1000 JPY to KRW"]
        }
    
    # Get real-time exchange rate
    rate_data = await get_exchange_rate(from_currency, to_currency)
    
    if rate_data.get("error"):
        return {
            "bot_response": f"❌ Sorry, unable to get exchange rate for {from_currency} to {to_currency}.\nError: {rate_data['error']}\n\nPlease try again later.",
            "error": rate_data["error"]
        }
    
    # Calculate conversion
    try:
        rate = rate_data["rate"]
        result = amount * rate
        source = rate_data["source"]
        timestamp = rate_data["timestamp"]
        
        # Format output
        from_name = CURRENCY_NAMES.get(from_currency, from_currency)
        to_name = CURRENCY_NAMES.get(to_currency, to_currency)
        
        # Adjust decimal places based on currency type
        if to_currency in ['JPY', 'KRW']:
            formatted_result = f"{result:.0f}"
        elif to_currency in ['USD', 'EUR', 'GBP', 'CAD', 'HKD', 'CNY']:
            formatted_result = f"{result:.2f}"
        else:
            formatted_result = f"{result:.2f}"
        
        response_text = f"""💱 **Currency Conversion Result**

{amount:g} {from_name} = **{formatted_result} {to_name}**

📊 **Exchange Rate**: 1 {from_name} = {rate:.4f} {to_name}
🔄 **Source**: {source}
⏰ **Rate Date**: {timestamp}

💡 Data is for reference only. Actual transactions follow bank exchange rates."""

        return {
            "bot_response": response_text,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "result": result,
            "rate": rate,
            "source": source,
            "timestamp": timestamp
        }
    
    except Exception as e:
        return {
            "bot_response": f"❌ Exchange rate calculation error: {str(e)}\n\nPlease try again later or re-enter your query.",
            "error": str(e)
        }