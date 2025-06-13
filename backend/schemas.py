from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
import json
from typing import Optional, Dict, List
from uuid import UUID
from fastapi_users import schemas
from pydantic import computed_field


# Post
class PostResponse(BaseModel):
    id: int
    title: str
    text: str
    date: datetime = datetime.now(timezone.utc)

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str
    text: str

    class Config:
        from_attributes = True


# Location
class LocationResponse(BaseModel):
    location: str
    weather: str
    battery: int
    date: datetime = datetime.now(timezone.utc)

    class Config:
        from_attributes = True


class LocationCreate(BaseModel):
    location: str
    weather: str
    battery: int

    class Config:
        from_attributes = True


# Health
class HealthResponse(BaseModel):
    height: Optional[float] = None
    weight: Optional[float] = None
    heart_rate: Optional[float] = None
    energy: Optional[float] = None
    steps: Optional[int] = None
    water: Optional[int] = None
    sleep: Optional[float] = None
    date: datetime = datetime.now(timezone.utc)

    class Config:
        from_attributes = True


class HealthCreate(BaseModel):
    # For Health v2 shortcut:
    # height: Optional[float] = None
    # weight: Optional[float] = None
    # heart_rate: Optional[float] = None
    # energy: Optional[float] = None
    # steps: Optional[int] = None
    # water: Optional[int] = None
    # sleep: Optional[float] = None

    # For Health v1 shortcut + Auto Export Health app:
    data: Dict

    @field_validator("data", mode="before")
    def parse_data(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON string {v}")
        return v

    class Config:
        from_attributes = True


# Activity
class ActivityResponse(BaseModel):
    id: int
    name: str
    date: datetime = datetime.now(timezone.utc)

    class Config:
        from_attributes = True


class ActivityCountResponse(BaseModel):
    date: datetime = datetime.now(timezone.utc)
    activities: Dict[str, int]

    class Config:
        from_attributes = True


class ActivityCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True


class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[datetime] = None

    class Config:
        from_attributes = True


# Project
class ProjectResponse(BaseModel):
    id: int
    name: str
    date: datetime = datetime.now(timezone.utc)

    class Config:
        from_attributes = True


class ProjectScoreResponse(BaseModel):
    name: str
    score: int
    interaction_count: int

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True


# Table
class ColumnInfo(BaseModel):
    name: str
    type: str


class TableInfo(BaseModel):
    name: str
    columns: List[ColumnInfo]


# User
class UserRead(schemas.BaseUser[UUID]):
    username: str


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None


# Contact
class ContactResponse(BaseModel):
    id: int
    name: str
    date: datetime = datetime.now(timezone.utc)

    class Config:
        from_attributes = True


class ContactScoreResponse(BaseModel):
    name: str
    score: int
    interaction_count: int

    class Config:
        from_attributes = True


class ContactCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[datetime] = None

    class Config:
        from_attributes = True


# Users Table
class TableCreate(BaseModel):
    table_name: str


class TableRename(BaseModel):
    new_name: str


# Sessions
class MetricBase(BaseModel):
    type: str
    operator: str
    targetValue: int
    filterValue: Optional[str] = None


class SessionBase(BaseModel):
    title: str
    end_time: datetime
    data_collection_methods: List[str]
    visualization_preferences: List[str]
    goal_type: Optional[str] = "observe"
    metric: Optional[MetricBase] = None


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    title: Optional[str] = None
    end_time: Optional[datetime] = None
    data_collection_methods: Optional[List[str]] = None
    visualization_preferences: Optional[List[str]] = None
    goal_type: Optional[str] = None
    metric: Optional[MetricBase] = None


class Session(SessionBase):
    id: int
    user_id: UUID
    is_active: bool
    is_paused: bool
    pause_start_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def time_remaining(self) -> float:
        now = datetime.now(timezone.utc)
        if self.is_paused and self.pause_start_time:
            # Calculate frozen remaining time
            return (self.end_time - self.pause_start_time).total_seconds()
        return (self.end_time - now).total_seconds()

    class Config:
        from_attributes = True


class SessionPause(BaseModel):
    is_paused: bool
