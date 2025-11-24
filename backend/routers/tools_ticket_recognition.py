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
            
        # Basic extraction logic (can be improved with regex or NLP)
        extracted_info = {
            "raw_text": text,
            "origin": extract_origin(text),
            "destination": extract_destination(text),
            "date": extract_date(text),
            "ticket_number": extract_ticket_number(text)
        }
        
        return extracted_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

def extract_origin(text):
    # Simple heuristic: look for "From:" or "Departure:"
    match = re.search(r'(?:From|Departure|Origin)[:\s]+([A-Za-z\s]+)', text, re.IGNORECASE)
    return match.group(1).strip() if match else "Unknown"

def extract_destination(text):
    # Simple heuristic: look for "To:" or "Arrival:" or "Destination:"
    match = re.search(r'(?:To|Arrival|Destination)[:\s]+([A-Za-z\s]+)', text, re.IGNORECASE)
    return match.group(1).strip() if match else "Unknown"

def extract_date(text):
    # Look for common date formats
    match = re.search(r'(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})', text)
    return match.group(1) if match else "Unknown"

def extract_ticket_number(text):
    # Look for ticket number patterns
    match = re.search(r'(?:Ticket|Booking|Reference)\s*(?:No|Number|Ref)?[:\s]+([A-Z0-9]+)', text, re.IGNORECASE)
    return match.group(1) if match else "Unknown"
