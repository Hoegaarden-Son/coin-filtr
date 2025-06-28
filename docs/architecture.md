# CoinFiltr 시스템 구조

## 프론트엔드 (Next.js)
- src/app/page.tsx: 메인 페이지
- API 호출: `/tags`, `/topics`, `/favorites` 등

## 백엔드 (FastAPI)
- `main.py`: 앱 진입점
- `models.py`: 데이터 구조
- `routers/tags.py`: 태그 API 처리
- `services/recommendation.py`: 추천 로직 (예정)

## 공통 흐름
1. 사용자가 주제 선택
2. 관련 태그/유튜버 추천
3. 하트 누르면 인기 태그 반영
4. 즐겨찾기는 최대 3개 저장
