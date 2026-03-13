from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class DeclarativeModel(MappedAsDataclass, DeclarativeBase, kw_only=True):
    pass
