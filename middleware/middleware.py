from fastapi import Depends, Security, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dao.models import User
from sqlalchemy.orm import Session
from dao.database import get_db
from routers.auth import ALGORITHM, SECRET_KEY


# OAuth2PasswordBearer will automatically look for the "Authorization" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to decode and verify the JWT token
def verify_token(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get the user from the database
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user

# Dependency to get the current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return verify_token(token, db)
