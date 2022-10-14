from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


def close_project_or_donation(obj):
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def process_investments(
    session: AsyncSession
):
    projects = await session.execute(
        select(CharityProject).where(
            ~CharityProject.fully_invested
        ).order_by(CharityProject.create_date)
    )
    for project in projects.scalars().all():
        donations = await session.execute(
            select(Donation).where(
                ~Donation.fully_invested
            ).order_by(Donation.create_date)
        )
        for donation in donations.scalars().all():
            project_amount_left = (
                project.full_amount - project.invested_amount
            )
            donation_amount_left = (
                donation.full_amount - donation.invested_amount
            )
            if project_amount_left > donation_amount_left:
                project.invested_amount += donation_amount_left
                close_project_or_donation(donation)
            elif project_amount_left < donation_amount_left:
                donation.invested_amount += project_amount_left
                close_project_or_donation(project)
            else:  # project_amount_left == donation_amount_left
                close_project_or_donation(project)
                close_project_or_donation(donation)
            session.add(project)
            session.add(donation)
            if project.fully_invested:
                break
    await session.commit()
