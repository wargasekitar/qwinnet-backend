from fastapi import FastAPI, APIRouter, HTTPException, Request
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

from models import (
    CoverageInquiryCreate, CoverageInquiry, CoverageInquiryResponse,
    PackageInquiryCreate, PackageInquiry, PackageInquiryResponse,
    Package
)

from admin_routes import admin_router
from settings_routes import settings_router
import auth  # ⬅️ PENTING


# =========================
# ENV & ROOT
# =========================
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")


# =========================
# DATABASE
# =========================
mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

# ⬇️ INJECT DB KE auth.py (INI KUNCI LOGIN ADMIN)
auth.db = db


# =========================
# APP
# =========================
app = FastAPI(
    title="QWINNET ISP API",
    version="1.0.0"
)

api_router = APIRouter(prefix="/api")


# =========================
# ROOT API
# =========================
@api_router.get("/")
async def api_root():
    return {
        "message": "QWINNET ISP API is running",
        "status": "ok"
    }


# =========================
# COVERAGE CHECK
# =========================
@api_router.post("/coverage-check", response_model=CoverageInquiryResponse)
async def create_coverage_check(inquiry: CoverageInquiryCreate):
    try:
        inquiry_obj = CoverageInquiry(**inquiry.model_dump())
        await db.coverage_inquiries.insert_one(inquiry_obj.model_dump())

        return CoverageInquiryResponse(
            id=inquiry_obj.id,
            message="Terima kasih! Tim kami akan menghubungi Anda dalam 1x24 jam",
            timestamp=inquiry_obj.timestamp
        )
    except Exception as e:
        logging.error(f"Error creating coverage inquiry: {e}")
        raise HTTPException(
            status_code=500,
            detail="Terjadi kesalahan. Silakan coba lagi."
        )


# =========================
# PACKAGE INQUIRY
# =========================
@api_router.post("/package-inquiry", response_model=PackageInquiryResponse)
async def create_package_inquiry(inquiry: PackageInquiryCreate):
    try:
        inquiry_obj = PackageInquiry(**inquiry.model_dump())
        await db.package_inquiries.insert_one(inquiry_obj.model_dump())

        return PackageInquiryResponse(
            id=inquiry_obj.id,
            message="Pendaftaran berhasil! Tim kami akan menghubungi Anda segera",
            inquiry_number=inquiry_obj.inquiry_number,
            timestamp=inquiry_obj.timestamp
        )
    except Exception as e:
        logging.error(f"Error creating package inquiry: {e}")
        raise HTTPException(
            status_code=500,
            detail="Terjadi kesalahan. Silakan coba lagi."
        )


# =========================
# PACKAGES
# =========================
@api_router.get("/packages")
async def get_packages():
    try:
        settings = await db.site_settings.find_one(
            {"type": "packages"},
            {"_id": 0}
        )

        if settings and "packages" in settings:
            return {"packages": settings["packages"]}

        return {
            "packages": [
                {
                    "id": 1,
                    "name": "Internet Rumah",
                    "category": "home",
                    "speed": "50 Mbps",
                    "price": "249.000",
                    "features": [
                        "Unlimited Kuota",
                        "Free Instalasi",
                        "Support 24/7",
                        "Cocok untuk 4-6 Perangkat"
                    ],
                    "popular": False,
                    "image": "https://images.unsplash.com/photo-1750711158632-5273ec9b9b86"
                },
                {
                    "id": 2,
                    "name": "Internet Bisnis",
                    "category": "business",
                    "speed": "100 Mbps",
                    "price": "499.000",
                    "features": [
                        "Unlimited Kuota",
                        "Prioritas Support",
                        "IP Publik (Opsional)",
                        "Cocok untuk 10-15 Perangkat"
                    ],
                    "popular": True,
                    "image": "https://images.unsplash.com/photo-1768796371784-3ad0bf2723a0"
                },
                {
                    "id": 3,
                    "name": "Dedicated Corporate",
                    "category": "corporate",
                    "speed": "200 Mbps",
                    "price": "1.299.000",
                    "features": [
                        "Bandwidth Dedicated",
                        "SLA 99.9%",
                        "Priority Support 24/7",
                        "IP Publik & VPN"
                    ],
                    "popular": False,
                    "image": "https://images.unsplash.com/photo-1597733336794-12d05021d510"
                }
            ]
        }
    except Exception as e:
        logging.error(f"Error fetching packages: {e}")
        return {"packages": []}


# =========================
# ADMIN DATA
# =========================
@api_router.get("/coverage-inquiries")
async def get_coverage_inquiries():
    inquiries = await db.coverage_inquiries.find().sort(
        "timestamp", -1
    ).to_list(100)

    for i in inquiries:
        i["_id"] = str(i["_id"])

    return {"count": len(inquiries), "inquiries": inquiries}


@api_router.get("/package-inquiries")
async def get_package_inquiries():
    inquiries = await db.package_inquiries.find().sort(
        "timestamp", -1
    ).to_list(100)

    for i in inquiries:
        i["_id"] = str(i["_id"])

    return {"count": len(inquiries), "inquiries": inquiries}


# =========================
# MIDDLEWARE
# =========================
@app.middleware("http")
async def add_db_to_request(request: Request, call_next):
    request.state.db = db
    return await call_next(request)


# =========================
# ROUTERS
# =========================
app.include_router(api_router)
app.include_router(admin_router)
app.include_router(settings_router)


# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "QWINNET Backend",
        "docs": "/docs"
    }


@app.on_event("shutdown")
async def shutdown_db():
    client.close()
