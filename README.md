# CoinFiltr

🎯 코인 유튜브 영상의 키워드와 태그를 자동으로 추출하고,
인기 태그 및 개인화 추천 기능을 제공하는 스마트 도구입니다.

## 핵심 기능
- 주제별 태그 추천 및 직접 입력
- 태그 하트 기능 → 실시간 인기 태그 TOP 10
- 태그 즐겨찾기 (최대 3개)
- 관련 유튜버 추천

## 구조
- `/coin-back`: FastAPI API 서버
- `/coin-front`: Next.js 프론트엔드

## 실행
```bash
cd coin-back
uvicorn main:app --reload

cd coin-front
npm run dev
