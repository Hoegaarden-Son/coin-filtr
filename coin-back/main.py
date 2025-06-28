# coin-back/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_db_and_tables

from routers import topics, tags, favorites, youtubers, videos

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


# app = FastAPI()
app = FastAPI(lifespan=lifespan)


# ✅ CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 모두 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(topics.router, prefix="/topics", tags=["Topics"])
app.include_router(tags.router, prefix="/tags", tags=["Tags"])
app.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
app.include_router(youtubers.router, prefix="/youtubers", tags=["Youtubers"])
app.include_router(videos.router, prefix="/videos", tags=["Videos"])

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI backend!"}
