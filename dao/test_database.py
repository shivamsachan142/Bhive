from sqlalchemy import create_engine

DATABASE_URL = "postgresql://test_user:test123@localhost:5432/mutual_funds"
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")
