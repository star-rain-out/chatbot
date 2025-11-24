from fastapi import APIRouter, UploadFile, File, HTTPException
import PyPDF2
import io
import re

router = APIRouter()

@router.post("/upload")
async def upload_ticket(file: UploadFile = File(...)):
    """
    Upload a PDF ticket and extract information.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        # Read PDF content
        content = await file.read()
        pdf_file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
            
        # Enhanced extraction logic
        extracted_info = {
            "passenger_name": extract_passenger_name(text),
            "airline": extract_airline(text),
            "flight_number": extract_flight_number(text),
            "origin": extract_origin(text),
            "destination": extract_destination(text),
            "departure_date": extract_date(text),
            "departure_time": extract_departure_time(text),
            "arrival_time": extract_arrival_time(text),
            "confirmation_number": extract_confirmation_number(text),
            "booking_reference": extract_booking_reference(text),
        }
        
        return extracted_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

def extract_passenger_name(text):
    # Look for passenger name patterns
    patterns = [
        r'Passenger[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'Name[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'Traveler[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return "Not found"

def extract_airline(text):
    # Look for airline name
    airlines = ['Pacific Coastal Airlines', 'Air Canada', 'WestJet', 'United', 'Delta', 'American Airlines']
    for airline in airlines:
        if airline in text:
            return airline
    # Fallback pattern
    match = re.search(r'Airlines?[:\s]*([A-Za-z\s]+)', text, re.IGNORECASE)
    return match.group(1).strip() if match else "Not found"

def extract_flight_number(text):
    # Look for flight number patterns (e.g., AA123, WJ456)
    match = re.search(r'\b([A-Z]{2}\s*\d{3,4})\b', text)
    return match.group(1) if match else "Not found"

def extract_origin(text):
    # Enhanced origin extraction - look for city names with airport codes
    patterns = [
        r'([A-Za-z\s,]+)\s*\([A-Z]{3}\)',  # City (IATA code)
        r'Departs[:\s]+[A-Za-z,\s]+\d{1,2}\s+[A-Za-z]+\s+([A-Za-z\s,]+)\s*\(',
        r'From[:\s]+([A-Za-z\s,]+?)(?:\s+to|\n)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            city = match.group(1).strip()
            # Clean up common artifacts
            city = re.sub(r'\s+to\s+.*', '', city, flags=re.IGNORECASE)
            return city
    return "Not found"

def extract_destination(text):
    # Look for "to Victoria" or similar patterns
    patterns = [
        r'(?:to|Arrival|Arrives)\s+([A-Za-z\s]+)',
        r'Flight to\s+([A-Za-z\s]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            dest = match.group(1).strip()
            # Clean up - take first word or two
            dest = ' '.join(dest.split()[:2])
            return dest
    return "Not found"

def extract_date(text):
    # Look for various date formats
    patterns = [
        r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})',  # 21 Dec 2025
        r'(\d{4}-\d{2}-\d{2})',  # 2025-12-21
        r'(\d{2}/\d{2}/\d{4})',  # 12/21/2025
        r'(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)[a-z]*,?\s+(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*)',  # Sun, 21 Dec
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "Not found"

def extract_departure_time(text):
    # Look for departure time (e.g., 17:25)
    match = re.search(r'(?:Departs?|Departure)[:\s]+[A-Za-z,\s]*(\d{1,2}:\d{2})', text, re.IGNORECASE)
    if match:
        return match.group(1)
    # Alternative pattern
    match = re.search(r'(\d{1,2}:\d{2})\s*Departs?', text, re.IGNORECASE)
    return match.group(1) if match else "Not found"

def extract_arrival_time(text):
    # Look for arrival time
    match = re.search(r'(?:Arrives?|Arrival)[:\s]+[A-Za-z,\s]*(\d{1,2}:\d{2})', text, re.IGNORECASE)
    if match:
        return match.group(1)
    # Alternative pattern
    match = re.search(r'(\d{1,2}:\d{2})\s*Arrives?', text, re.IGNORECASE)
    return match.group(1) if match else "Not found"

def extract_confirmation_number(text):
    # Look for confirmation number
    patterns = [
        r'Confirmation[:\s]+([A-Z0-9]+)',
        r'Confirmation\s+(?:No|Number|Code)[:\s]+([A-Z0-9]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return "Not found"

def extract_booking_reference(text):
    # Look for booking reference or itinerary number
    patterns = [
        r'(?:Expedia|Booking)\s+itinerary[:\s]+(\d+)',
        r'Booking\s+(?:reference|number)[:\s]+([A-Z0-9]+)',
        r'Itinerary[:\s]+([A-Z0-9]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return "Not found"
