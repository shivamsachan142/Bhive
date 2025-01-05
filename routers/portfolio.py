from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dao.database import SessionLocal
from dao.models import Portfolio
from dao.models import User, FundCache
from middleware.middleware import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_id_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user.id
    else:
        return None

@router.post("/")
def add_to_portfolio(email: str, scheme_code: str, amount: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = get_user_id_by_email(email, db)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    #calculation of units and cur value
    #addition If same fund is added

    fund = db.query(FundCache).filter(FundCache.scheme_code == scheme_code).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found in cache")
    
    net_asset_value = fund.net_asset_value

    # units purchased and current value
    units_purchased = amount / net_asset_value
    current_value = units_purchased * net_asset_value

    # Check if the fund is already in the user's portfolio
    existing_portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.user_id == user_id, Portfolio.scheme_code == scheme_code)
        .first()
    )

    if existing_portfolio:
        # existing portfolio entry
        existing_portfolio.amount_invested += amount
        existing_portfolio.initial_fund_value += amount
        existing_portfolio.current_value += current_value
        existing_portfolio.current_fund_value = net_asset_value
        db.commit()
        db.refresh(existing_portfolio)
        return existing_portfolio
    else:
        # new portfolio entry
        new_portfolio = Portfolio(
            user_id=user_id,
            scheme_code=scheme_code,
            amount_invested=amount,
            initial_fund_value=amount,
            current_value=current_value,
            current_fund_value=net_asset_value,
        )
        db.add(new_portfolio)
        db.commit()
        db.refresh(new_portfolio)
        return new_portfolio


@router.get("/")
def view_portfolio(email: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = get_user_id_by_email(email, db)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
    return portfolio
