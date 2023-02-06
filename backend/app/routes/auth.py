"""Module used to authentication purposes."""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

import app.security as security
from app.config import settings
from app.crud import user_crud
from app.schemas.token import Token, TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


async def authenticate_user(email: str, password: str):
    """Checks if there is username in databe based on given email
    and compares password from databe with given password.

    Args:
        email (str): user email.
        password (str): user password.

    Returns:
        user (dict) | False (bool): User schema recived from database or False (bool).
    """
    user = await user_crud.get_user_by_email(email)
    if not user:
        return False
    if not security.verify_password(password, user["password"]):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Decodes access_token to gather current logged in username from database.

    Args:
        token (str, optional): access token (JWT). Defaults to Depends(oauth2_scheme).

    Raises:
        credentials_exception: HTTP 401 code (Unathorized). Could not validate credentials.

    Returns:
        user (dict): User schema retured from database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await user_crud.get_user_by_email(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint used to login and gather access token (JWT token).
    Username is at real an email (but named as username for proper auth convention)

    Args:
        form_data (OAuth2PasswordRequestForm, optional): username (email) and password.

    Raises:
        HTTPException: HTTP 401 code (Unathorized). Incorrct username or passowrd.

    Returns:
        dict: contains access_token and token_type.
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
