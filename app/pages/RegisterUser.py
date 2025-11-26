import streamlit as st
from partials.BasePage import BasePage
from app.resources import UserResource

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
        with st.container(border=True):
            self.usuario = st.text_input("Usuário *")
            self.email = st.text_input('Email *')
            st.divider()
            self.senha1 = st.text_input("Senha *", type="password")
            self.senha2 = st.text_input("Confirme a Senha *", type="password")
            st.divider()
            c1, _, _, c2 = st.columns([1, 2, 2, 1])
            disabled =  not self.usuario or not self.email or not self.senha1 or not self.senha2
            disabled_ = self.senha1 != self.senha2
            if c1.button("Registrar", disabled = disabled or disabled_):
                self._register_user()
            if c2.button("Voltar"):
                st.switch_page('main.py')

if __name__ == "__main__":
    registerUser = RegistroUsuario()
    registerUser.draw()