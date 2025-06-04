from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

async def get_user(db: AsyncSession, user_id: int):
    return await db.get(User, user_id)