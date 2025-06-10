# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt  # pyyaml 등

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    try:
        # Cognito의 JWKS로 서명 검증 + 클레임 파싱
        payload = jwt.decode(token, "YOUR_COGNITO_JWT_SECRET", algorithms=["RS256"])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    # payload 안에 담긴 정보로 User 모델 생성하거나
    return SimpleNamespace(
        username=payload.get("cognito:username"),
        email=payload.get("email"),
    )
