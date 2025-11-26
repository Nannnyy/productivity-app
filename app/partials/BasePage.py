import streamlit as st
from resources import UserResource
class BasePage:

    def __init__(
        self, title: str,
        icon: str,
        layout: str = "centered",
        sidebar_state: str = "collapsed",
    ):
        """
        Configura a página base com título, ícone, layout e estado da sidebar.
        
        Args:
            icon (str): Ícone da página, pode ser um emoji ou material icon (google).
            layout (str): Layout da página, pode ser "centered" ou "wide".
            sidebar_state (str): Estado da sidebar, pode ser "expanded" ou "collapsed".
        """
        try:
            st.set_page_config(
                page_title=title,
                page_icon=icon,
                layout=layout,
                initial_sidebar_state=sidebar_state,
            )
        except Exception as e:
            st.warning(f"Erro ao configurar página base: {e}")
            ...
    
    def mount(self, ):
        userResource = UserResource()
        isAuthenticated = userResource.check_login_cookie()
        if isAuthenticated:
            username, self.user = userResource.get_name_from_cookie(return_user=True)
            col1, _, col3, col4 = st.columns([1, 1, 1, 1])
            col1.caption(f"Olá, {username}")
            if col4.button("Logout", use_container_width=True):
                userResource.logout()
        self.draw()