import streamlit as st
from partials.BasePage import BasePage
from resources import UserResource, PomodoroResource, TaskResource

class History(BasePage):
    def __init__(self):
        super().__init__("Histórico", '📊', 'wide', 'collapsed')    
        st.session_state['page'] = 'History'    
    
    def draw(self):
        userResource = UserResource()
        isAuthenticated = userResource.check_login_cookie()
        user_id = userResource.get_user_id_by_cookie()
        
        if not isAuthenticated:
            st.switch_page('main.py')
        
        st.title("📊 Histórico de Atividades")
        
        tab1, tab2 = st.tabs(["🍅 Pomodoros", "✅ Tarefas"])
        
        with tab1:
            self._render_pomodoro_history(user_id)
        
        with tab2:
            self._render_task_history(user_id)
    
    def _render_pomodoro_history(self, user_id):
        pomodoroResource = PomodoroResource()
        
        st.subheader("Ciclos Concluídos")
        success, cycles = pomodoroResource.get_completed_cycles(user_id)
        
        if success and cycles:
            for cycle in cycles:
                with st.expander(f"Ciclo #{cycle.cycle_number} - {cycle.completed_at.strftime('%d/%m/%Y %H:%M')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Iniciado:** {cycle.started_at.strftime('%d/%m/%Y %H:%M')}")
                        st.write(f"**Concluído:** {cycle.completed_at.strftime('%d/%m/%Y %H:%M')}")
                    
                    with col2:
                        work_sessions = [s for s in cycle.sessions if s.type == "work" and s.status == "completed"]
                        st.write(f"**Pomodoros:** {len(work_sessions)}")
                        duration = cycle.completed_at - cycle.started_at
                        st.write(f"**Duração:** {duration}")
        else:
            st.info("Nenhum ciclo concluído encontrado.")
        
        st.subheader("Sessões Recentes")
        success, sessions = pomodoroResource.get_completed_sessions(user_id)
        
        if success and sessions:
            for session in sessions[:10]:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                
                with col1:
                    icon = "🍅" if session.type == "work" else "☕"
                    st.write(f"{icon} {session.type.title()}")
                
                with col2:
                    st.write(f"{session.duration_minutes}min")
                
                with col3:
                    st.write(session.status.title())
                
                with col4:
                    st.write(session.completed_at.strftime('%d/%m/%Y %H:%M'))
        else:
            st.info("Nenhuma sessão concluída encontrada.")
    
    def _render_task_history(self, user_id):
        taskResource = TaskResource()
        
        st.subheader("Tarefas Concluídas")
        success, completed_tasks = taskResource.get_completed_tasks(user_id)
        
        if success and completed_tasks:
            for task in completed_tasks:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"✅ {task.title}")
                
                with col2:
                    st.write(task.finished_at.strftime('%d/%m/%Y %H:%M'))
        else:
            st.info("Nenhuma tarefa concluída encontrada.")

if __name__ == "__main__":
    history = History()
    history.mount()