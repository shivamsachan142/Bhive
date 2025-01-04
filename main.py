from fastapi import FastAPI
from auth import router as auth_router
from funds import router as funds_router
from portfolio import router as portfolio_router
# import update_nav

from models import Base
from database import engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Tables created in PostgreSQL!"}

app.include_router(auth_router, prefix="/account")
app.include_router(funds_router, prefix="/funds")
app.include_router(portfolio_router, prefix="/portfolio")
