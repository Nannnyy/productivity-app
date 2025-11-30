from datetime import timezone
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from .database import Base

class PomodoroCycle(Base):
    __tablename__ = "pomodoro_cycle"
    
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    cycle_number = sa.Column(sa.Integer, nullable=False)
    started_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=sa.func.now(tzinfo=timezone.utc))
    completed_at = sa.Column(sa.DateTime(timezone=True), nullable=True)
    status = sa.Column(sa.String, nullable=False, default="in_progress")
    
    sessions = relationship(
        "PomodoroSession",
        back_populates="cycle",
        cascade="all, delete-orphan",
        order_by="PomodoroSession.order_index"
    )

class PomodoroSession(Base):
    __tablename__ = "pomodoro_session"
    
    id = sa.Column(sa.Integer, primary_key=True)
    cycle_id = sa.Column(sa.Integer, sa.ForeignKey('pomodoro_cycle.id'), nullable=False, index=True)
    type = sa.Column(sa.String(), nullable=False)
    order_index = sa.Column(sa.Integer, nullable=False)
    duration_minutes = sa.Column(sa.Integer, nullable=False)
    remaining_seconds = sa.Column(sa.Integer, nullable=True)
    status = sa.Column(sa.String, nullable=False, default="pending")
    started_at = sa.Column(sa.DateTime(timezone=True), nullable=True)
    paused_at = sa.Column(sa.DateTime(timezone=True), nullable=True)
    completed_at = sa.Column(sa.DateTime(timezone=True), nullable=True)
    total_paused_seconds = sa.Column(sa.Integer, default=0)
    
    created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=sa.func.now(tzinfo=timezone.utc))
    
    cycle = relationship("PomodoroCycle", back_populates="sessions")


class PomodoroUserConfig(Base):
    __tablename__ = "pomodoro_user_config"
    
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), unique=True)
    
    work_minutes = sa.Column(sa.Integer, nullable=False, default=25)
    short_break_minutes = sa.Column(sa.Integer, nullable=False, default=5)
    long_break_minutes = sa.Column(sa.Integer, nullable=False, default=15)
    pomodoros_per_cycle = sa.Column(sa.Integer, nullable=False, default=4)