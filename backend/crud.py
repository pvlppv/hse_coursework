from sqlalchemy import (
    desc,
    func,
    distinct,
    select,
    insert,
    update,
    delete,
    MetaData,
    Table,
    inspect,
    Column,
    TIMESTAMP,
    String,
    Integer,
    or_,
)
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.sql import text, quoted_name
from sqlalchemy.exc import SQLAlchemyError, NoSuchTableError
import models
import schemas
from database import metadata, engine
from datetime import datetime, timedelta, timezone
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, create_model
from fastapi import HTTPException
import sqlalchemy as sa
import re
from sqlalchemy.schema import CreateTable, DropTable
from uuid import UUID


# Post
async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Post).order_by(desc(models.Post.date)).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_post(db: AsyncSession, id: int):
    result = await db.execute(select(models.Post).filter(models.Post.id == id))
    return result.scalars().first()


async def create_post(db: AsyncSession, post: schemas.PostCreate):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def delete_post(db: AsyncSession, id: int):
    db_post = await get_post(db, id)
    if db_post:
        await db.delete(db_post)
        await db.commit()
    return db_post


# Location
async def get_location(db: AsyncSession):
    result = await db.execute(
        select(models.Location).order_by(desc(models.Location.date))
    )
    return result.scalars().first()


async def create_location(db: AsyncSession, location: schemas.LocationCreate):
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    await db.commit()
    await db.refresh(db_location)
    return db_location


# Health
async def get_health(db: AsyncSession):
    result = await db.execute(select(models.Health).order_by(desc(models.Health.date)))
    return result.scalars().first()


async def get_health_all(db: AsyncSession):
    subquery = (
        select(func.max(models.Health.id).label("max_id"))
        .group_by(func.date(models.Health.date))
        .subquery()
    )

    results = await db.execute(
        select(models.Health).filter(models.Health.id.in_(select(subquery.c.max_id)))
    )
    return results.scalars().all()


# For Health v2 shortcut:
# def create_health(db: Session, health: schemas.HealthCreate):
#     db_health = models.Health(**health.model_dump())
#     db.add(db_health)
#     db.commit()
#     db.refresh(db_health)
#     return db_health


async def create_health(db: AsyncSession, health: schemas.HealthCreate):
    height = weight = heart_rate = energy = steps = water = sleep = None

    # For Health v1 shortcut + Auto Export Health app:
    metrics = health.data.get("metrics", [])

    for metric in metrics:
        name = metric.get("name")
        data_list = metric.get("data", [])
        if not data_list:
            continue

        data_point = data_list[0]
        qty = data_point.get("qty")

        if name == "height":
            height = round(qty, 1) if qty else None
        elif name == "weight_body_mass":
            weight = round(qty, 1) if qty else None
        elif name == "heart_rate":
            heart_rate = (
                round(data_point.get("Avg"), 1) if "Avg" in data_point else None
            )
        elif name == "step_count":
            steps = qty if qty else None
        elif name == "active_energy":
            energy = round(qty, 1) if qty else None
        elif name == "dietary_water":
            water = qty if qty else None
        elif name == "sleep_analysis":
            sleep_start_str = data_point.get("sleepStart")
            sleep_end_str = data_point.get("sleepEnd")
            awake_time = data_point.get("awake", 0)
            if sleep_start_str and sleep_end_str:
                try:
                    sleep_start = datetime.strptime(
                        sleep_start_str, "%Y-%m-%d %H:%M:%S %z"
                    )
                    sleep_end = datetime.strptime(sleep_end_str, "%Y-%m-%d %H:%M:%S %z")
                    sleep_duration = sleep_end - sleep_start
                    sleep = round(
                        (sleep_duration.total_seconds() / 3600) - awake_time, 2
                    )
                except ValueError:
                    sleep = None

    previous_health = await get_health(db)
    if previous_health:
        height = height if height is not None else previous_health.height
        weight = weight if weight is not None else previous_health.weight

    db_health = models.Health(
        height=height,
        weight=weight,
        heart_rate=heart_rate,
        energy=energy,
        steps=steps,
        water=water,
        sleep=sleep,
    )

    db.add(db_health)
    await db.commit()
    await db.refresh(db_health)
    return db_health


