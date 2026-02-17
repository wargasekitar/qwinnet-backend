from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging
from auth import verify_token
from settings_models import (
    SiteSettings, PackageSettings, TestimonialSettings, 
    CoverageSettings, WhyChooseSettings
)

settings_router = APIRouter(prefix="/api/admin/settings", tags=["Settings"])

# Get General Settings
@settings_router.get("/general")
async def get_general_settings(current_user: dict = Depends(verify_token)):
    """Get general site settings."""
    from server import db
    
    try:
        settings = await db.site_settings.find_one({"type": "general"}, {"_id": 0})
        
        if not settings:
            # Return default settings if not found
            return {
                "company_name": "QWINNET",
                "hero": {
                    "title": "Internet Cepat, Stabil, Tanpa Ribet",
                    "subtitle": "Solusi internet handal untuk rumah dan bisnis Anda dengan kecepatan maksimal dan harga terjangkau",
                    "badge_text": "Provider Internet Terpercaya",
                    "cta_primary": "Cek Jangkauan",
                    "cta_secondary": "Hubungi Kami",
                    "stats": [
                        {"value": "10K+", "label": "Pelanggan Puas"},
                        {"value": "99.9%", "label": "Uptime Guarantee"},
                        {"value": "24/7", "label": "Customer Support"}
                    ]
                },
                "contact": {
                    "whatsapp": "6281234567890",
                    "phone": "+62 812-3456-7890",
                    "email": "info@qwinnet.id",
                    "address": "Jl. Sudirman No. 123, Jakarta Selatan, 12190"
                },
                "social_media": {
                    "facebook": "https://facebook.com",
                    "instagram": "https://instagram.com",
                    "twitter": "https://twitter.com"
                },
                "footer_text": "Provider internet terpercaya yang menghadirkan koneksi cepat, stabil, dan terjangkau untuk rumah dan bisnis Anda.",
                "cta": {
                    "title": "Siap Upgrade Internet Anda Hari Ini?",
                    "subtitle": "Bergabunglah dengan ribuan pelanggan yang sudah merasakan internet cepat dan stabil bersama QWINNET",
                    "features": ["Free Instalasi", "Tanpa Biaya Tersembunyi", "Support 24/7"]
                },
                "sections": {
                    "packages_title": "Paket Internet Kami",
                    "packages_subtitle": "Pilih paket yang sesuai dengan kebutuhan Anda, dari rumahan hingga korporat",
                    "testimonials_title": "Apa Kata Pelanggan Kami?",
                    "testimonials_subtitle": "Ribuan pelanggan telah mempercayai QWINNET untuk kebutuhan internet mereka",
                    "coverage_title": "Area Jangkauan Kami",
                    "coverage_subtitle": "Kami terus memperluas jaringan QWINNET untuk menjangkau lebih banyak area",
                    "why_choose_title": "Kenapa Pilih QWINNET?",
                    "why_choose_subtitle": "Kami berkomitmen memberikan layanan internet terbaik dengan berbagai keunggulan"
                },
                "trust_badges": [
                    {"value": "4.9/5", "label": "Rating Pelanggan"},
                    {"value": "10K+", "label": "Pelanggan Aktif"},
                    {"value": "5 Tahun", "label": "Pengalaman"},
                    {"value": "99.9%", "label": "Kepuasan"}
                ]
            }
        
        return settings
    except Exception as e:
        logging.error(f"Error fetching general settings: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching settings")

# Update General Settings
@settings_router.put("/general")
async def update_general_settings(
    settings: SiteSettings,
    current_user: dict = Depends(verify_token)
):
    """Update general site settings."""
    from server import db
    
    try:
        settings_dict = settings.dict()
        settings_dict["type"] = "general"
        
        result = await db.site_settings.update_one(
            {"type": "general"},
            {"$set": settings_dict},
            upsert=True
        )
        
        return {"message": "Settings updated successfully", "settings": settings_dict}
    except Exception as e:
        logging.error(f"Error updating general settings: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating settings")

