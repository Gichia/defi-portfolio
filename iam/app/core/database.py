from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.api.users.models import User
from app.api.users.schemas import UserCreate


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    """Initialize the database with the first superuser."""

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )

        user = crud.create_user(session=session, user_create=user_in)
