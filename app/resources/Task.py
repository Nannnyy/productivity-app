from datetime import datetime, timezone
from db import DatabaseSession
from models import Task
from sqlalchemy import select
import traceback
import streamlit as st

class TaskResource():
    
    def __init__(self):
        self.db = DatabaseSession()
        self.session = self.db.get_session()
    
    def create_task(self, title: str, user_id: int):
        try:
            task = Task(
                title=title,
                user_id=user_id
            )
            self.session.add(task)
            self.session.commit()
            return [True, task]
        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            return [False, str(e)]
    
    def get_tasks(self, user_id: int):
        try:
            stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
            tasks = self.session.scalars(stmt).all()
            return [True, tasks]
        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            return [False, str(e)]
    
    def complete_task(self, task_id: int, user_id: int):
        try:
            task = self.session.get(Task, task_id)
            if not task or task.user_id != user_id:
                return [False, "Tarefa não encontrada"]
            
            task.finished_at = datetime.now(timezone.utc)
            self.session.commit()
            return [True, task]
        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            return [False, str(e)]
    
    def delete_task(self, task_id: int, user_id: int):
        try:
            task = self.session.get(Task, task_id)
            if not task or task.user_id != user_id:
                return [False, "Tarefa não encontrada"]
            
            self.session.delete(task)
            self.session.commit()
            return [True, "Tarefa excluída"]
        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            return [False, str(e)]
    
    def get_completed_tasks(self, user_id: int):
        try:
            stmt = (
                select(Task)
                .where(Task.user_id == user_id, Task.finished_at.isnot(None))
                .order_by(Task.finished_at.desc())
            )
            tasks = self.session.scalars(stmt).all()
            return [True, tasks]
        except Exception as e:
            traceback.print_exc()
            return [False, e]