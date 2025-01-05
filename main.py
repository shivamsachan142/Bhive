from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.funds import router as funds_router
from routers.portfolio import router as portfolio_router
from scheduler import scheduler

from dao.models import Base
from dao.database import engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start the scheduler when the app starts and shut it down gracefully on shutdown"""
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Tables created in PostgreSQL!"}

app.include_router(auth_router, prefix="/account")
app.include_router(funds_router, prefix="/funds")
app.include_router(portfolio_router, prefix="/portfolio")


# {
#     "Scheme_Code": 120437,
#     "ISIN_Div_Payout_ISIN_Growth": "-",
#     "ISIN_Div_Reinvestment": "INF846K01CU0",
#     "Scheme_Name": "Axis Banking & PSU Debt Fund - Direct Plan - Daily IDCW",
#     "Net_Asset_Value": 1039.131,
#     "Date": "03-Jan-2025",
#     "Scheme_Type": "Open Ended Schemes",
#     "Scheme_Category": "Debt Scheme - Banking and PSU Fund",
#     "Mutual_Fund_Family": "Axis Mutual Fund"
# }
