from datetime import datetime, timezone
from db import DatabaseSession
from models import User
from sqlalchemy import and_, select
from dotenv import load_dotenv
import traceback

from models import PomodoroCycle, PomodoroSession, PomodoroUserConfig

class PomodoroResource():
    
    def __init__(self):
        self.db = DatabaseSession()
        self.session = self.db.get_session()
    
    def get_config(self, user_id: int):
        config = self.session.scalar(
            select(PomodoroUserConfig).where(PomodoroUserConfig.user_id == user_id)
        )
        
        if not config:
            config = PomodoroUserConfig(user_id=user_id)
            self.session.add(config)
            self.session.commit()
        return config
    
    def _is_cycle_finished(self, user_id: int, cycle: PomodoroCycle) -> bool:
        completed_works = sum(1 for s in cycle.sessions if s.type == "work" and s.status == "completed")
        config = self.get_config(user_id)
        return completed_works >= config.pomodoros_per_cycle
    
    def get_current_cycle(self, user_id: int) -> PomodoroCycle:
        stmt = (
            select(PomodoroCycle).where(and_(
                PomodoroCycle.status == "in_progress",
                PomodoroCycle.user_id == user_id
            )).order_by(PomodoroCycle.started_at.desc()).limit(1)
        )
        return self.session.scalar(stmt)

    def get_current_session(self, user_id: int) -> PomodoroSession:
        cycle = self.get_current_cycle(user_id=user_id)
        if not cycle:
            return None
        
        for sess in reversed(cycle.sessions):
            if sess.status not in ('completed', 'skipped'):
                return sess
        return None
    
    def _create_next_session(self, cycle_id: int, user_id: int):
        try:
            cycle = self.session.get(PomodoroCycle, cycle_id)
            if not cycle:
                return [False, "Ciclo não encontrado"]

            config = self.get_config(user_id=user_id)

            completed_works = sum(1 for s in cycle.sessions if s.type == "work" and s.status == "completed")
            last_session = cycle.sessions[-1] if cycle.sessions else None
            next_index = len(cycle.sessions)

            # Se terminou o ciclo vai para a long break
            if completed_works >= config.pomodoros_per_cycle:
                next_type = "long_break"
                duration = config.long_break_minutes

            # Depois de work vai para pausa curta
            elif last_session and last_session.type == "work":
                next_type = "short_break"
                duration = config.short_break_minutes

            # Depois de break vai para novo work
            else:
                next_type = "work"
                duration = config.work_minutes

            new_session = PomodoroSession(
                cycle_id=cycle_id,
                type=next_type,
                order_index=next_index,
                duration_minutes=duration,
                remaining_seconds=duration * 60,
                status="running",
                started_at=datetime.now(timezone.utc)
            )

            self.session.add(new_session)
            self.session.commit()
            return [True, new_session]

        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            return [False, e]

        
    
    def start_pomodoro(self, user_id: int):
        try:
            # Se já tem sessão pausada, então só retoma
            current_session = self.get_current_session(user_id)
            if current_session and current_session.status == "paused":
                current_session.status = "running"
                self.session.commit()
                return [True, "Pomodoro retomado!"]

            # Se o ciclo atual já terminou, vai fechar ele
            cycle = self.get_current_cycle(user_id)
            if cycle and self._is_cycle_finished(cycle=cycle, user_id=user_id):
                cycle.status = "completed"
                cycle.completed_at = datetime.now(timezone.utc)
                self.session.commit()
                cycle = None

            # Cria novo ciclo se necessário
            if not cycle:
                last_cycle = self.session.scalar(
                    select(PomodoroCycle)
                    .where(PomodoroCycle.user_id == user_id)
                    .order_by(PomodoroCycle.cycle_number.desc())
                )
                new_number = (last_cycle.cycle_number + 1) if last_cycle else 1

                cycle = PomodoroCycle(
                    user_id=user_id,
                    cycle_number=new_number,
                    status="in_progress",
                    started_at=datetime.now(timezone.utc)
                )
                self.session.add(cycle)
                self.session.flush()

            # Cria a primeira sessão de trabalho
            config = self.get_config(user_id)
            order_index = len(cycle.sessions) if cycle.sessions else 0

            work_session = PomodoroSession(
                cycle_id=cycle.id,
                type="work",
                order_index=order_index,
                duration_minutes=config.work_minutes,
                remaining_seconds=config.work_minutes * 60,
                status="running",
                started_at=datetime.now(timezone.utc)
            )
            self.session.add(work_session)
            self.session.commit()

            return [True, work_session]

        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            return [False, str(e)]
    
    def complete_current_session(self, user_id):
        try:
            session = self.get_current_session(user_id=user_id)
            if not session:
                return [False, "Não existe uma sessão ativa"]
            
            session.status = "completed"
            session.completed_at = datetime.now(timezone.utc)
            session.remaining_seconds = 0
            self.session.commit()
            
            success, new_session = self._create_next_session(session.cycle_id, user_id)
            if success:
                return [True, new_session]
            else:
                return [False, new_session]
        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            return [False, e]
    
    def skip_break(self, user_id: int):
        try:
            session = self.get_current_session(user_id=user_id)
            print(f"Current session: {session.type}")

            if not session or session.type == "work":
                return [False, "Nenhuma pausa para pular"]

            cycle = self.get_current_cycle(user_id=user_id)
            if not cycle:
                return [False, "Nenhum ciclo ativo"]

            config = self.get_config(user_id)
            completed_works = sum(1 for s in cycle.sessions if s.type == "work" and s.status == "completed")

            # Se uma long_break for pulada, então o ciclo já acabou
            if session.type == "long_break":
                session.status = "skipped"
                session.completed_at = datetime.now(timezone.utc)
                session.remaining_seconds = 0

                cycle.status = "completed"
                cycle.completed_at = datetime.now(timezone.utc)

                self.session.commit()
                return [True, None]  

            session.status = "skipped"
            session.completed_at = datetime.now(timezone.utc)
            session.remaining_seconds = 0
            self.session.commit()

            return self._create_next_session(session.cycle_id, user_id)

        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            return [False, e]

    
    def toggle_pause(self, user_id: int):
        try:
            session = self.get_current_session(user_id=user_id)
            if not session:
                return [False, "Nenhuma sessão ativa"]

            now = datetime.now(timezone.utc)

            if session.status == "running":
                if not session.started_at:
                    return [False, "Erro: started_at nulo"]

                started_at = session.started_at
                if started_at.tzinfo is None:
                    started_at = started_at.replace(tzinfo=timezone.utc)

                elapsed = (now - started_at).total_seconds()
                remaining = session.remaining_seconds - int(elapsed)
                session.remaining_seconds = max(0, remaining)

                session.status = "paused"
                session.paused_at = now
                session.total_paused_seconds += int(elapsed)

                self.session.commit()
                return [True, "Pomodoro pausado", session]

            else:  
                session.status = "running"
                self.session.commit()
                return [True, "Pomodoro retomado!", session]

        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            return [False, str(e)]
    
    def reset_all(self, user_id: int):
        try:
            cycle = self.get_current_cycle(user_id=user_id)
            if not cycle:
                return [True, "Nada para resetar (nenhum ciclo ativo)"]

                
            cycle.status = "abandoned" 
            cycle.completed_at = datetime.now(timezone.utc)
            self.session.commit()

            return [True, "Ciclo resetado com sucesso"]

        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            return [False, str(e)]
    
    
    
    
        
            
            
            
        