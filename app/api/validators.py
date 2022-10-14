from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_before_edit(
    project_id: int,
    session: AsyncSession,
    full_amount: int = None,
    delete: bool = False
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    if project.fully_invested and not delete:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    if full_amount and full_amount < project.invested_amount:
        raise HTTPException(
            status_code=403,
            detail=(
                'Нельзя установить требуемую сумму меньше внесённой в проект!'
            )
        )
    if delete and project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project
