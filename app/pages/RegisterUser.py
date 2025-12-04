import streamlit as st
from partials.BasePage import BasePage
from resources import UserResource

class RegistroUsuario(BasePage):
    def __init__(self):
        super().__init__("Registro de Usuário", '', 'centered', 'collapsed')    
        st.session_state['page'] = 'Registro de Usuário'    
    
    def _register_user(self):
        userResource = UserResource()
        success, message =  userResource.register(
            self.usuario,
            self.email,  self.senha1,
        )
        if success:
            st.success("Usuário registrado com sucesso!")
        else:
            st.error("Erro ao registrar usuário: " + str(message))
    
    def draw(self):
        # CSS para design centralizado (mesmo da tela de login)
        st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
        }
        .main .block-container {
            background-color: #ffffff;
        }
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
        .app-description {
            text-align: center;
            color: #666;
            font-size: 0.85rem;
            margin-top: 1rem;
            font-style: italic;
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
        div[style*="border"] {
            border: 1px solid #333333 !important;
        }
        .stContainer {
            border: 1px solid #333333 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Título centralizado
        st.markdown('<h1 class="login-title">Criar Conta</h1>', unsafe_allow_html=True)
        
        # Container centralizado para o cadastro (mais largo)
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            with st.container(border=True):
                # Subtítulo centralizado
                st.markdown('<h3 class="login-subtitle">Preencha seus dados</h3>', unsafe_allow_html=True)
                
                # Inputs centralizados
                self.usuario = st.text_input(
                    "Usuário", 
                    placeholder="Digite seu usuário",
                    label_visibility="collapsed"
                )
                
                self.email = st.text_input(
                    "Email", 
                    placeholder="Digite seu email",
                    label_visibility="collapsed"
                )
                
                self.senha1 = st.text_input(
                    "Senha", 
                    type="password", 
                    placeholder="Digite sua senha",
                    label_visibility="collapsed"
                )
                
                self.senha2 = st.text_input(
                    "Confirme a Senha", 
                    type="password", 
                    placeholder="Confirme sua senha",
                    label_visibility="collapsed"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Botão Registrar (preto)
                disabled = not self.usuario or not self.email or not self.senha1 or not self.senha2
                disabled_ = self.senha1 != self.senha2
                
                if st.button("Registrar", disabled=disabled or disabled_, key="register_btn", type="primary", use_container_width=True):
                    self._register_user()
                
                # Botão Voltar
                if st.button("Voltar", type="secondary", key="back_btn", use_container_width=True):
                    st.switch_page('main.py')
                
                # Descrição do app
                st.markdown(
                    '<p class="app-description">App de Produtividade • Pomodoro & Tarefas</p>',
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    registerUser = RegistroUsuario()
    registerUser.draw()