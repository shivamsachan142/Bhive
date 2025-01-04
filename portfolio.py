from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Portfolio
from models import User

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
def add_to_portfolio(email: str, fund_name: str, amount: float, db: Session = Depends(get_db)):
    user_id = get_user_id_by_email(email, db)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    #calculation of units and cur value
    #addition If same fund is added
    portfolio_item = Portfolio(user_id=user_id, fund_name=fund_name, amount_invested=amount)
    db.add(portfolio_item)
    db.commit()
    db.refresh(portfolio_item)
    return portfolio_item

@router.get("/")
def view_portfolio(email: str, db: Session = Depends(get_db)):
    user_id = get_user_id_by_email(email, db)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
    return portfolio
