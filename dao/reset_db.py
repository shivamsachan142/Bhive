from sqlalchemy import create_engine
from dao.models import Base 
from dao.database import engine  

def recreate_tables():
    Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)
    print("Tables have been recreated successfully!")

if __name__ == "__main__":
    recreate_tables()
