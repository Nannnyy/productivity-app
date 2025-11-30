from datetime import datetime, timezone
import time
import streamlit as st
from partials.BasePage import BasePage
from resources import UserResource
from resources import PomodoroResource

class Pomodoro(BasePage):
    def __init__(self):
        super().__init__("Pomodoro", ':material/timer:', 'centered', 'collapsed')    
        st.session_state['page'] = 'Pomodoro'
        
        self.userResource = UserResource()
        self.pomodoroResource = PomodoroResource()
        self.user_id = self.userResource.get_user_id_by_cookie()
        self.config_pomodoro = self.pomodoroResource.get_config(self.user_id)
    
    def get_current_state(self):
        session = self.pomodoroResource.get_current_session(self.user_id)
        cycle = self.pomodoroResource.get_current_cycle(self.user_id)
        config = self.pomodoroResource.get_config(self.user_id)
        
        completed_works = 0
        if cycle:
            completed_works = sum(1 for s in cycle.sessions if s.type == "work" and s.status == "completed")
        return {
            "session": session,
            "cycle": cycle,
            "config": config,
            "completed_works": completed_works,
            "total_works": config.pomodoros_per_cycle,
            "is_running": session and session.status == "running",
            "cycle_completed": cycle and cycle.status == "completed",
        }
    
    def calculate_remaining(self, session):
        if not session:
            return 0

        if session.status == "paused":
            return session.remaining_seconds or 0

        if session.status == "running" and session.started_at:
            now = datetime.now(timezone.utc)
            started = session.started_at
            if started.tzinfo is None:
                started = started.replace(tzinfo=timezone.utc)

            elapsed = (now - started).total_seconds()
            remaining = (session.remaining_seconds or 0) - int(elapsed)
            return max(0, remaining)

        return session.remaining_seconds or 0
    
    def draw_timer(self):
        state = self.get_current_state()
        session = state["session"]

        timer_text = f"{self.config_pomodoro.work_minutes}:00"
        session_type = "Pronto para começar"
        pomodoros_text = "0 pomodoros"

        if session:
            remaining = self.calculate_remaining(session)
            mins, secs = divmod(int(remaining), 60)
            timer_text = f"{mins:02d}:{secs:02d}"

            type_map = {
                "work": "Foco",
                "short_break": "Pausa curta",
                "long_break": "Pausa longa"
            }
            session_type = type_map.get(session.type, session.type.replace("_", " ").title())
            pomodoros_text = f"{state['completed_works']}/{state['total_works']} pomodoros"

            if remaining <= 0 and session.status == "running":
                self.pomodoroResource.complete_current_session(self.user_id)
                st.toast("Sessão concluída!", icon="party")
                st.rerun()

        elif state["cycle_completed"]:
            timer_text = "Ciclo Completo!"
            session_type = "Parabéns! Você finalizou o ciclo"
            pomodoros_text = f"{state['total_ work']}/{state['total_works']} pomodoros"
            st.success("Ciclo concluído com sucesso!")
            st.balloons()

        else:
            pomodoros_text = "0 pomodoros"

        st.markdown(f"""
        <div style="text-align: center; padding: 60px 0;">
            <h1 style="font-size: 130px; margin: 0; color: #ff4757; font-weight: bold;">
                {timer_text}
            </h1>
            <h3 style="color: #1e90ff; margin: 20px 0 10px 0;">{session_type}</h3>
            <p style="color: #95a5a6; font-size: 22px;">{pomodoros_text}</p>
        </div>
        """, unsafe_allow_html=True)

        if state["cycle"]:
            st.progress(state["completed_works"] / state["total_works"])
        elif state["cycle_completed"]:
            st.progress(1.0)
    
    def draw_buttons(self):
        state = self.get_current_state()
        session = state['session']
        
        col1, col2, col3 = st.columns(3)
        
        if col3.button('Resetar Tudo', use_container_width=True, type="secondary", icon=':material/rotate_auto:'):
            self.pomodoroResource.reset_all(self.user_id)
            st.toast('Tudo resetado')
            st.rerun()
        
        if not session:
            if col1.button('Iniciar Pomodoro', use_container_width=True, type="primary", icon=':material/play_arrow:'):
                success, result = self.pomodoroResource.start_pomodoro(self.user_id)
                if success:
                    st.toast('Pomodoro Iniciado')
                st.rerun()
        else:
            if session.status in ('running', 'paused'):
                pause_label = "Pausar" if session.status == "running" else "Retomar"
                pause_icon = ':material/pause:' if session.status == "running" else ':material/resume:'
                if col1.button(pause_label, use_container_width=True, type="primary", icon=pause_icon):
                    success, msg, sess = self.pomodoroResource.toggle_pause(self.user_id)
                    if success:
                        st.toast(msg)
                    st.rerun()
                
                if session.type == "work":
                    if col2.button("Completar Sessão", use_container_width=True, type="primary", icon=':material/skip_next:'):
                        success, new_sess = self.pomodoroResource.complete_current_session(self.user_id)
                        if success:
                            st.toast("Sessão concluída")
                        st.rerun()
                else:
                    if col2.button("Pular Intervalo", use_container_width=True, type="secondary", icon=':material/skip_next:'):
                        success, new_sess = self.pomodoroResource.skip_break(self.user_id)
                        if success:
                            st.toast("Pausa Pulada")
                        st.rerun()
    
    def auto_rerun(self):
        state = self.get_current_state()
        
        if state["is_running"]:
            time.sleep(1)
            st.rerun()

    @st.dialog('Configuração Pomodoro')
    def draw_config_pomodoro(self):
        work = st.number_input(
            'Tempo de trabalho (min)', min_value=1, max_value=120,
            value=self.config_pomodoro.work_minutes
        )
        
        short_break = st.number_input(
            'Pausa Curta (min)', min_value=1, max_value=30,
            value=self.config_pomodoro.short_break_minutes
        )
        
        long_break = st.number_input(
            "Pausa longa (min)", min_value=1, max_value=60,
            value=self.config_pomodoro.long_break_minutes
        )
        
        cycle = st.number_input(
            'Clicos antes da pausa longa', min_value=1, max_value=10,
            value=self.config_pomodoro.pomodoros_per_cycle
        )
        
        if st.button("Salvar", type="primary"):
            success, msg = self.pomodoroResource.update_config(
                self.user_id, work, long_break, short_break, cycle
            )
            
            if success:
                st.rerun()
            else:
                st.error(f"Ocorreu um erro ao atualizar configurações: {msg}")
    
    def draw(self):
        st.title("Pomodoro Timer")
        col1, col2 = st.columns([6.5, 2], gap='medium')
        if col2.button('Configurações', icon=':material/settings:'):
            self.draw_config_pomodoro()
        
        self.draw_timer()
        self.draw_buttons()

        session = self.pomodoroResource.get_current_session(self.user_id)

        self.auto_rerun()
        
if __name__ == "__main__":
    timer = Pomodoro()
    timer.mount()
    