# Get Packages
@settings_router.get("/packages")
async def get_packages_settings(current_user: dict = Depends(verify_token)):
    """Get packages settings."""
    from server import db
    
    try:
        settings = await db.site_settings.find_one({"type": "packages"}, {"_id": 0})
        
        if not settings:
            # Return default packages
            return {
                "packages": [
                    {
                        "id": 1,
                        "name": "Internet Rumah",
                        "category": "home",
                        "speed": "50 Mbps",
                        "price": "249.000",
                        "features": ["Unlimited Kuota", "Free Instalasi", "Support 24/7", "Cocok untuk 4-6 Perangkat"],
                        "popular": False,
                        "image": "https://images.unsplash.com/photo-1750711158632-5273ec9b9b86?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxODl8MHwxfHNlYXJjaHwyfHxtb2Rlcm4lMjBob21lJTIwb2ZmaWNlJTIwY29ubmVjdGl2aXR5fGVufDB8fHx8MTc3MDI1NDg3MHww&ixlib=rb-4.1.0&q=85"
                    },
                    {
                        "id": 2,
                        "name": "Internet Bisnis",
                        "category": "business",
                        "speed": "100 Mbps",
                        "price": "499.000",
                        "features": ["Unlimited Kuota", "Prioritas Support", "IP Publik (Opsional)", "Cocok untuk 10-15 Perangkat"],
                        "popular": True,
                        "image": "https://images.unsplash.com/photo-1768796371784-3ad0bf2723a0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA3MDR8MHwxfHNlYXJjaHw0fHxvZmZpY2UlMjB0ZWFtd29yayUyMHRlY2hub2xvZ3l8ZW58MHx8fHwxNzcwMjU0ODg0fDA&ixlib=rb-4.1.0&q=85"
                    },
                    {
                        "id": 3,
                        "name": "Dedicated Corporate",
                        "category": "corporate",
                        "speed": "200 Mbps",
                        "price": "1.299.000",
                        "features": ["Bandwidth Dedicated", "SLA 99.9%", "Priority Support 24/7", "IP Publik & VPN"],
                        "popular": False,
                        "image": "https://images.unsplash.com/photo-1597733336794-12d05021d510?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxODF8MHwxfHNlYXJjaHwyfHxmaWJlciUyMGludGVybmV0fGVufDB8fHx8MTc3MDI1NDg3OXww&ixlib=rb-4.1.0&q=85"
                    }
                ]
            }
        
        return settings
    except Exception as e:
        logging.error(f"Error fetching packages settings: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching packages")

# Update Packages
@settings_router.put("/packages")
async def update_packages_settings(
    packages: List[PackageSettings],
    current_user: dict = Depends(verify_token)
):
    """Update packages settings."""
    from server import db
    
    try:
        packages_dict = {
            "type": "packages",
            "packages": [pkg.dict() for pkg in packages]
        }
        
        result = await db.site_settings.update_one(
            {"type": "packages"},
            {"$set": packages_dict},
            upsert=True
        )
        
        return {"message": "Packages updated successfully"}
    except Exception as e:
        logging.error(f"Error updating packages: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating packages")

# Get Testimonials
@settings_router.get("/testimonials")
async def get_testimonials_settings(current_user: dict = Depends(verify_token)):
    """Get testimonials settings."""
    from server import db
    
    try:
        settings = await db.site_settings.find_one({"type": "testimonials"}, {"_id": 0})
        
        if not settings:
            return {
                "testimonials": [
                    {
                        "id": 1,
                        "name": "Budi Santoso",
                        "role": "Pemilik Warung Kopi",
                        "rating": 5,
                        "text": "Pelanggan di warung kopi saya sangat puas dengan WiFi dari QWINNET. Cepat dan stabil, bahkan saat ramai!",
                        "image": "https://ui-avatars.com/api/?name=Budi+Santoso&background=1e3a8a&color=fff&size=128"
                    },
                    {
                        "id": 2,
                        "name": "Siti Nurhaliza",
                        "role": "Ibu Rumah Tangga",
                        "rating": 5,
                        "text": "Anak-anak bisa sekolah online dengan lancar. Harga terjangkau dan customer service ramah banget!",
                        "image": "https://ui-avatars.com/api/?name=Siti+Nurhaliza&background=1e3a8a&color=fff&size=128"
                    },
                    {
                        "id": 3,
                        "name": "Agus Wijaya",
                        "role": "Digital Marketing Agency",
                        "rating": 5,
                        "text": "Sudah 2 tahun pakai QWINNET untuk kantor. Upload download kencang, meeting online lancar jaya!",
                        "image": "https://ui-avatars.com/api/?name=Agus+Wijaya&background=1e3a8a&color=fff&size=128"
                    }
                ]
            }
        
        return settings
    except Exception as e:
        logging.error(f"Error fetching testimonials: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching testimonials")

