from sqlalchemy.orm import DeclarativeBase  # Base class from SQLAlchemy used to define ORM models

class Base(DeclarativeBase):  # Custom base class that all database models will inherit from
    pass                      # No extra configuration needed — just activates SQLAlchemy's ORM mapping system