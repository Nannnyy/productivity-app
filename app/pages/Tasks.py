import streamlit as st
from partials.BasePage import BasePage
from resources import UserResource, TaskResource

class Tasks(BasePage):
    def __init__(self):
        super().__init__("Tarefas", '', 'centered', 'collapsed')    
        st.session_state['page'] = 'Tasks'
        
        self.userResource = UserResource()
        self.taskResource = TaskResource()
        self.user_id = self.userResource.get_user_id_by_cookie()
    
    def draw_add_task(self):
        with st.container(border=True):
            with st.form("add_task_form", clear_on_submit=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    new_task = st.text_input("", placeholder="Digite o título da sua próxima tarefa...", label_visibility="collapsed")
                with col2:
                    submitted = st.form_submit_button("Adicionar", use_container_width=True)
                
            if submitted:
                if new_task.strip():
                    success, result = self.taskResource.create_task(new_task.strip(), self.user_id)
                    if success:
                        st.toast("Tarefa adicionada!")
                        st.rerun()
                    else:
                        st.error(f"Erro: {result}")
                else:
                    st.warning("Digite um título para a tarefa")
    
    def draw_task_list(self):
        success, tasks = self.taskResource.get_tasks(self.user_id)
        
        if not success:
            st.error(f"Erro ao carregar tarefas: {tasks}")
            return
        
        if not tasks:
            st.info("Nenhuma tarefa encontrada. Adicione uma nova tarefa acima.")
            return
        
        # Separar tarefas pendentes e concluídas
        pending_tasks = [t for t in tasks if not t.finished_at]
        completed_tasks = [t for t in tasks if t.finished_at]
        
        # Tarefas Pendentes
        if pending_tasks:
            st.subheader(f"Tarefas Pendentes ({len(pending_tasks)})")
            
            for task in pending_tasks:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([4, 1.5, 1.5])
                    
                    with col1:
                        st.write(task.title)
                        st.caption(f"Criada em: {task.created_at.strftime('%d/%m/%Y')}")
                    
                    with col2:
                        if st.button("Concluir", key=f"complete_{task.id}", use_container_width=True):
                            success, result = self.taskResource.complete_task(task.id, self.user_id)
                            if success:
                                st.toast("Tarefa concluída!")
                                st.rerun()
                            else:
                                st.error(f"Erro: {result}")
                    
                    with col3:
                        if st.button("Excluir", key=f"delete_{task.id}", use_container_width=True):
                            success, result = self.taskResource.delete_task(task.id, self.user_id)
                            if success:
                                st.toast("Tarefa excluída!")
                                st.rerun()
                            else:
                                st.error(f"Erro: {result}")
        
        # Tarefas Concluídas
        if completed_tasks:
            st.divider()
            with st.expander(f"Tarefas Concluídas ({len(completed_tasks)})", expanded=False):
                for task in completed_tasks:
                    with st.container(border=True):
                        col1, col2 = st.columns([5, 1.5])
                        
                        with col1:
                            st.write(f"~~{task.title}~~")
                            st.caption(f"Concluída em: {task.finished_at.strftime('%d/%m/%Y')}")
                        
                        with col2:
                            if st.button("Excluir", key=f"delete_completed_{task.id}", use_container_width=True):
                                success, result = self.taskResource.delete_task(task.id, self.user_id)
                                if success:
                                    st.toast("Tarefa excluída!")
                                    st.rerun()
                                else:
                                    st.error(f"Erro: {result}")
    
    def draw_header(self):
        username, _ = self.userResource.get_name_from_cookie(return_user=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"Olá, {username}")
        with col2:
            if st.button("Logout", use_container_width=True, key="logout_tasks"):
                self.userResource.logout()
                st.rerun()
        
        st.divider()
    
    def draw(self):
        isAuthenticated = self.userResource.check_login_cookie()
        if not isAuthenticated:
            st.switch_page('main.py')
        
        st.title("Tarefas")
        
        self.draw_add_task()
        self.draw_task_list()

if __name__ == "__main__":
    tasks = Tasks()
    tasks.mount()