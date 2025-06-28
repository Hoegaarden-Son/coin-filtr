
from typing import List
from fastapi import APIRouter
from models import Topic

router = APIRouter()

# 더미 데이터
topics = [
    Topic(id=1, name="비트코인", description="대표적인 암호화폐"),
    Topic(id=2, name="이더리움", description="스마트 계약 플랫폼"),
]

@router.get("/", response_model=List[Topic])
def get_topics():
    return topics
