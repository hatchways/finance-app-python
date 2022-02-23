from api import schemas
from api.dependencies.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/api", tags=["user"])


@router.get("/user", response_model=schemas.User)
def get_authenticated_user(
    current_user: schemas.User = Depends(get_current_user),
):
    """Get the currently logged in user if the token is valid"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please log in"
        )
    return current_user
