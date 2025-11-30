import streamlit as st
from partials.BasePage import BasePage
from resources import UserResource

class Dashboard(BasePage):
    def __init__(self):
        super().__init__("Dashboard", '', 'centered', 'collapsed')    
        st.session_state['page'] = 'Dashboard'    
    
    def draw(self):
        userResource = UserResource()
        isAuthenticated = userResource.check_login_cookie()
        user_id = userResource.get_user_id_by_cookie()
        if not isAuthenticated:
            st.switch_page('main.py')
        with st.container(border=True):
            st.write(f"Bem-vindo ao Dashboard, {user_id}")
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            if col1.button("Pomodoro Timer", use_container_width=True, type="primary"):
                st.switch_page('pages/Pomodoro.py')
                
            if col2.button("Tarefas", use_container_width=True, type="secondary"):
                st.switch_page('pages/Tasks.py')
    
if __name__ == "__main__":
        dashboard = Dashboard()
        dashboard.mount()