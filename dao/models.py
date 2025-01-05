from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Portfolio(Base):
    __tablename__ = "portfolio"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheme_code = Column(Integer, ForeignKey("fund_cache.scheme_code"), nullable=False)
    amount_invested = Column(Float)
    current_value = Column(Float)
    initial_fund_value = Column(Float)
    current_fund_value = Column(Float)

class FundCache(Base):
    __tablename__ = "fund_cache"

    # id = Column(Integer, primary_key=True, index=True)
    scheme_code = Column(Integer, primary_key=True) 
    isin_div_payout_isin_growth = Column(String, nullable=True)
    isin_div_reinvestment = Column(String, nullable=True)
    scheme_name = Column(String, nullable=False)
    net_asset_value = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    scheme_type = Column(String, nullable=False)
    scheme_category = Column(String, nullable=False)
    mutual_fund_family = Column(String, nullable=False)
