from pydantic import BaseModel
from typing import List, Optional, Any, Dict

# Site Settings Models
class ContactInfo(BaseModel):
    whatsapp: Optional[str] = ""
    phone: Optional[str] = ""
    email: Optional[str] = ""
    address: Optional[str] = ""

class SocialMedia(BaseModel):
    facebook: Optional[str] = ""
    instagram: Optional[str] = ""
    twitter: Optional[str] = ""

class HeroStat(BaseModel):
    value: Optional[str] = ""
    label: Optional[str] = ""

class HeroContent(BaseModel):
    title: Optional[str] = ""
    subtitle: Optional[str] = ""
    badge_text: Optional[str] = "Provider Internet Terpercaya"
    cta_primary: Optional[str] = "Cek Jangkauan"
    cta_secondary: Optional[str] = "Hubungi Kami"
    stats: Optional[List[HeroStat]] = None

class CTAContent(BaseModel):
    title: Optional[str] = ""
    subtitle: Optional[str] = ""
    features: Optional[List[str]] = []

class SectionTitles(BaseModel):
    packages_title: Optional[str] = ""
    packages_subtitle: Optional[str] = ""
    testimonials_title: Optional[str] = ""
    testimonials_subtitle: Optional[str] = ""
    coverage_title: Optional[str] = ""
    coverage_subtitle: Optional[str] = ""
    why_choose_title: Optional[str] = ""
    why_choose_subtitle: Optional[str] = ""

class TrustBadge(BaseModel):
    value: Optional[str] = ""
    label: Optional[str] = ""

class SiteSettings(BaseModel):
    company_name: Optional[str] = "QWINNET"
    hero: Optional[HeroContent] = None
    contact: Optional[ContactInfo] = None
    social_media: Optional[SocialMedia] = None
    footer_text: Optional[str] = ""
    cta: Optional[CTAContent] = None
    sections: Optional[SectionTitles] = None
    trust_badges: Optional[List[TrustBadge]] = None
    
    class Config:
        extra = "allow"  # Allow extra fields

# Package Model
class PackageFeature(BaseModel):
    text: str

class PackageSettings(BaseModel):
    id: int
    name: str
    category: Optional[str] = "home"
    speed: str
    price: str
    features: List[str]
    popular: Optional[bool] = False
    image: Optional[str] = ""

# Testimonial Model
class TestimonialSettings(BaseModel):
    id: int
    name: str
    role: Optional[str] = ""
    rating: Optional[int] = 5
    text: str
    image: Optional[str] = ""

# Coverage Area Model
class CoverageSettings(BaseModel):
    areas: List[str]

# Why Choose Model
class WhyChooseItem(BaseModel):
    id: int
    title: str
    description: str
    icon: Optional[str] = "zap"

class WhyChooseSettings(BaseModel):
    items: List[WhyChooseItem]
