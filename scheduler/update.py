from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dao.database import SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from contextlib import asynccontextmanager

from dao.models import FundCache, Portfolio


def update_portfolio_value(db: Session):
    portfolios = db.query(Portfolio).all()

    for portfolio in portfolios:
        fund = db.query(FundCache).filter(FundCache.scheme_code == portfolio.scheme_code).first()
        
        if fund:
            current_value = portfolio.amount_invested * fund.net_asset_value / fund.initial_fund_value
            portfolio.current_value = current_value
            db.commit()
            db.refresh(portfolio)


def update_portfolio_hourly():
    with SessionLocal() as db:
        update_portfolio_value(db)


scheduler = BackgroundScheduler()

scheduler.add_job(
    update_portfolio_hourly,
    trigger=IntervalTrigger(hours=1),
    id="update_portfolio_task",
    replace_existing=True
)

