from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:3000"] 처럼 프론트 주소.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router, prefix="/auth")
