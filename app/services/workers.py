from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import Role, UserRole, WorkSession


class WorkerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_workers(self) -> list[int]:
        query = (
            select(WorkSession.user_id)
            .join(UserRole, UserRole.user_id == WorkSession.user_id)
            .where(WorkSession.is_active.is_(True), UserRole.role_name == Role.worker)
            .order_by(WorkSession.started_at.asc())
        )
        rows = await self.session.execute(query)
        return [r[0] for r in rows.all()]

    async def assign_worker_round_robin(self, order_id: int, candidates: list[int]) -> int | None:
        if not candidates:
            return None
        assigned = candidates[order_id % len(candidates)]
        return assigned
