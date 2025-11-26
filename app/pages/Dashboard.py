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
            # Código de exemplo
            st.write(f"Bem-vindo ao Dashboard, {user_id}")
    
if __name__ == "__main__":
        dashboard = Dashboard()
        dashboard.mount()