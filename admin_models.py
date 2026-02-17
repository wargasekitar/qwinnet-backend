from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

# Admin User Models
class AdminUser(BaseModel):
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    role: str = "admin"
    created_at: datetime

class AdminSession(BaseModel):
    session_id: str
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime

# Google OAuth Session Data Response
class GoogleSessionData(BaseModel):
    id: str
    email: str
    name: str
    picture: str
    session_token: str
