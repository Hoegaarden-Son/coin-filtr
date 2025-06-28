from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from models.favorite import FavoriteTag, FavoriteTagCreate, FavoriteTagUpdate
from database import get_session


router = APIRouter()

# 간단한 유저별 즐겨찾기 저장소 (메모리)
favorites = []

# GET /favorites/user/{user_id}
@router.get("/user/{user_id}", response_model=List[FavoriteTag])
def get_favorites_for_user(user_id: int, session: Session = Depends(get_session)):
    return session.exec(select(FavoriteTag).where(FavoriteTag.user_id == user_id)).all()

# POST /favorites/
@router.post("/", response_model=FavoriteTag)
def create_favorite(data: FavoriteTagCreate, session: Session = Depends(get_session)):
    # 중복 방지 (같은 user_id + tag_id 조합 존재 시)
    existing = session.exec(
        select(FavoriteTag).where(
            (FavoriteTag.user_id == data.user_id) & (FavoriteTag.tag_id == data.tag_id)
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already favorited")

    fav = FavoriteTag.model_validate(data)
    session.add(fav)
    session.commit()
    session.refresh(fav)
    return fav

# DELETE /favorites/{favorite_id}
@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: int, session: Session = Depends(get_session)):
    fav = session.get(FavoriteTag, favorite_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    session.delete(fav)
    session.commit()
    return {"message": "Favorite deleted"}