# Activity
async def get_activity_count(db: AsyncSession):
    activity_counts = await db.execute(
        select(
            models.Activity.name,
            func.count(models.Activity.id).label("count"),
            func.date(models.Activity.date).label("activity_date"),
        ).group_by(models.Activity.name, func.date(models.Activity.date))
    )

    result = {}
    for activity, count, activity_date in activity_counts:
        date_str = activity_date.isoformat()
        if date_str not in result:
            result[date_str] = {"date": date_str, "activities": {}}
        if activity in result[date_str]["activities"]:
            result[date_str]["activities"][activity] += count
        else:
            result[date_str]["activities"][activity] = count

    result_list = list(result.values())
    return result_list


async def get_activity(db: AsyncSession):
    result = await db.execute(select(models.Activity))
    return result.scalars().all()


async def create_activity(db: AsyncSession, name: schemas.ActivityCreate):
    db_activity = models.Activity(**name.model_dump())
    db.add(db_activity)
    await db.commit()
    await db.refresh(db_activity)
    return db_activity


async def update_activity(
    db: AsyncSession, name: str, activity: schemas.ActivityUpdate
):
    db_activity = (
        (
            await db.execute(
                select(models.Activity)
                .filter(models.Activity.name == name)
                .order_by(models.Activity.date.desc())
            )
        )
        .scalars()
        .first()
    )

    if db_activity:
        if activity.name is not None:
            db_activity.name = activity.name
        if activity.date is not None:
            db_activity.date = activity.date
        await db.commit()
        await db.refresh(db_activity)
        return db_activity


# Project
async def get_project(db: AsyncSession):
    result = await db.execute(select(models.Project))
    return result.scalars().all()


async def get_project_score(db: AsyncSession, time_range: str = "today"):
    from datetime import datetime, timedelta

    now = datetime.now(timezone.utc)

    if time_range == "today":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_range == "week":
        start_date = now - timedelta(days=7)
    elif time_range == "month":
        start_date = now - timedelta(days=30)
    elif time_range == "year":
        start_date = now - timedelta(days=365)
    else:  # "all"
        start_date = datetime.min.replace(tzinfo=timezone.utc)

    # Get project entries and count interactions per project
    result = await db.execute(
        select(
            models.Project.name,
            func.count(models.Project.id).label("interaction_count"),
        )
        .where(models.Project.date >= start_date)
        .group_by(models.Project.name)
        .order_by(desc("interaction_count"))
    )

    project_counts = result.all()
    if not project_counts:
        return []

    # Find the maximum number of interactions
    max_interactions = max(count for _, count in project_counts)

    # Calculate scores based on percentage of max_interactions
    project_scores = []
    for name, count in project_counts:
        percentage = (count / max_interactions) * 100
        if percentage >= 80:
            score = 5
        elif percentage >= 60:
            score = 4
        elif percentage >= 40:
            score = 3
        elif percentage >= 20:
            score = 2
        else:
            score = 1

        project_scores.append(
            schemas.ProjectScoreResponse(
                name=name, score=score, interaction_count=count
            )
        )

    return project_scores

    # to calculate project score based on time spent
    """
    one_week_ago = datetime.now(timezone.utc) - timedelta(weeks=1)

    # Get all project entries from the last week, ordered by date
    project_entries = (
        await db.execute(
            select(models.Project.name, models.Project.date)
            .filter(models.Project.date >= one_week_ago)
            .order_by(models.Project.date)
        )
    ).all()

    if not project_entries:
        return []

    # Calculate time spent on each project
    project_durations = {}
    for i in range(len(project_entries) - 1):
        current = project_entries[i]
        next_entry = project_entries[i + 1]

        # Calculate duration until next project switch
        duration = (
            next_entry.date - current.date
        ).total_seconds() / 3600  # Convert to hours

        project_durations[current.name] = (
            project_durations.get(current.name, 0) + duration
        )

    # Handle the last entry - assume it's active until now if it's the current day
    last_entry = project_entries[-1]
    if last_entry.date.date() == datetime.now(timezone.utc).date():
        duration = (datetime.now(timezone.utc) - last_entry.date).total_seconds() / 3600
        project_durations[last_entry.name] = (
            project_durations.get(last_entry.name, 0) + duration
        )

    if not project_durations:
        return []

    # Find the maximum time spent
    max_duration = max(project_durations.values())

    # Calculate scores based on percentage of max_duration
    project_scores = []
    for project_name, duration in project_durations.items():
        percentage = (duration / max_duration) * 100
        if percentage >= 80:
            score = 5
        elif percentage >= 60:
            score = 4
        elif percentage >= 40:
            score = 3
        elif percentage >= 20:
            score = 2
        else:
            score = 1

        project_scores.append(
            schemas.ProjectScoreResponse(name=project_name, score=score)
        )

    # Sort the project_scores list by score in descending order
    project_scores.sort(key=lambda x: x.score, reverse=True)
    return project_scores
    """


