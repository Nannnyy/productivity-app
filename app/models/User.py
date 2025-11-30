from datetime import timezone
import sqlalchemy as sa
from .database import Base

class User(Base):
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(255), nullable=False, unique=True)
    email = sa.Column(sa.String(255), nullable=False, unique=True)
    password = sa.Column(sa.String(), nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, default=sa.func.now(tzinfo=timezone.utc))
    updated_at = sa.Column(sa.DateTime, nullable=False, default=sa.func.now(tzinfo=timezone.utc))
    last_login = sa.Column(sa.DateTime, nullable=True)
    is_active = sa.Column(sa.Boolean, nullable=False, default=True)
    