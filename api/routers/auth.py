from api.core import auth, security
from api.crud import UserCrud
from api.dependencies.db import get_db
from api.schemas.auth import LoginRequestBody, LoginResponse, RegisterResponse
from api.schemas.users import UserCreate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(form_data: LoginRequestBody, db: Session = Depends(get_db)):
    """User will attempt to authenticate with a email/password flow"""

    user = await auth.login_user(db, form_data.email, form_data.password)
    if not user:
        # Wrong email or password provided
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = security.create_access_token(data={"sub": user.email})

    return LoginResponse(token=token, user=user)


@router.post("/signup", response_model=RegisterResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user record in the database and send a registration confirmation email"""
    db_user = UserCrud.get_user_by_email(db, data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = UserCrud.create_user(db, data)

    token = security.create_access_token(data={"sub": new_user.email})

    return RegisterResponse(token=token, user=new_user)