async def create_project(db: AsyncSession, project: schemas.ProjectCreate):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project


# Contact
async def get_contact_score(db: AsyncSession, time_range: str = "today"):
    from datetime import datetime, timedelta

    now = datetime.now(timezone.utc)

    if time_range == "today":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_range == "week":
        start_date = now - timedelta(days=7)
    elif time_range == "month":
        start_date = now - timedelta(days=30)
    elif time_range == "year":
        start_date = now - timedelta(days=365)
    else:  # "all"
        start_date = datetime.min.replace(tzinfo=timezone.utc)

    # Get contact entries and count interactions per person
    result = await db.execute(
        select(
            models.Contact.name,
            func.count(models.Contact.id).label("interaction_count"),
        )
        .where(models.Contact.date >= start_date)
        .group_by(models.Contact.name)
        .order_by(desc("interaction_count"))
    )

    contact_counts = result.all()
    if not contact_counts:
        return []

    # Find the maximum number of interactions
    max_interactions = max(count for _, count in contact_counts)

    # Calculate scores based on percentage of max_interactions
    contact_scores = []
    for name, count in contact_counts:
        percentage = (count / max_interactions) * 100
        if percentage >= 80:
            score = 5
        elif percentage >= 60:
            score = 4
        elif percentage >= 40:
            score = 3
        elif percentage >= 20:
            score = 2
        else:
            score = 1

        contact_scores.append(
            schemas.ContactScoreResponse(
                name=name, score=score, interaction_count=count
            )
        )

    return contact_scores


# Table
# async def get_entries(db: AsyncSession, table_name: str, skip: int = 0, limit: int = 10):
#     table = await get_table(table_name)
#     stmt = select(table).order_by(desc(table.c.date)).offset(skip).limit(limit)
#     results = (await db.execute(stmt)).fetchall()
#     return [{col.name: val for col, val in zip(table.columns, row)} for row in results]

# async def get_entry(db: AsyncSession, table_name: str, id: int):
#     table = await get_table(table_name)
#     stmt = select(table).where(table.c.id == id)
#     result = await db.execute(stmt)
#     row = result.first()
#     if row is None:
#         return None
#     return {col.name: val for col, val in zip(table.columns, row)}

# async def create_entry(db: AsyncSession, table_name: str, entry_data: dict):
#     if 'date' in entry_data:
#         entry_data['date'] = datetime.fromisoformat(entry_data['date'].replace("Z", "+00:00"))
#     table = await get_table(table_name)
#     stmt = table.insert().values(**entry_data)
#     result = await db.execute(stmt)
#     await db.commit()
#     return await get_entry(db, table_name, result.inserted_primary_key[0])

