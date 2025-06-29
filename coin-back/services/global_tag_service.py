from sqlmodel import Session, select
from models import GlobalTag, TopicGlobalTag
from models.topic import Topic

def assign_all_global_tags_to_topic(topic_id: int, session: Session):
    global_tags = session.exec(select(GlobalTag)).all()

    for tag in global_tags:
        exists = session.exec(
            select(TopicGlobalTag).where(
                (TopicGlobalTag.topic_id == topic_id) &
                (TopicGlobalTag.global_tag_id == tag.id)
            )
        ).first()
        if not exists:
            link = TopicGlobalTag(
                topic_id=topic_id,
                global_tag_id=tag.id,
                like_count=0
            )
            session.add(link)

    session.commit()


def assign_global_tag_to_all_topics(global_tag_id: int, session: Session):
    topics = session.exec(select(Topic)).all()

    for topic in topics:
        # 중복 연결 방지
        existing = session.get(TopicGlobalTag, (topic.id, global_tag_id))
        if not existing:
            link = TopicGlobalTag(topic_id=topic.id, global_tag_id=global_tag_id)
            session.add(link)

    session.commit()