from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
import uuid

# Coverage Inquiry Models
class CoverageInquiryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    address: str = Field(..., min_length=1, max_length=500)
    city: str = Field(..., min_length=1, max_length=100)

class CoverageInquiry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    phone: str
    address: str
    city: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"  # pending, contacted, completed

# Package Inquiry Models
class PackageInquiryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    address: str = Field(..., min_length=1, max_length=500)
    package_id: int = Field(..., ge=1, le=3)
    message: Optional[str] = Field(None, max_length=1000)

class PackageInquiry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: str
    address: str
    package_id: int
    message: Optional[str]
    inquiry_number: str = Field(default_factory=lambda: f"INQ-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"  # pending, contacted, completed

# Response Models
class CoverageInquiryResponse(BaseModel):
    id: str
    message: str
    timestamp: datetime

class PackageInquiryResponse(BaseModel):
    id: str
    message: str
    inquiry_number: str
    timestamp: datetime

# Package Model (for reference)
class Package(BaseModel):
    id: int
    name: str
    category: str
    speed: str
    price: str
    features: list[str]
    popular: bool
    image: str