# async def update_entry(db: AsyncSession, table_name: str, id: int, entry_data: dict):
#     if 'date' in entry_data:
#         entry_data['date'] = datetime.fromisoformat(entry_data['date'].replace("Z", "+00:00"))

#     table = await get_table(table_name)
#     stmt = table.update().where(table.c.id == id).values(**entry_data)
#     await db.execute(stmt)
#     await db.commit()
#     return await get_entry(db, table_name, id)

# async def delete_entry(db: AsyncSession, table_name: str, id: int):
#     table = await get_table(table_name)
#     stmt = table.delete().where(table.c.id == id)
#     result = await db.execute(stmt)
#     await db.commit()
#     return result.rowcount > 0


class DynamicTableSchema:
    """Handles dynamic schema creation and validation for database tables"""

    @staticmethod
    async def create_schema_for_table(table: sa.Table) -> type[BaseModel]:
        """Creates a Pydantic model matching the table structure"""
        fields = {}
        for column in table.columns:
            python_type = DynamicTableSchema._map_sql_to_python_type(column)
            # Make fields optional for UPDATE operations
            fields[column.name] = (Optional[python_type], None)

        return create_model(
            f"Dynamic{table.name.capitalize()}Model",
            **fields,
            __config__=type("Config", (), {"from_attributes": True}),
        )

    @staticmethod
    def _map_sql_to_python_type(column: Column) -> type:
        """Maps SQL types to Python types"""
        if isinstance(column.type, sa.String):
            return str
        elif isinstance(column.type, sa.Integer):
            return int
        elif isinstance(column.type, sa.TIMESTAMP):
            return datetime
        elif isinstance(column.type, sa.Boolean):
            return bool
        elif isinstance(column.type, sa.Float):
            return float
        # Add more type mappings as needed
        return Any


async def get_tables_structure(db: AsyncSession) -> List[schemas.TableInfo]:
    """Fetch structure of all tables in the database."""
    async with db.begin():
        conn = await db.connection()
        tables = await conn.run_sync(lambda conn: inspect(conn).get_table_names())

        structures = []
        for table_name in tables:
            if table_name in ("alembic_version", "users"):
                continue
            columns = await conn.run_sync(
                lambda conn: inspect(conn).get_columns(table_name)
            )
            column_info = [
                schemas.ColumnInfo(name=col["name"], type=str(col["type"]))
                for col in columns
                if col["name"] != "id"  # Exclude 'id' column
            ]
            structures.append(schemas.TableInfo(name=table_name, columns=column_info))
    return structures


async def validate_data(
    table: Table, data: Dict[str, Any], is_update: bool = False
) -> Dict[str, Any]:
    """Validate and convert data to match the table's schema."""
    schema = await DynamicTableSchema.create_schema_for_table(table)
    for key, value in data.items():
        if key in table.columns and isinstance(table.columns[key].type, sa.TIMESTAMP):
            try:
                data[key] = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(f"Invalid datetime format for field {key}")
    return schema(**data).model_dump(exclude_unset=True)


async def get_table(db: AsyncSession, table_name: str, user_id: str = None) -> Table:
    """Fetch table by name, reflecting if necessary."""
    async with db.begin():
        conn = await db.connection()
        await conn.run_sync(metadata.reflect)

    full_table_name = (
        construct_table_name(user_id, table_name) if user_id else table_name
    )
    if full_table_name not in metadata.tables:
        raise NoSuchTableError(f"Table '{full_table_name}' not found")
    return metadata.tables[full_table_name]


