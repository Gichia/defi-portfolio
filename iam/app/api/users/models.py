from pydantic import EmailStr

from sqlmodel import Field

from app.core.database import SQLModel


class UserBase(SQLModel):
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
