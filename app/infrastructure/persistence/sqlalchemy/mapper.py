from app.domain.entities.user import User
from app.infrastructure.persistence.models.user import User as UserModel


class UserMapper:
    @staticmethod
    def to_domain(user_model: UserModel) -> User:
        """Преобразует ORM-модель в доменную сущность User."""
        return User(
            id=user_model.id,
            firstname=user_model.firstname,
            lastname=user_model.lastname,
            email=user_model.email,
            oauth_provider=user_model.oauth_provider,
            oauth_id=user_model.oauth_id,
        )

    @staticmethod
    def to_model(user: User) -> UserModel:
        """Преобразует доменную сущность User в ORM-модель."""
        return UserModel(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            oauth_provider=user.oauth_provider,
            oauth_id=user.oauth_id,
        )
