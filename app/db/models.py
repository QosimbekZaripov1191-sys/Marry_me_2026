import enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Enum,
    ForeignKey,
    BigInteger,
    Text,
    JSON,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utcnow():
    return datetime.utcnow()


class Base(DeclarativeBase):
    pass


# ---------- ENUMS ----------

class ProfileStatus(str, enum.Enum):
    draft = "draft"
    pending = "pending"
    active = "active"
    blocked = "blocked"


class Gender(str, enum.Enum):
    male = "male"
    female = "female"


# ---------- MODELS ----------

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    tg_user_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=False,
    )
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        nullable=False,
    )


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    owner_user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )

    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    display_name: Mapped[str] = mapped_column(String(128), nullable=False)
    bio: Mapped[str] = mapped_column(Text, default="")
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    city: Mapped[str] = mapped_column(String(128), default="")
    region: Mapped[str] = mapped_column(String(64), default="", nullable=False)


    tg_username_public: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    photos: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    status: Mapped[ProfileStatus] = mapped_column(
        Enum(ProfileStatus),
        default=ProfileStatus.draft,
        nullable=False,
    )

    active_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    vip_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        onupdate=utcnow,
    )
