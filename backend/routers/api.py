import crud
from database import get_db, get_user_db
import schemas
import models
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    APIRouter,
    Request,
    Security,
    status,
    Query,
)
from sqlalchemy import inspect
from typing import List, Dict, Any, Optional
from fastapi_cache.decorator import cache
from fastapi.security.api_key import APIKeyHeader
from settings import get_settings
from fastapi_users import FastAPIUsers, BaseUserManager, UUIDIDMixin
from uuid import UUID
from fastapi_users.authentication import (
    JWTStrategy,
    CookieTransport,
    AuthenticationBackend,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoSuchTableError

cfg = get_settings()

API_KEY = cfg.api_key
API_KEY_NAME = "API-KEY"
AUTH_TOKEN = cfg.auth_token
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")


api_router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


# User
class UserManager(UUIDIDMixin, BaseUserManager[models.User, UUID]):
    reset_password_token_secret = AUTH_TOKEN
    verification_token_secret = AUTH_TOKEN

    async def on_after_register(
        self, user: models.User, request: Optional[Request] = None
    ):
        # Set username to the part of email before @
        if not user.username and user.email:
            user.username = user.email.split("@")[0]
            await self.user_db.update(user, {"username": user.username})
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: models.User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: models.User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=AUTH_TOKEN, lifetime_seconds=604800)


cookie_transport = CookieTransport(cookie_max_age=604800, cookie_secure=False)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[models.User, UUID](get_user_manager, [auth_backend])
current_user = fastapi_users.current_user()

api_router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=False),
    prefix="/auth/jwt",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_verify_router(schemas.UserRead),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_users_router(schemas.UserRead, schemas.UserUpdate),
    prefix="/users",
    tags=["users"],
)


