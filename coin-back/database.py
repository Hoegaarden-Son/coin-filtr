# database.py
from sqlmodel import SQLModel, create_engine, Session

# SQLite 파일 경로 (루트 디렉토리의 coinfiltr.db로 저장됨)
DATABASE_URL = "sqlite:///./coinfiltr.db"

# SQLAlchemy Engine 생성
engine = create_engine(DATABASE_URL, echo=True)  # echo=True: SQL 쿼리 로그 보여줌


# 테이블 생성용 함수 (앱 시작 시 1회 실행)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# DB 세션 꺼내는 함수 (의존성 주입에 사용 가능)
def get_session():
    return Session(engine)
