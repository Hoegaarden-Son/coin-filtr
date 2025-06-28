from fastapi import APIRouter, HTTPException
from models import FavoriteTag

router = APIRouter()

# 간단한 유저별 즐겨찾기 저장소 (메모리)
favorites = []

@router.get("/{user_id}", response_model=list[FavoriteTag])
def get_favorites(user_id: int):
    return [f for f in favorites if f.user_id == user_id]

@router.post("/", response_model=FavoriteTag)
def add_favorite(fav: FavoriteTag):
    user_favs = [f for f in favorites if f.user_id == fav.user_id]
    if len(user_favs) >= 3:
        raise HTTPException(status_code=400, detail="즐겨찾기는 최대 3개까지 가능")
    if any(f.tag_id == fav.tag_id for f in user_favs):
        raise HTTPException(status_code=400, detail="이미 즐겨찾기한 태그입니다")
    favorites.append(fav)
    return fav


@router.delete("/", status_code=204)
def remove_favorite(fav: FavoriteTag):
    try:
        favorites.remove(fav)
    except ValueError:
        raise HTTPException(status_code=404, detail="해당 즐겨찾기 항목 없음")