# Posts
@api_router.get("/posts/", response_model=list[schemas.PostResponse])
@cache(expire=60)
async def get_posts(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    db_posts = await crud.get_posts(db, skip=skip, limit=limit)
    if db_posts is None:
        raise HTTPException(status_code=404, detail="Posts not found")
    return db_posts


# @api_router.get("/api/posts/{id}", response_model=schemas.PostResponse)
# @cache(expire=60)
# async def get_post(id: int, db: AsyncSession = Depends(get_db)):
#     db_post = await crud.get_post(db, id=id)
#     if db_post is None:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return db_post

# @api_router.post("/api/posts/", response_model=schemas.PostResponse, dependencies=[Depends(get_api_key)])
# async def create_post(post: schemas.PostCreate, db: AsyncSession = Depends(get_db)):
#     db_post = await crud.create_post(db, post=post)
#     return db_post

# @api_router.delete("/api/posts/{id}", response_model=schemas.PostResponse, dependencies=[Depends(get_api_key)])
# async def delete_post(id: int, db: AsyncSession = Depends(get_db)):
#     db_post = await crud.delete_post(db, id=id)
#     return db_post


# Location
@api_router.get("/location/", response_model=schemas.LocationResponse)
@cache(expire=60)
async def get_location(db: AsyncSession = Depends(get_db)):
    db_location = await crud.get_location(db)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


# @api_router.post("/api/location/", response_model=schemas.LocationResponse, dependencies=[Depends(get_api_key)])
# async def create_location(location: schemas.LocationCreate, db: AsyncSession = Depends(get_db)):
#     return await crud.create_location(db, location=location)


# Health
@api_router.get("/health/", response_model=schemas.HealthResponse)
@cache(expire=60)
async def get_health(db: AsyncSession = Depends(get_db)):
    db_health = await crud.get_health(db)
    if db_health is None:
        raise HTTPException(status_code=404, detail="Health not found")
    return db_health


@api_router.get("/health_all/", response_model=List[schemas.HealthResponse])
@cache(expire=60)
async def get_health_all(db: AsyncSession = Depends(get_db)):
    return await crud.get_health_all(db)


@api_router.post(
    "/health_external/",
    response_model=schemas.HealthResponse,
    dependencies=[Depends(get_api_key)],
)
async def create_health(
    health: schemas.HealthCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_health(db, health=health)


# Activity
@api_router.get("/activity/", response_model=List[schemas.ActivityResponse])
@cache(expire=60)
async def get_activity(db: AsyncSession = Depends(get_db)):
    return await crud.get_activity(db)


@api_router.get("/activity_count/", response_model=List[schemas.ActivityCountResponse])
@cache(expire=60)
async def get_activity_count(db: AsyncSession = Depends(get_db)):
    return await crud.get_activity_count(db)


# @api_router.post("/api/activity/", response_model=schemas.ActivityResponse, dependencies=[Depends(get_api_key)])
# async def create_activity(name: schemas.ActivityCreate, db: AsyncSession = Depends(get_db)):
#     return await crud.create_activity(db, name=name)

# @api_router.put("/api/activity/{name}", response_model=schemas.ActivityResponse, dependencies=[Depends(get_api_key)])
# async def update_activity(name: str, activity: schemas.ActivityUpdate, db: AsyncSession = Depends(get_db)):
#     return await crud.update_activity(db, name=name, activity=activity)


# Project
@api_router.get("/project/", response_model=List[schemas.ProjectResponse])
@cache(expire=60)
async def get_project(db: AsyncSession = Depends(get_db)):
    return await crud.get_project(db)


@api_router.get(
    "/project_score/{time_range}", response_model=List[schemas.ProjectScoreResponse]
)
async def get_project_score(time_range: str, db: AsyncSession = Depends(get_db)):
    return await crud.get_project_score(db, time_range)


# @api_router.post("/api/project/", response_model=schemas.ProjectResponse, dependencies=[Depends(get_api_key)])
# async def create_project(project: schemas.ProjectCreate, db: AsyncSession = Depends(get_db)):
#     return await crud.create_project(db, project=project)


# Contact
@api_router.get(
    "/contact_score/{time_range}", response_model=List[schemas.ContactScoreResponse]
)
async def get_contact_score(time_range: str, db: AsyncSession = Depends(get_db)):
    return await crud.get_contact_score(db, time_range)


# Table
@api_router.get("/tables/structure/", response_model=List[schemas.TableInfo])
async def get_tables_structure(db: AsyncSession = Depends(get_db)):
    try:
        return await crud.get_tables_structure(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/{table_name}/latest/", response_model=List[Dict[str, Any]])
async def get_entries(
    table_name: str,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_user),
):
    try:
        return await crud.get_entries(db, table_name, skip, limit, str(user.id))
    except NoSuchTableError:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")


@api_router.get("/{table_name}/{id}", response_model=Dict[str, Any])
async def get_entry(
    table_name: str,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_user),
):
    entry = await crud.get_entry(db, table_name, id, str(user.id))
    if entry is None:
        raise HTTPException(
            status_code=404,
            detail=f"Entry with ID '{id}' not found in table '{table_name}'",
        )
    return entry


@api_router.post(
    "/{table_name}/", response_model=Dict[str, Any], dependencies=[Depends(get_api_key)]
)
async def create_entry(
    table_name: str,
    data: dict,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_user),
):
    return await crud.create_entry(db, table_name, data, str(user.id))


@api_router.put(
    "/{table_name}/{id}",
    response_model=Dict[str, Any],
    dependencies=[Depends(get_api_key)],
)
async def update_entry(
    table_name: str,
    id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_user),
):
    updated_entry = await crud.update_entry(db, table_name, id, data, str(user.id))
    if updated_entry is None:
        raise HTTPException(
            status_code=404,
            detail=f"Entry with ID '{id}' not found in table '{table_name}'",
        )
    return updated_entry


