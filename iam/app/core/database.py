from sqlmodel import Session, create_engine, select, SQLModel

from app.core.config import settings


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    """Initialize the database with the first superuser."""

    # Import here to avoid circular imports
    from app.api.users import (
        models as user_model,
        schemas as user_schema,
        repository as user_repository,
    )

    user = session.exec(
        select(user_model.User).where(
            user_model.User.email == settings.FIRST_SUPERUSER_EMAIL)
    ).first()
    if not user:
        user_in = user_schema.UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )

        user = user_repository.create_user(
            session=session, user_create=user_in)
