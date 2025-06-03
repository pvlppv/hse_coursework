from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    BigInteger,
    DateTime,
    TIMESTAMP,
    JSON,
    ForeignKey,
    func,
    DECIMAL,
    Boolean,
    text,
)
from base import Base
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.dialects.postgresql import JSONB, UUID


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    text = Column(String)
    date = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String)
    weather = Column(String)
    battery = Column(Integer)
    date = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Health(Base):
    __tablename__ = "health"

    id = Column(Integer, primary_key=True, autoincrement=True)
    height = Column(DECIMAL(precision=5, scale=1))  # 5 total digits, 1 after decimal
    weight = Column(DECIMAL(precision=5, scale=1))
    heart_rate = Column(DECIMAL(precision=5, scale=1))
    energy = Column(DECIMAL(precision=5, scale=1))
    steps = Column(Integer)
    water = Column(Integer)
    sleep = Column(DECIMAL(precision=5, scale=1))
    date = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    date = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    date = Column(TIMESTAMP(timezone=True), server_default=func.now())


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    username = Column(String, unique=True)
    date = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    date = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    end_time = Column(TIMESTAMP(timezone=True))
    data_collection_methods = Column(JSONB, nullable=False)
    visualization_preferences = Column(JSONB, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_paused = Column(Boolean, default=False)
    pause_start_time = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
