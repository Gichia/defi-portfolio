

from sqlmodel import Session

from app.core.security import get_password_hash
from app.api.users import models as user_model, schemas as user_schema


def create_user(
        *, session: Session,
        user_create: user_schema.UserCreate
    ) -> user_model.User:
    """Create a new user in the database."""

    user_obj = user_model.UserUser.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )

    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)

    return user_obj