async def get_entries(
    db: AsyncSession, table_name: str, skip: int, limit: int, user_id: str = None
) -> List[Dict[str, Any]]:
    """Retrieve paginated entries from a table ordered by date in descending order, excluding the id column."""
    table = await get_table(db, table_name, user_id)

    # Select all columns except 'id'
    columns = [col for col in table.c if col.name != "id"]

    query = select(*columns).offset(skip).limit(limit).order_by(table.c.datetime.desc())
    result = await db.execute(query)
    return [dict(row) for row in result.mappings()]


async def get_entry(
    db: AsyncSession, table_name: str, id: int, user_id: str = None
) -> Optional[Dict[str, Any]]:
    table = await get_table(db, table_name, user_id)
    query = select(table).where(table.c.id == id)
    result = await db.execute(query)
    row = result.mappings().first()
    return dict(row) if row else None


async def create_entry(
    db: AsyncSession, table_name: str, data: Dict[str, Any], user_id: str = None
) -> Dict[str, Any]:
    """Create a new entry in the specified table."""
    table = await get_table(db, table_name, user_id)
    data = await validate_data(table, data)
    stmt = table.insert().values(**data)
    result = await db.execute(stmt)
    await db.commit()
    return await get_entry(db, table_name, result.inserted_primary_key[0], user_id)


async def update_entry(
    db: AsyncSession,
    table_name: str,
    id: int,
    data: Dict[str, Any],
    user_id: str = None,
) -> Optional[Dict[str, Any]]:
    """Update an existing entry in the specified table."""
    table = await get_table(db, table_name, user_id)
    data = await validate_data(table, data, is_update=True)
    stmt = table.update().where(table.c.id == id).values(**data)
    result = await db.execute(stmt)
    await db.commit()
    return await get_entry(db, table_name, id, user_id) if result.rowcount > 0 else None


async def delete_entry(
    db: AsyncSession, table_name: str, id: int, user_id: str = None
) -> bool:
    """Delete an entry from the specified table by ID."""
    table = await get_table(db, table_name, user_id)
    stmt = table.delete().where(table.c.id == id)
    result = await db.execute(stmt)
    await db.commit()

    # Update has_data field in sessions table if this is a session table
    if "session_" in table_name:
        # Check if there are any remaining rows
        count_stmt = select(func.count()).select_from(table)
        count_result = await db.execute(count_stmt)
        remaining_rows = count_result.scalar()

        if remaining_rows == 0:
            session_id = int(table_name.split("_")[1])
            session = await db.get(models.Session, session_id)
            if session:
                session.has_data = False
                await db.commit()

    return result.rowcount > 0


# Table User
def construct_table_name(user_id: str, table_name: str) -> str:
    """Generate a secure table name based on the user_id and table_name."""
    sanitized_table_name = re.sub(r"[^a-zA-Z0-9_]", "", table_name)
    if not sanitized_table_name:
        raise ValueError(
            "Имя таблицы может содержать лишь английские буквы, цифры и символы подчёркивания"
        )
    return f"user_{user_id[:8]}_{sanitized_table_name}"


async def verify_table_ownership(user_id: str, table_name: str) -> bool:
    """Verify that a table belongs to the specified user."""
    full_table_name = construct_table_name(user_id, table_name)
    prefix = f"user_{user_id[:8]}_"
    return full_table_name.startswith(prefix)


