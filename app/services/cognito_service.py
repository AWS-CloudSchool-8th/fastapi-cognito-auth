import boto3
import hmac
import hashlib
import base64
from botocore.exceptions import ClientError
from app.core.config import AWS_REGION, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET

client = boto3.client("cognito-idp", region_name=AWS_REGION)

def get_secret_hash(email: str) -> str:
    message = email + COGNITO_CLIENT_ID
    dig = hmac.new(
        COGNITO_CLIENT_SECRET.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

def sign_up_user(email: str, password: str):
    try:
        secret_hash = get_secret_hash(email)
        client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            SecretHash=secret_hash,
            Username=email,  # ✅ email을 username으로 사용
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email}
            ]
        )
        return {"message": "회원가입 성공. 이메일 인증 코드를 확인하세요."}
    except ClientError as e:
        raise e
    
def confirm_user_signup(email: str, code: str):
    try:
        secret_hash = get_secret_hash(email)
        client.confirm_sign_up(
            ClientId=COGNITO_CLIENT_ID,
            SecretHash=secret_hash,
            Username=email,
            ConfirmationCode=code,
        )
        return {"message": "이메일 인증이 완료되었습니다."}
    except ClientError as e:
        raise e
    
def sign_in_user(email: str, password: str):
    secret_hash = get_secret_hash(email)
    try:
        response = client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password,
                "SECRET_HASH": secret_hash
            }
        )
        return {
            "access_token": response["AuthenticationResult"]["AccessToken"],
            "id_token": response["AuthenticationResult"]["IdToken"],
            "refresh_token": response["AuthenticationResult"]["RefreshToken"]
        }
    except ClientError as e:
        raise e