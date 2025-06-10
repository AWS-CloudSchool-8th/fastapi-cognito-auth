from fastapi import APIRouter, HTTPException, Depends
from app.models.auth_models import SignUpRequest
from app.services.cognito_service import sign_up_user
from botocore.exceptions import ClientError
from app.models.auth_models import ConfirmSignUpRequest
from app.services.cognito_service import confirm_user_signup
from app.models.auth_models import SignInRequest
from app.services.cognito_service import sign_in_user
from app.dependencies import get_current_user



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

@router.get("/me")
async def read_current_user(user = Depends(get_current_user)):
    """
    Authorization 헤더에 Bearer <access_token>을 담아서 호출하세요.
    """
    return {
        "username": user.username,
        "email": user.email,
        # 필요하면 다른 프로필 필드도 추가
    }
