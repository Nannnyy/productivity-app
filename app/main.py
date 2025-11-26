import streamlit as st
import os
import sys

from resources import UserResource
from partials.BasePage import BasePage
from streamlit import switch_page

class Main(BasePage):
    def __init__(self):
        super().__init__('Login', '🔑', 'centered', 'collapsed')
        st.session_state['page'] = 'login'
        
    def draw(self):
        userResource = UserResource()
        isAuthenticated = userResource.check_login_cookie()
        if isAuthenticated:
            # Redirecioonar para a página inicial, por exemplo de dashboard...
            switch_page('pages/Dashboard.py')
            st.success(f"Você está logado")
            
        with st.container(border=True):
            usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            c1, _, _, c2 = st.columns([1, 2, 2, 1])
            if c1.button('Entrar', disabled=not usuario or not senha):
                #Logica para checar senha
                response = userResource.login(usuario,senha)
                if response[0] is True:
                    # Logou, portanto redirecionar para a página inicial
                    switch_page('pages/Dashboard.py')   
                    st.success(f"Você está logado")

            if c2.button('Registrar'):
                #Go to tela de registro
                switch_page('pages/RegisterUser.py')
if __name__ == "__main__":
    
    # project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # if project_root not in sys.path:
    #     sys.path.insert(0, project_root)
    
    main = Main()
    main.mount()