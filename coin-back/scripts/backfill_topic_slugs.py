# scripts/backfill_topic_slugs.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlmodel import Session, select
from database import engine
from models import Topic
from utils.slug import generate_unique_slug

def backfill_slugs():
    with Session(engine) as session:
        topics = session.exec(select(Topic)).all()
        for topic in topics:
            if not topic.slug:
                topic.slug = generate_unique_slug(topic.name, session)
        session.commit()
        print("✅ 모든 토픽에 slug가 채워졌습니다.")

if __name__ == "__main__":
    backfill_slugs()
