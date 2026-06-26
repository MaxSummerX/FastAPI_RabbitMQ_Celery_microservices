from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.users import IUserRepositoryAsync, IUserRepositorySync
from app.infrastructure.persistence.models import User as UserModel
from app.infrastructure.persistence.sqlalchemy.mapper import UserMapper


class UserSQLAlchemyRepositoryAsync(IUserRepositoryAsync):
    """
    Асинхронная SQLAlchemy реализация репозитория пользователей.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализирует репозиторий.

        Args:
            db: Асинхронная сессия SQLAlchemy
        """
        self.db = db

    async def get_by_id(self, user_id: UUID) -> User | None:
        """
        Получить пользователя по ID.

        Args:
            user_id: Уникальный идентификатор пользователя

        Returns:
            Объект User или None, если пользователь не найден
        """
        db_user = await self.db.scalar(select(UserModel).where(UserModel.id == user_id))

        if db_user:
            return UserMapper.to_domain(db_user)
        return None

    async def get_by_email(self, email: str) -> User | None:
        """
        Получить пользователя по email.

        Args:
            email: Email адрес

        Returns:
            Объект User или None, если пользователь не найден
        """
        db_user = await self.db.scalar(select(UserModel).where(UserModel.email == email))
        if db_user:
            return UserMapper.to_domain(db_user)
        return None

    async def create(self, user: User) -> User:
        """
        Создать нового пользователя.

        Args:
            User: Объект User с данными пользователя

        Returns:
            Созданный объект User
        """
        db_user = UserMapper.to_model(user)
        self.db.add(db_user)
        await self.db.commit()
        return user

    async def save(self, user: User) -> User:
        """
        Сохранить изменения пользователя.

        Args:
            User: Объект User с обновлёнными данными

        Returns:
            Сохранённый объект User
        """
        db_user = UserMapper.to_model(user)
        await self.db.merge(db_user)  # Скрытый INSERT
        await self.db.commit()
        return user

    async def delete(self, user_id: UUID) -> None:
        """
        Удалить пользователя по ID

        Args:
            user_id: Уникальный идентификатор пользователя
        """
        raise NotImplementedError  # TODO: Реализовать позже, нужно мягкое удаление

    async def get_by_oauth(self, oauth_provider: str, oauth_id: str) -> User | None:
        """
        Найти пользователя по OAuth провайдеру и ID.

        Args:
            oauth_provider: Название OAuth провайдера
            oauth_id: Уникальный идентификатор пользователя в OAuth

        Returns:
            Объект User или None, если пользователь не найден
        """
        db_user = await self.db.scalar(
            select(UserModel).where(UserModel.oauth_provider == oauth_provider, UserModel.oauth_id == oauth_id)
        )
        if db_user:
            return UserMapper.to_domain(db_user)

        return None


class UserSQLAlchemyRepositorySync(IUserRepositorySync):
    """
    Синхронная SQLAlchemy реализация репозитория пользователей.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> Sequence[User]:
        """Возвращает всех пользователей из базы данных.

        Returns:
            Sequence[User]: Список всех пользователей.
        """
        db_users = self.db.scalars(select(UserModel)).all()
        return [UserMapper.to_domain(user) for user in db_users]
