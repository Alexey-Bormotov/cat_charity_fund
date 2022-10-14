from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.api.validators import (
    check_charity_project_before_edit, check_name_duplicate
)
from app.services.process_investments import (
    close_project_or_donation,
    process_investments
)

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await process_investments(session)
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    full_amount = (
        obj_in.full_amount if obj_in.full_amount is not None else None
    )
    existing_project = await check_charity_project_before_edit(
        project_id, session, full_amount=full_amount
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if full_amount == existing_project.invested_amount:
        existing_project.full_amount = full_amount
        close_project_or_donation(existing_project)
    updated_project = await charity_project_crud.update(
        existing_project, obj_in, session
    )
    return updated_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

    existing_project = await check_charity_project_before_edit(
        project_id, session, delete=True
    )
    deleted_project = await charity_project_crud.remove(
        existing_project, session
    )

    return deleted_project
