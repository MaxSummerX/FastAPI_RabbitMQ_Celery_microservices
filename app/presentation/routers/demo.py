"""Demo-эндпоинт для создания пользователей в базе данных для тестирования рассылки"""

from uuid import uuid4

from fastapi import APIRouter, Depends, Query

from app.domain.entities.user import User
from app.domain.repositories.users import IUserRepositoryAsync
from app.presentation.dependencies import get_user_repo


router = APIRouter(prefix="/demo", tags=["Demo"])


@router.post("/created")
async def demo_created(
    count: int = Query(default=10, ge=1, le=50),
    user_repo: IUserRepositoryAsync = Depends(get_user_repo),
) -> dict[str, str]:
    """Создает пользователей в базе данных для тестирования рассылки"""
    users = [
        User.create_from_oauth(
            email=f"test_{uuid4()}@example.com",
            firstname=f"First_name_{i}",
            lastname=f"Last_name_{i}",
            oauth_provider="test",
            oauth_id=str(uuid4()),
        )
        for i in range(count)
    ]

    await user_repo.add_many_users(users)

    return {"message": f"Создано {count} пользователей"}
