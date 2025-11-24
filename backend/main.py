from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import various independent modules
from routers import (
    auth, chat_general, tools_weather, tools_translate, tools_currency,
    tools_travel, tools_landmark, tools_social_media, tools_timezone,
    tools_attraction_tickets, tools_hotel_booking, tools_transport_route,
    tools_china_experience, tools_visa_info, tools_travel_insurance,
    tools_budget_estimator,
    tools_ticket_recognition
)
from fastapi.staticfiles import StaticFiles
import os

# Create static directory if it doesn't exist
if not os.path.exists("static/avatars"):
    os.makedirs("static/avatars")

from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


app = FastAPI()

# Allow cross-origin requests (required for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes, each module has independent path prefix
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(chat_general.router, prefix="/api/chat", tags=["General Chat"])
app.include_router(tools_weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(tools_translate.router, prefix="/api/translate", tags=["Translation"])
app.include_router(tools_currency.router, prefix="/api/currency", tags=["Currency"])
app.include_router(tools_travel.router, prefix="/api/travel", tags=["Travel Q&A"])
app.include_router(tools_landmark.router, prefix="/api/landmark", tags=["Landmark Recognition"])
app.include_router(tools_social_media.router, prefix="/api/social_media", tags=["Social Media Caption"])
app.include_router(tools_timezone.router, prefix="/api/timezone", tags=["Time Zone Converter"])

# New China tourism features
app.include_router(tools_attraction_tickets.router, prefix="/api/attraction_tickets", tags=["Attraction Tickets"])
app.include_router(tools_hotel_booking.router, prefix="/api/hotel_recommendations", tags=["Hotel Recommendations"])
app.include_router(tools_transport_route.router, prefix="/api/transport_route", tags=["Transport Route"])
app.include_router(tools_china_experience.router, prefix="/api/china_experience", tags=["China Experience"])
app.include_router(tools_visa_info.router, prefix="/api/visa_info", tags=["Visa Information"])
app.include_router(tools_travel_insurance.router, prefix="/api/travel_insurance", tags=["Travel Insurance"])
app.include_router(tools_budget_estimator.router, prefix="/api/budget_estimator", tags=["Budget Estimator"])
app.include_router(tools_ticket_recognition.router, prefix="/api/ticket_recognition", tags=["Ticket Recognition"])

@app.get("/")
def root():
    return {"message": "Backend is running"}
    # Reload for ticket recognition updates

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
