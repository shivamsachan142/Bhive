from fastapi import APIRouter, Depends, HTTPException
import requests
from sqlalchemy.orm import Session
from dao.database import SessionLocal
from dao.models import FundCache, User
from datetime import datetime

from middleware.middleware import get_current_user

router = APIRouter()

RAPIDAPI_KEY = "1dcd792442mshbd22d68b06a4986p10406fjsn355584da3eaa"
RAPIDAPI_HOST = "latest-mutual-fund-nav.p.rapidapi.com"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def fetch_funds(Mutual_Fund_Family : str = "Default_Fund_Family", db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    url = f"https://{RAPIDAPI_HOST}/latest"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    querystring = {
        "Scheme_Type":"Open",
        "Mutual_Fund_Family":Mutual_Fund_Family
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch funds")
    
    funds_data = response.json()

    for fund in funds_data:
        scheme_code = fund.get("Scheme_Code")
        if not scheme_code:
            continue

        existing_fund = db.query(FundCache).filter(FundCache.scheme_code == scheme_code).first()

        if existing_fund:
            existing_fund.scheme_name = fund.get("Scheme_Name")
            existing_fund.net_asset_value = fund.get("Net_Asset_Value")
            existing_fund.date = fund.get("Date")
            existing_fund.scheme_type = fund.get("Scheme_Type")
            existing_fund.scheme_category = fund.get("Scheme_Category")
            existing_fund.mutual_fund_family = fund.get("Mutual_Fund_Family")
            db.commit()
        else:
            new_fund = FundCache(
                scheme_code=scheme_code,
                scheme_name=fund.get("Scheme_Name"),
                net_asset_value=fund.get("Net_Asset_Value"),
                date=fund.get("Date"),
                scheme_type=fund.get("Scheme_Type"),
                scheme_category=fund.get("Scheme_Category"),
                mutual_fund_family=fund.get("Mutual_Fund_Family"),
            )
            db.add(new_fund)
            db.commit()

    return {
        "message": f"Funds fetch completed.",
        "data" : funds_data
    }
    
    # we can cache for faster response and less number of calls to rapid API
