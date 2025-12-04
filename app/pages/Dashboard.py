import streamlit as st
from partials.BasePage import BasePage
from resources import UserResource

class Dashboard:
    def __init__(self):
        st.set_page_config(
            page_title="Dashboard",
            page_icon="📋",
            layout="centered",
            initial_sidebar_state="collapsed"
        )
        st.session_state['page'] = 'Dashboard'    
    
    def draw(self):
        userResource = UserResource()
        isAuthenticated = userResource.check_login_cookie()
        user_id = userResource.get_user_id_by_cookie()
        if not isAuthenticated:
            st.switch_page('main.py')
        
        username, _ = userResource.get_name_from_cookie(return_user=True)
        
        # CSS para navbar tradicional e estilos
        st.markdown("""
        <style>
        .stApp > header {
            display: none;
        }
        .main .block-container {
            padding-top: 0;
        }
        .navbar {
            background: linear-gradient(90deg, #1f1f1f 0%, #333333 100%);
            padding: 1rem 0;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            width: 100%;
            z-index: 999;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .navbar-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .main-content {
            margin-top: 80px;
        }
        .navbar-brand {
            color: #ffffff;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 0;
        }
        .navbar-user {
            color: #ffffff;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .navbar-logout {
            background-color: transparent;
            color: #ffffff;
            border: 1px solid #ffffff;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s;
        }
        .navbar-logout:hover {
            background-color: #ffffff;
            color: #1f1f1f;
        }
        h1 {
            font-weight: 300;
            color: #1f1f1f;
        }
        .stButton > button {
            border-radius: 6px;
            height: 3rem;
            font-weight: 500;
        }
        .stButton > button[kind="primary"] {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #000000 !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #333333 !important;
            color: #ffffff !important;
        }
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            width: 100%;
            background-color: #f8f9fa;
            text-align: center;
            color: #666;
            font-size: 0.85rem;
            padding: 1rem 0;
            border-top: 1px solid #eee;
            font-style: italic;
            z-index: 998;
        }
        .main-content {
            margin-top: 80px;
            margin-bottom: 60px;
            min-height: calc(100vh - 140px);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Navbar tradicional no topo com logout
        st.markdown(f"""
        <div class="navbar">
            <div class="navbar-content">
                <div class="navbar-brand">Productivity App</div>
                <div class="navbar-user">
                    <span>Olá, {username}</span>
                    <button class="navbar-logout" onclick="window.location.href='/main.py'">Logout</button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Conteúdo principal com margem
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
        # Importar e usar PomodoroResource
        from resources import PomodoroResource
        pomodoroResource = PomodoroResource()
        
        # Funções do Pomodoro integradas
        def get_current_state():
            session = pomodoroResource.get_current_session(user_id)
            cycle = pomodoroResource.get_current_cycle(user_id)
            config = pomodoroResource.get_config(user_id)
            
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
        
        def calculate_remaining(session):
            if not session:
                return 0
            if session.status == "paused":
                return session.remaining_seconds or 0
            if session.status == "running" and session.started_at:
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
                started = session.started_at
                if started.tzinfo is None:
                    started = started.replace(tzinfo=timezone.utc)
                elapsed = (now - started).total_seconds()
                remaining = (session.remaining_seconds or 0) - int(elapsed)
                return max(0, remaining)
            return session.remaining_seconds or 0
        
        # Timer do Pomodoro
        state = get_current_state()
        session = state["session"]
        config = state["config"]
        
        timer_text = f"{config.work_minutes}:00"
        session_type = "Pronto para começar"
        pomodoros_text = "0 pomodoros"
        
        if session:
            remaining = calculate_remaining(session)
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
                pomodoroResource.complete_current_session(user_id)
                st.toast("Sessão concluída!", icon="party")
                st.rerun()
        
        # Display do Timer
        st.markdown(f"""
        <div style="text-align: center; padding: 40px 0;">
            <h1 style="font-size: 100px; margin: 0; color: #ff4757; font-weight: bold;">
                {timer_text}
            </h1>
            <h3 style="color: #1e90ff; margin: 20px 0 10px 0;">{session_type}</h3>
            <p style="color: #95a5a6; font-size: 18px;">{pomodoros_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if state["cycle"]:
            st.progress(state["completed_works"] / state["total_works"])
        elif state["cycle_completed"]:
            st.progress(1.0)
        
        # Botões do Pomodoro
        col1, col2, col3 = st.columns(3)
        
        if col3.button('Resetar', use_container_width=True, type="secondary"):
            pomodoroResource.reset_all(user_id)
            st.toast('Resetado')
            st.rerun()
        
        if not session:
            if col1.button('Iniciar Pomodoro', use_container_width=True, type="primary"):
                success, result = pomodoroResource.start_pomodoro(user_id)
                if success:
                    st.toast('Pomodoro Iniciado')
                st.rerun()
        else:
            if session.status in ('running', 'paused'):
                pause_label = "Pausar" if session.status == "running" else "Retomar"
                if col1.button(pause_label, use_container_width=True, type="primary"):
                    success, msg, sess = pomodoroResource.toggle_pause(user_id)
                    if success:
                        st.toast(msg)
                    st.rerun()
                
                if session.type == "work":
                    if col2.button("Completar", use_container_width=True, type="primary"):
                        success, new_sess = pomodoroResource.complete_current_session(user_id)
                        if success:
                            st.toast("Sessão concluída")
                        st.rerun()
                else:
                    if col2.button("Pular Pausa", use_container_width=True, type="secondary"):
                        success, new_sess = pomodoroResource.skip_break(user_id)
                        if success:
                            st.toast("Pausa Pulada")
                        st.rerun()
        
        # Navegação para outras páginas
        st.divider()
        nav_col1, nav_col2 = st.columns(2)
        
        if nav_col1.button("Gerenciar Tarefas", use_container_width=True, type="secondary"):
            st.switch_page('pages/Tasks.py')
            
        if nav_col2.button("Histórico", use_container_width=True):
            st.info("Em desenvolvimento")
        
        # Auto-refresh para timer ativo
        if state["is_running"]:
            import time
            time.sleep(1)
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)  # Fecha main-content
        
        # Footer fixo no final da página
        st.markdown(
            '<div class="footer">App de Produtividade • Pomodoro & Tarefas</div>',
            unsafe_allow_html=True
        )
    
    def mount(self):
        self.draw()
    
if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.mount()