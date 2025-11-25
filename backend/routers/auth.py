from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
import json
import os
import shutil

# Create router object
router = APIRouter()
security = HTTPBearer()

# Password encryption context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret key (should be obtained from environment variables in production)
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# User data storage file path
USERS_FILE = "users.json"

# Data models
class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    phone_number: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user_name: str

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def load_users() -> Dict:
    """Load user data from file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users_data: Dict):
    """Save user data to file"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency function to get current user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    users = load_users()
    user = users.get(email)
    if user is None:
        raise credentials_exception
    return user

# API endpoints
@router.post("/register", response_model=dict)
async def register(user: UserRegister):
    """User Registration - Independent Registration API"""
    users = load_users()

    # Check if email already exists
    if user.email in users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered"
        )

    # Check email format (simple validation)
    if "@" not in user.email or "." not in user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Check password length
    if len(user.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    users[user.email] = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hashed_password,
        "phone_number": user.phone_number,
        "avatar_url": None,
        "created_at": datetime.utcnow().isoformat()
    }

    # Save user data
    save_users(users)

    return {
        "message": "User registered successfully",
        "email": user.email,
        "name": user.name
    }

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """User Login - Independent Login API"""
    users = load_users()

    # Verify user
    db_user = users.get(user.email)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "name": db_user["name"]},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_name": db_user["name"]
    }

@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Get current user information - Independent user verification API"""
    return {
        "email": current_user["email"],
        "name": current_user["name"],
        "phone_number": current_user.get("phone_number"),
        "avatar_url": current_user.get("avatar_url"),
        "created_at": current_user["created_at"]
    }

@router.put("/me")
async def update_profile(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    """Update user profile"""
    users = load_users()
    user_email = current_user["email"]
    
    if user_email not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields
    if user_update.name:
        users[user_email]["name"] = user_update.name
    if user_update.phone_number:
        users[user_email]["phone_number"] = user_update.phone_number
    if user_update.avatar_url:
        users[user_email]["avatar_url"] = user_update.avatar_url
    if user_update.password:
        users[user_email]["hashed_password"] = get_password_hash(user_update.password)
        
    save_users(users)
    
    return {
        "message": "Profile updated successfully",
        "user": {
            "name": users[user_email]["name"],
            "email": user_email,
            "phone_number": users[user_email].get("phone_number"),
            "avatar_url": users[user_email].get("avatar_url")
        }
    }

@router.post("/upload_avatar")
async def upload_avatar(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    """Upload user avatar"""
    try:
        # Create directory if not exists
        os.makedirs("static/avatars", exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"avatar_{current_user['email']}{file_extension}"
        file_path = f"static/avatars/{filename}"
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Return URL
        avatar_url = f"http://103.189.140.199:8000/static/avatars/{filename}"
        
        # Update user profile with new avatar URL
        users = load_users()
        if current_user["email"] in users:
            users[current_user["email"]]["avatar_url"] = avatar_url
            save_users(users)
            
        return {"avatar_url": avatar_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))