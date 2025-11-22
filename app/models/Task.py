from datetime import timezone
import sqlalchemy as sa
from  app.models.database import Base

class Task(Base):
    __tablename__ = "task"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, default=sa.func.now(tzinfo=timezone.utc))
    finished_at = sa.Column(sa.DateTime, nullable=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)