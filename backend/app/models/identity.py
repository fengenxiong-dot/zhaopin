import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Table, Column, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

user_roles = Table(
    "user_roles", Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

class OrgUnit(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "org_units"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("org_units.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class Role(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "roles"
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    employee_no: Mapped[str | None] = mapped_column(String(50), unique=True)
    org_unit_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("org_units.id"))
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    roles: Mapped[list[Role]] = relationship(secondary=user_roles, lazy="selectin")

class AuthSession(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "auth_sessions"
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user: Mapped[User] = relationship(lazy="selectin")

class DictionaryType(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "dictionary_types"
    code: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

class DictionaryItem(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "dictionary_items"
    __table_args__ = (UniqueConstraint("dictionary_type_id", "code"),)
    dictionary_type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dictionary_types.id", ondelete="RESTRICT"))
    code: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("dictionary_items.id"))

class AuditLog(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "audit_logs"
    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(80), nullable=False)
    resource_id: Mapped[str | None] = mapped_column(String(100))
    detail: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
