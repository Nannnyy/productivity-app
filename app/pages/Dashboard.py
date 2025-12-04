import streamlit as st
from partials.BasePage import BasePage
from resources import UserResource

class Dashboard:
    def __init__(self):
        st.set_page_config(
            page_title="Dashboard",
            page_icon="📋",
            layout="wide",
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
        .stApp {
            background-color: #ffffff;
        }
        .stApp > header {
            display: none;
        }
        .main .block-container {
            padding-top: 0;
            padding-bottom: 0;
            background-color: #ffffff;
        }
        .block-container {
            padding-top: 0 !important;
            background-color: #ffffff;
        }
        .navbar {
            background: linear-gradient(90deg, #1f1f1f 0%, #333333 100%);
            padding: 0.75rem 0;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            width: 100%;
            z-index: 999;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            height: 60px;
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
            background-color: #ffffff;
            text-align: center;
            color: #666;
            font-size: 0.85rem;
            padding: 1rem 0;
            border-top: 1px solid #eee;
            font-style: italic;
            z-index: 998;
        }
        .stTextInput > div > div > input {
            background-color: #f8f9fa !important;
            border: 0.5px solid #e9ecef !important;
            color: #1f1f1f !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #333333 !important;
            box-shadow: 0 0 0 0.2rem rgba(51, 51, 51, 0.25) !important;
        }
        .stTextInput button {
            background-color: transparent !important;
            border: none !important;
            color: #000000 !important;
        }
        .stTextInput button:hover {
            color: #000000 !important;
            background-color: transparent !important;
        }
        .stButton > button[kind="secondary"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #333333 !important;
        }
        .stButton > button[kind="secondary"]:hover {
            background-color: #f8f9fa !important;
            color: #000000 !important;
        }
        .stFormSubmitButton > button {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #000000 !important;
        }
        .stFormSubmitButton > button:hover {
            background-color: #333333 !important;
            color: #ffffff !important;
        }
        .main-content {
            margin-top: 65px;
            margin-bottom: 60px;
        }
        .logout-button {
            position: fixed !important;
            top: 12px !important;
            right: 30px !important;
            z-index: 1001 !important;
            margin: 0 !important;
            height: 36px !important;
        }
        .logout-button button {
            background-color: transparent !important;
            color: #ffffff !important;
            border: 1px solid #ffffff !important;
            padding: 0.5rem 1rem !important;
            border-radius: 4px !important;
            font-size: 0.9rem !important;
        }
        .logout-button button:hover {
            background-color: #ffffff !important;
            color: #1f1f1f !important;
        }
        div[data-testid="stDataFrame"] {
            background-color: #ffffff !important;
        }
        div[data-testid="stDataFrame"] table {
            background-color: #ffffff !important;
            border-collapse: collapse !important;
        }
        div[data-testid="stDataFrame"] th {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #000000 !important;
            padding: 8px !important;
        }
        div[data-testid="stDataFrame"] td {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #000000 !important;
            padding: 8px !important;
        }
        div[data-testid="stDataFrame"] tr {
            background-color: #ffffff !important;
        }
        .stAlert {
            color: #000000 !important;
        }
        .stAlert > div {
            color: #000000 !important;
        }
        
        /* Responsividade Mobile */
        @media (max-width: 768px) {
            .navbar-content {
                padding: 0 1rem;
                flex-wrap: wrap;
            }
            .navbar-user {
                font-size: 0.9rem;
            }
            .main-content {
                margin-top: 80px;
            }
            
            /* Forçar layout vertical no mobile */
            div[data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-direction: column !important;
                gap: 1rem !important;
            }
            
            div[data-testid="column"] {
                width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            
            .desktop-divider {
                display: none !important;
            }
            
            div[style*="text-align: center"] {
                text-align: center !important;
            }
            
            /* Centralizar TUDO no mobile */
            * {
                text-align: center !important;
            }
            
            div, p, h1, h2, h3, h4, h5, h6 {
                text-align: center !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }
            
            .stButton > button {
                margin: 0 auto !important;
                display: block !important;
            }
            
            .stForm {
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
            }
            
            .stTextInput {
                display: flex !important;
                justify-content: center !important;
            }
            
            .stDataFrame {
                display: flex !important;
                justify-content: center !important;
            }
            
            .stContainer {
                text-align: center !important;
            }
            
            /* Centralizar timer especificamente */
            div[style*="font-size: 120px"] {
                text-align: center !important;
                margin: 0 auto !important;
                display: flex !important;
                justify-content: center !important;
            }
            
            div[style*="text-align: center"] {
                margin: 0 auto !important;
                display: block !important;
            }
        }
        
        @media (max-width: 480px) {
            .navbar-brand {
                font-size: 1.2rem;
            }
            .navbar-user {
                font-size: 0.8rem;
            }
            .main-content {
                padding: 0 0.5rem;
            }
            div[style*="font-size: 120px"] h1 {
                font-size: 80px !important;
            }
            .stButton > button {
                height: 2.5rem;
                font-size: 0.9rem;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Navbar tradicional no topo com botão de sair integrado
        st.markdown(f"""
        <div class="navbar">
            <div class="navbar-content">
                <div class="navbar-brand">Productivity App</div>
                <div class="navbar-user">
                    <span>Olá, {username}</span>
                    <form method="get" style="display: inline; margin-left: 1rem;">
                        <button type="submit" name="logout" value="true" class="navbar-logout">Sair</button>
                    </form>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Verificar se logout foi solicitado
        if st.query_params.get("logout") == "true":
            userResource.logout()
            st.query_params.clear()
            st.switch_page('main.py')
        
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
        <div style="text-align: center; padding: 10px 0;">
            <h1 style="font-size: 120px; margin: 0; color: #ff4757; font-weight: bold;">
                {timer_text}
            </h1>
            <h3 style="color: #000000; margin: 20px 0 10px 0;">{session_type}</h3>
            <p style="color: #95a5a6; font-size: 18px;">{pomodoros_text}</p>
        </div>
        """, unsafe_allow_html=True)
        

        
        # Botões do Pomodoro centralizados
        if not session:
            # Botões Iniciar e Resetar lado a lado centralizados
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
            
            with col2:
                if st.button('Iniciar Pomodoro', use_container_width=True, type="primary"):
                    success, result = pomodoroResource.start_pomodoro(user_id)
                    if success:
                        st.toast('Pomodoro Iniciado')
                    st.rerun()
            
            with col4:
                if st.button('Resetar', use_container_width=True, type="secondary"):
                    pomodoroResource.reset_all(user_id)
                    st.toast('Resetado')
                    st.rerun()
        else:
            # Botões durante sessão ativa
            if session.status in ('running', 'paused'):
                col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1.5])
                
                pause_label = "Pausar" if session.status == "running" else "Retomar"
                with col2:
                    if st.button(pause_label, use_container_width=True, type="primary"):
                        success, msg, sess = pomodoroResource.toggle_pause(user_id)
                        if success:
                            st.toast(msg)
                        st.rerun()
                
                if session.type == "work":
                    with col3:
                        if st.button("Completar", use_container_width=True, type="primary"):
                            success, new_sess = pomodoroResource.complete_current_session(user_id)
                            if success:
                                st.toast("Sessão concluída")
                            st.rerun()
                else:
                    with col3:
                        if st.button("Pular Pausa", use_container_width=True, type="secondary"):
                            success, new_sess = pomodoroResource.skip_break(user_id)
                            if success:
                                st.toast("Pausa Pulada")
                            st.rerun()
                
                with col4:
                    if st.button('Resetar', use_container_width=True, type="secondary"):
                        pomodoroResource.reset_all(user_id)
                        st.toast('Resetado')
                        st.rerun()
        
        # Layout responsivo
        st.divider()
        
        # Detectar largura da tela via JavaScript
        st.markdown("""
        <script>
        if (window.innerWidth <= 768) {
            document.body.classList.add('mobile-view');
        }
        </script>
        """, unsafe_allow_html=True)
        
        # Layout adaptativo baseado em CSS
        left_col, middle_col, right_col = st.columns([5, 0.1, 5])
        
        # Linha vertical no meio (oculta no mobile via CSS)
        with middle_col:
            st.markdown("""
            <div class="desktop-divider" style="height: 500px; border-left: 1px solid #e9ecef; margin: 0 auto; width: 1px;"></div>
            """, unsafe_allow_html=True)
        

        
        # Coluna Esquerda - Tarefas (conteúdo original completo)
        with left_col:
            st.subheader("Tarefas")
            
            # Importar TaskResource
            from resources import TaskResource
            taskResource = TaskResource()
            
            # Formulário para adicionar tarefa
            with st.form("add_task_form", clear_on_submit=True, border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    new_task = st.text_input("", placeholder="Digite o título da sua próxima tarefa...", label_visibility="collapsed")
                with col2:
                    submitted = st.form_submit_button("Adicionar", use_container_width=True, type="primary")
                    
                if submitted:
                    if new_task.strip():
                        success, result = taskResource.create_task(new_task.strip(), user_id)
                        if success:
                            st.toast("Tarefa adicionada!")
                            st.rerun()
                        else:
                            st.error(f"Erro: {result}")
                    else:
                        st.warning("Digite um título para a tarefa")
            
            # Lista de tarefas
            success, tasks = taskResource.get_tasks(user_id)
            
            if success and tasks:
                # Tarefas Pendentes
                pending_tasks = [t for t in tasks if not t.finished_at]
                
                if pending_tasks:
                    st.write(f"**Tarefas Pendentes ({len(pending_tasks)})**")
                    
                    for task in pending_tasks:
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([4, 1.5, 1.5])
                            
                            with col1:
                                st.write(task.title)
                                st.caption(f"Criada em: {task.created_at.strftime('%d/%m/%Y')}")
                            
                            with col2:
                                if st.button("Concluir", key=f"complete_{task.id}", use_container_width=True, type="primary"):
                                    success, result = taskResource.complete_task(task.id, user_id)
                                    if success:
                                        st.toast("Tarefa concluída!")
                                        st.rerun()
                                    else:
                                        st.error(f"Erro: {result}")
                            
                            with col3:
                                if st.button("Excluir", key=f"delete_{task.id}", use_container_width=True):
                                    success, result = taskResource.delete_task(task.id, user_id)
                                    if success:
                                        st.toast("Tarefa excluída!")
                                        st.rerun()
                                    else:
                                        st.error(f"Erro: {result}")
                

            else:
                st.info("Nenhuma tarefa encontrada. Adicione uma nova tarefa acima.")
        
        # Coluna Direita - Histórico (conteúdo original completo)
        with right_col:
            st.subheader("Histórico de Atividades")
            
            tab1, tab2 = st.tabs(["Pomodoros", "Tarefas"])
            
            with tab1:
                st.write("**Ciclos Concluídos**")
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
                
                st.write("**Sessões Recentes**")
                success, sessions = pomodoroResource.get_completed_sessions(user_id)
                
                if success and sessions:
                    import pandas as pd
                    
                    data = []
                    for session in sessions[:10]:
                        data.append({
                            "Tipo": session.type.title(),
                            "Duração": f"{session.duration_minutes}min",
                            "Status": session.status.title(),
                            "Data": session.completed_at.strftime('%d/%m/%Y %H:%M')
                        })
                    
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("Nenhuma sessão concluída encontrada.")
            
            with tab2:
                st.write("**Tarefas Concluídas**")
                success, completed_tasks = taskResource.get_completed_tasks(user_id)
                
                if success and completed_tasks:
                    import pandas as pd
                    
                    data = []
                    for task in completed_tasks:
                        data.append({
                            "Tarefa": task.title,
                            "Data de Conclusão": task.finished_at.strftime('%d/%m/%Y %H:%M')
                        })
                    
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("Nenhuma tarefa concluída encontrada.")
        
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