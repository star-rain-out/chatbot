@echo off
echo Starting Backend...
cd backend
uvicorn main:app --reload --port 8000