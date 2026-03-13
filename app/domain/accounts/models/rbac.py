from typing import TYPE_CHECKING, List

from sqlalchemy import Column, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.model import BaseModel, DeclarativeModel

if TYPE_CHECKING:
    from app.domain.accounts.models import User


class Permission(BaseModel):
    __tablename__ = 'permissions'
    __table_args__ = UniqueConstraint(
        'resource', 'action', 'idx_permission_resource_action'
    )

    resource: Mapped[str] = mapped_column(String(50), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)

    roles: Mapped[List['Role']] = relationship(
        back_populates='permissions',
        secondary='role_permissions',
        lazy='raise',
        init=False,
    )


class Role(BaseModel):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(200))

    permissions: Mapped[list['Permission']] = relationship(
        back_populates='roles',
        secondary='role_permissions',
        lazy='raise',
        init=False,
    )
    users: Mapped[list['User']] = relationship(
        back_populates='roles',
        secondary='user_roles',
        lazy='raise',
        init=False,
    )


role_permissions = Table(
    'role_permissions',
    DeclarativeModel.metadata,
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', ForeignKey('permissions.id'), primary_key=True),
)

user_roles = Table(
    'user_roles',
    DeclarativeModel.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
)