# Update Testimonials
@settings_router.put("/testimonials")
async def update_testimonials_settings(
    testimonials: List[TestimonialSettings],
    current_user: dict = Depends(verify_token)
):
    """Update testimonials settings."""
    from server import db
    
    try:
        testimonials_dict = {
            "type": "testimonials",
            "testimonials": [t.dict() for t in testimonials]
        }
        
        result = await db.site_settings.update_one(
            {"type": "testimonials"},
            {"$set": testimonials_dict},
            upsert=True
        )
        
        return {"message": "Testimonials updated successfully"}
    except Exception as e:
        logging.error(f"Error updating testimonials: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating testimonials")

# Get Coverage Areas
@settings_router.get("/coverage")
async def get_coverage_settings(current_user: dict = Depends(verify_token)):
    """Get coverage areas settings."""
    from server import db
    
    try:
        settings = await db.site_settings.find_one({"type": "coverage"}, {"_id": 0})
        
        if not settings:
            return {
                "areas": ["Jakarta Selatan", "Jakarta Barat", "Tangerang", "Depok", "Bekasi", "Bandung"]
            }
        
        return settings
    except Exception as e:
        logging.error(f"Error fetching coverage settings: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching coverage")

# Update Coverage Areas
@settings_router.put("/coverage")
async def update_coverage_settings(
    coverage: CoverageSettings,
    current_user: dict = Depends(verify_token)
):
    """Update coverage areas settings."""
    from server import db
    
    try:
        coverage_dict = coverage.dict()
        coverage_dict["type"] = "coverage"
        
        result = await db.site_settings.update_one(
            {"type": "coverage"},
            {"$set": coverage_dict},
            upsert=True
        )
        
        return {"message": "Coverage areas updated successfully"}
    except Exception as e:
        logging.error(f"Error updating coverage: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating coverage")

# Get Why Choose Settings
@settings_router.get("/why-choose")
async def get_why_choose_settings(current_user: dict = Depends(verify_token)):
    """Get why choose settings."""
    from server import db
    
    try:
        settings = await db.site_settings.find_one({"type": "why_choose"}, {"_id": 0})
        
        if not settings:
            return {
                "items": [
                    {
                        "id": 1,
                        "title": "Kecepatan Stabil",
                        "description": "Koneksi internet super cepat dan konsisten untuk semua aktivitas online Anda",
                        "icon": "zap"
                    },
                    {
                        "id": 2,
                        "title": "Jaringan Andal",
                        "description": "Infrastruktur fiber optik dengan teknologi terkini untuk reliability maksimal",
                        "icon": "wifi"
                    },
                    {
                        "id": 3,
                        "title": "Support Responsif",
                        "description": "Tim technical support siap membantu Anda 24/7 dengan respons time cepat",
                        "icon": "headphones"
                    },
                    {
                        "id": 4,
                        "title": "Harga Transparan",
                        "description": "Tanpa biaya tersembunyi, harga yang Anda lihat adalah harga yang Anda bayar",
                        "icon": "shield-check"
                    }
                ]
            }
        
        return settings
    except Exception as e:
        logging.error(f"Error fetching why choose settings: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching why choose")

# Update Why Choose Settings
@settings_router.put("/why-choose")
async def update_why_choose_settings(
    why_choose: WhyChooseSettings,
    current_user: dict = Depends(verify_token)
):
    """Update why choose settings."""
    from server import db
    
    try:
        why_choose_dict = why_choose.dict()
        why_choose_dict["type"] = "why_choose"
        
        result = await db.site_settings.update_one(
            {"type": "why_choose"},
            {"$set": why_choose_dict},
            upsert=True
        )
        
        return {"message": "Why choose settings updated successfully"}
    except Exception as e:
        logging.error(f"Error updating why choose: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating why choose")
