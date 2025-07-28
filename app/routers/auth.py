from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..models import user_model
from ..schemas import user_schema
from ..core.security import get_password_hash, verify_password




router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/register")
async def register(
    request: user_schema.Register,
    response: Response,
    db: Session = Depends(get_db),
):
    if request.password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
   
    
    existing_user = db.query(user_model.User).filter_by(email=request.email).first()
    if existing_user:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "error",
            "message": "Email already registered."
        }
    
    new_user = user_model.User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password=get_password_hash(request.password),
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    response.status_code = status.HTTP_201_CREATED
    return {
        "status": "success",
        "message": "User registered successfully!",
        "user": {
            "id": str(new_user.id),
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "emailVerified": new_user.emailVerified
        }
    }


@router.post("/login", response_model=user_schema.ShowUser)
async def login(request: user_schema.Login, response:Response, db: Session = Depends(get_db)):
    existing_user = db.query(user_model.User).filter_by(email=request.email).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    is_verified = verify_password(request.password, existing_user.password)
    if not is_verified:
        return{
            "status":"error",
            "message":"Invalid credentials"
        }
    
    user_data = user_schema.Show.model_validate(existing_user,from_attributes=True )
    return user_schema.ShowUser(
    status="success",
    message="Login successful",
    data=user_data
)