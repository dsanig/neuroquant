from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Role, User, UserRole


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_active_user_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email, User.is_active.is_(True)))

    def get_by_id(self, user_id: str) -> User | None:
        return self.db.scalar(select(User).where(User.id == user_id, User.is_active.is_(True)))

    def get_role_names(self, user_id: str) -> list[str]:
        stmt = (
            select(Role.name)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
            .order_by(Role.name)
        )
        return [row for row in self.db.scalars(stmt).all()]
