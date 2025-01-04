from fastapi import APIRouter, Depends, HTTPException
import requests
from sqlalchemy.orm import Session
from database import SessionLocal
# from models import FundCache
from datetime import datetime

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
def fetch_funds(Mutual_Fund_Family : str = "Default_Fund_Family", db: Session = Depends(get_db)):
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
    
    data = response.json()
    
