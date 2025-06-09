from fastapi import APIRouter, HTTPException
from app.models.auth_models import SignUpRequest
from app.services.cognito_service import sign_up_user
from botocore.exceptions import ClientError
from app.models.auth_models import ConfirmSignUpRequest
from app.services.cognito_service import confirm_user_signup
from app.models.auth_models import SignInRequest
from app.services.cognito_service import sign_in_user



router = APIRouter()

@router.post("/signup")
def signup(req: SignUpRequest):
    try:
        result = sign_up_user(req.email, req.password)  # ✅ 인자 순서 정확히 확인
        return {"email": req.email, **result}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response["Error"]["Message"])
    
@router.post("/confirm")
def confirm_signup(req: ConfirmSignUpRequest):
    try:
        return confirm_user_signup(req.email, req.code)
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response["Error"]["Message"])
    
@router.post("/login")
def login(req: SignInRequest):
    try:
        return sign_in_user(req.email, req.password)
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response["Error"]["Message"])