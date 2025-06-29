from slugify import slugify
from sqlmodel import Session, select
from models import Topic

def generate_unique_slug(base: str, session: Session) -> str:
    slug_base = slugify(base)
    slug = slug_base
    counter = 1

    while session.exec(select(Topic).where(Topic.slug == slug)).first():
        slug = f"{slug_base}-{counter}"
        counter += 1

    return slug