@api_router.delete(
    "/{table_name}/{id}",
    response_model=Dict[str, Any],
    dependencies=[Depends(get_api_key)],
)
async def delete_entry(
    table_name: str,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_user),
):
    success = await crud.delete_entry(db, table_name, id, str(user.id))
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Entry with ID '{id}' not found in table '{table_name}'",
        )
    return {"message": f"Entry with ID '{id}' deleted from table '{table_name}'"}


# Table User
@api_router.get("/users/table/", response_model=List[str])
async def list_user_tables(
    user: models.User = Depends(current_user), db: AsyncSession = Depends(get_db)
):
    """Get all tables for a user."""
    try:
        return await crud.get_user_tables(db, str(user.id))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@api_router.post("/users/table/", response_model=str)
async def create_table(
    table_data: schemas.TableCreate,
    user: models.User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new table for the user."""
    try:
        return await crud.create_user_table(db, table_data, str(user.id))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@api_router.delete("/users/table/{table_name}/", response_model=dict)
async def delete_table(
    table_name: str,
    user: models.User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await crud.delete_table(db, table_name, str(user.id))
        return {"message": f"Table {table_name} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.put("/users/table/{old_name}/rename/", response_model=dict)
async def rename_table(
    old_name: str,
    new_name: schemas.TableRename,
    user: models.User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    """Rename a table."""
    try:
        if not await crud.verify_table_ownership(str(user.id), old_name):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to rename this table",
            )
        return await crud.rename_table(db, old_name, new_name, str(user.id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.get("/users/table/{table_name}/rows/")
async def get_table_rows(
    table_name: str,
    skip: int = 0,
    limit: int = 1000000,  # until implemented lazy loading at frontend
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_user),
):
    try:
        return await crud.get_table_content(db, table_name, skip, limit, str(user.id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.post("/users/table/{table_name}/rows/")
async def add_table_row(
    table_name: str,
    data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_user),
):
    try:
        return await crud.add_row(db, table_name, data, str(user.id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.put("/users/table/{table_name}/rows/{row_id}/")
async def update_table_row(
    table_name: str,
    row_id: int,
    data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_user),
):
    try:
        return await crud.update_row(db, table_name, row_id, data, str(user.id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.delete("/users/table/{table_name}/rows/{row_id}/")
async def delete_table_row(
    table_name: str,
    row_id: int,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_user),
):
    try:
        return {"success": await crud.delete_row(db, table_name, row_id, str(user.id))}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Sessions
@api_router.post("/users/sessions/create", response_model=schemas.Session)
async def create_session(
    session_data: schemas.SessionCreate,
    user: models.User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        session = await crud.create_user_session(db, session_data, user.id)
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/users/sessions/get", response_model=List[schemas.Session])
async def list_sessions(
    active_only: bool = Query(True, description="Show only active sessions"),
    user: models.User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await crud.get_user_sessions(db, user.id, active_only)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/users/sessions/{session_id}/get", response_model=schemas.Session)
async def get_session(
    session_id: int,
    user: models.User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await crud.get_user_session(db, session_id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.put("/users/sessions/{session_id}/edit", response_model=schemas.Session)
async def update_session(
    session_id: int,
    session_data: schemas.SessionUpdate,
    user: models.User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await crud.update_user_session(db, session_id, user.id, session_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.delete("/users/sessions/{session_id}/soft_delete", status_code=204)
async def soft_delete_session(
    session_id: int,
    user: models.User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await crud.soft_delete_session(db, session_id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.delete("/users/sessions/{session_id}/delete", status_code=204)
async def delete_session(
    session_id: int,
    user: models.User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await crud.delete_user_session(db, session_id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.patch("/users/sessions/{session_id}/pause", response_model=schemas.Session)
async def pause_session(
    session_id: int,
    pause_data: schemas.SessionPause,
    user: models.User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await crud.pause_user_session(
            db, session_id, user.id, pause_data.is_paused
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.patch(
    "/users/sessions/{session_id}/restore", response_model=schemas.Session
)
async def restore_session(
    session_id: int,
    user: models.User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await crud.restore_user_session(db, session_id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