async def get_user_tables(db: AsyncSession, user_id: str) -> List[str]:
    """Retrieve all tables for a given user."""
    prefix = f"user_{user_id[:8]}_"
    query = text(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_name LIKE :prefix
        """
    )
    result = await db.execute(query, {"prefix": f"{prefix}%"})
    return [row[0] for row in result.fetchall()]


async def create_user_table(
    db: AsyncSession, table_data: schemas.TableCreate, user_id: str
) -> str:
    """Create a new user-specific table."""
    try:
        full_table_name = construct_table_name(user_id, table_data.table_name)
        metadata_obj = MetaData()
        table = Table(
            full_table_name,
            metadata_obj,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("value", String, nullable=False),
            Column("datetime", TIMESTAMP, server_default=func.now()),
        )
        create_table_stmt = CreateTable(table)
        await db.execute(create_table_stmt)
        await db.commit()
        return full_table_name
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Failed to create table: {str(e)}")


async def delete_table(db: AsyncSession, table_name: str, user_id: str):
    """Delete a table using SQLAlchemy DDL."""
    try:
        full_table_name = construct_table_name(user_id, table_name)
        if not await verify_table_ownership(user_id, full_table_name):
            raise ValueError("Table ownership verification failed")

        table = Table(full_table_name, MetaData())
        drop_stmt = DropTable(table, if_exists=True)
        await db.execute(drop_stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Failed to delete table: {str(e)}")


async def rename_table(
    db: AsyncSession, old_name: str, new_name: str, user_id: str
) -> dict:
    """Rename a table safely."""
    try:
        new_full_name = construct_table_name(user_id, new_name)

        safe_old_name = quoted_name(old_name, True)
        safe_new_name = quoted_name(new_full_name, True)

        await db.execute(text(f"ALTER TABLE {safe_old_name} RENAME TO {safe_new_name}"))
        await db.commit()

        return {"status": "success", "old_name": old_name, "new_name": new_full_name}
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Failed to rename table: {str(e)}")


async def get_table_content(
    db: AsyncSession, table_name: str, skip: int, limit: int, user_id: str
) -> List[Dict[str, Any]]:
    """Retrieve paginated content of a table."""
    try:
        full_table_name = construct_table_name(user_id, table_name)

        # Get a connection
        connection = await db.connection()

        # Define a function to create the table object synchronously
        def get_table_object(conn):
            return Table(full_table_name, MetaData(), autoload_with=conn)

        # Create table object synchronously
        table = await connection.run_sync(get_table_object)

        query = (
            select(table).offset(skip).limit(limit).order_by(table.c.datetime.desc())
        )

        result = await db.execute(query)
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise ValueError(f"Failed to get table content: {str(e)}")


async def add_row(
    db: AsyncSession, table_name: str, data: Dict[str, Any], user_id: str = None
) -> Dict[str, Any]:
    """Add a new row to a table."""
    try:
        full_table_name = (
            construct_table_name(user_id, table_name) if user_id else table_name
        )
        connection = await db.connection()

        def get_table(conn):
            return Table(
                full_table_name,
                metadata,
                autoload_with=conn,
            )

        table = await connection.run_sync(get_table)

        # Validate the input data
        value = data.get("value")
        if not isinstance(value, (str, int, float, bool, datetime)):
            raise ValueError("Invalid value type")

        if "session_" in table_name:
            stmt = table.insert().values(
                value=value, datetime=data.get("datetime", datetime.now())
            )
        else:
            stmt = table.insert().values(
                value=value, datetime=data.get("datetime", datetime.now())
            )

        result = await db.execute(stmt)
        await db.commit()

        # Update has_data field in sessions table if this is a session table
        if "session_" in table_name:
            session_id = int(table_name.split("_")[1])
            session = await db.get(models.Session, session_id)
            if session:
                session.has_data = True
                await db.commit()

        return {
            "id": result.inserted_primary_key[0],
            "value": value,
            "datetime": data.get("datetime", datetime.now()),
        }

    except Exception as e:
        await db.rollback()
        raise ValueError(f"Failed to add row: {str(e)}")


async def update_row(
    db: AsyncSession,
    table_name: str,
    row_id: int,
    data: Dict[str, Any],
    user_id: str = None,
) -> Dict[str, Any]:
    """Update an existing row in the table."""
    full_table_name = (
        construct_table_name(user_id, table_name) if user_id else table_name
    )
    table = Table(full_table_name, metadata, autoload_with=db.bind)
    if not isinstance(data.get("value"), (str, int, float, bool, datetime)):
        raise ValueError("Invalid value type")
    try:
        stmt = table.update().where(table.c.id == row_id).values(value=data["value"])
        result = await db.execute(stmt)
        await db.commit()
        if result.rowcount:
            return {"id": row_id, "value": data["value"]}
        raise ValueError("Row not found.")
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Failed to update row: {str(e)}")


async def delete_row(
    db: AsyncSession, table_name: str, row_id: int, user_id: str = None
) -> bool:
    """Delete a row by ID."""
    full_table_name = (
        construct_table_name(user_id, table_name) if user_id else table_name
    )
    table = Table(full_table_name, metadata, autoload_with=db.bind)
    stmt = table.delete().where(table.c.id == row_id)
    result = await db.execute(stmt)
    await db.commit()

    # Update has_data field in sessions table if this is a session table
    if "session_" in table_name:
        # Check if there are any remaining rows
        count_stmt = select(func.count()).select_from(table)
        count_result = await db.execute(count_stmt)
        remaining_rows = count_result.scalar()

        if remaining_rows == 0:
            session_id = int(table_name.split("_")[1])
            session = await db.get(models.Session, session_id)
            if session:
                session.has_data = False
                await db.commit()

    return result.rowcount > 0


# Sessions
async def create_user_session(
    db: AsyncSession, session_data: schemas.SessionCreate, user_id: UUID
) -> models.Session:
    try:
        session = models.Session(**session_data.dict(), user_id=user_id)
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Failed to create session: {str(e)}")


async def get_user_session(
    db: AsyncSession, session_id: int, user_id: UUID
) -> models.Session:
    result = await db.execute(
        select(models.Session).where(
            models.Session.id == session_id, models.Session.user_id == user_id
        )
    )
    session = result.scalars().first()
    if not session:
        raise ValueError("Session not found")
    return session


async def get_user_sessions(
    db: AsyncSession, user_id: UUID, active_only: bool = True
) -> List[models.Session]:
    query = select(models.Session).where(models.Session.user_id == user_id)

    if active_only:
        query = query.where(
            models.Session.is_active == True, models.Session.is_paused == False
        )
    else:
        query = query.where(
            or_(models.Session.is_active == False, models.Session.is_paused == True)
        )

    result = await db.execute(query)
    sessions = result.scalars().all()

    # Check for expired sessions and update their status
    now = datetime.now(timezone.utc)
    for session in sessions:
        if session.end_time and session.end_time <= now and session.is_active:
            session.is_active = False
            db.add(session)

    await db.commit()

    # Refresh all sessions to ensure all attributes are loaded
    for session in sessions:
        await db.refresh(session)

    return sessions


async def update_user_session(
    db: AsyncSession, session_id: int, user_id: UUID, update_data: schemas.SessionUpdate
) -> models.Session:
    session = await get_user_session(db, session_id, user_id)
    update_data = update_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(session, key, value)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def soft_delete_session(db: AsyncSession, session_id: int, user_id: UUID) -> None:
    session = await get_user_session(db, session_id, user_id)
    session.is_active = False
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def delete_user_session(db: AsyncSession, session_id: int, user_id: UUID) -> None:
    session = await get_user_session(db, session_id, user_id)
    await db.delete(session)
    await db.commit()


async def pause_user_session(
    db: AsyncSession, session_id: int, user_id: UUID, is_paused: bool
) -> models.Session:
    session = await get_user_session(db, session_id, user_id)

    if is_paused and not session.is_paused:
        # Starting pause
        session.is_paused = True
        session.pause_start_time = datetime.now(timezone.utc)
    elif not is_paused and session.is_paused:
        # Ending pause
        pause_duration = datetime.now(timezone.utc) - session.pause_start_time
        session.end_time += pause_duration
        session.is_paused = False
        session.pause_start_time = None

    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def restore_user_session(
    db: AsyncSession, session_id: int, user_id: UUID
) -> models.Session:
    session = await get_user_session(db, session_id, user_id)
    session.is_active = True
    session.end_time = datetime.now(timezone.utc) + timedelta(days=1)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session
