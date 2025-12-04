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
            switch_page('pages/Dashboard.py')
            st.success(f"Você está logado")
        
        # CSS para design centralizado
        st.markdown("""
        <style>
        .login-title {
            text-align: center;
            font-size: 2rem;
            font-weight: 300;
            margin-bottom: 2rem;
            color: #1f1f1f;
        }
        .login-subtitle {
            text-align: center;
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
            color: #333;
        }
        .stButton > button {
            width: 100%;
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
        .mini-footer {
            text-align: center;
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid #eee;
        }
        .mini-footer-text {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        .register-button {
            margin-bottom: 1rem;
        }
        .app-description {
            text-align: center;
            color: #666;
            font-size: 0.85rem;
            margin-top: 1rem;
            font-style: italic;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Título centralizado
        st.markdown('<h1 class="login-title">Bem-vindo</h1>', unsafe_allow_html=True)
        
        # Container centralizado para o login
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.container(border=True):
                # Subtítulo centralizado
                st.markdown('<h3 class="login-subtitle">Entrar na sua conta</h3>', unsafe_allow_html=True)
                
                # Inputs centralizados
                usuario = st.text_input(
                    "Usuário", 
                    placeholder="Digite seu usuário",
                    label_visibility="collapsed"
                )
                
                senha = st.text_input(
                    "Senha", 
                    type="password", 
                    placeholder="Digite sua senha",
                    label_visibility="collapsed"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Botão Entrar (preto)
                if st.button('Entrar', disabled=not usuario or not senha, key="login_btn", type="primary", use_container_width=True):
                    response = userResource.login(usuario, senha)
                    if response[0] is True:
                        switch_page('pages/Dashboard.py')   
                        st.success(f"Você está logado")
                
                # Botão cadastre-se próximo ao entrar
                if st.button('Cadastre-se', type="secondary", key="register_btn", use_container_width=True):
                    switch_page('pages/RegisterUser.py')
                
                # Descrição do app
                st.markdown(
                    '<p class="app-description">App de Produtividade • Pomodoro & Tarefas</p>',
                    unsafe_allow_html=True
                )
if __name__ == "__main__":
    
    # project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # if project_root not in sys.path:
    #     sys.path.insert(0, project_root)
    
    main = Main()
    main.mount()