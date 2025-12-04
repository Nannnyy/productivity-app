from db import DatabaseSession
from models import User
from sqlalchemy import or_, select
from dotenv import load_dotenv
from resources import CookieManager

import hashlib
import traceback
import os
import streamlit as st

class UserResource():

    COOKIE_SALT = "132KFGgffhKMll241jazmxnfrj48868aSDAS"

    def __init__(self):
        self.db = DatabaseSession()
        self.session = self.db.get_session()

    @classmethod
    def create_login_cookie(cls,username:str):
        cookie = f'{username}:{cls.COOKIE_SALT}'
        hashed_cookie = hashlib.sha256(cookie.encode()).hexdigest()
        return hashed_cookie

    @classmethod
    def check_login_cookie(cls) -> bool:
        """
        Retorna True se o cookie de autenticação estiver correto, False caso contrário.
        """
        CManager = CookieManager()
        username = CManager.get_cookie_manager().get("AUTH_USERNAME_COOKIE")
        if not username:
            return False
        hashed_cookie = hashlib.sha256(f'{username}:{cls.COOKIE_SALT}'.encode()).hexdigest()
        cookie = CManager.get_cookie_manager().get('AUTH_COOKIE')
        return hashed_cookie == cookie

    @staticmethod 
    def check_password(plain_password: str, saved_password: str):
        hashed_pass = hashlib.sha256(plain_password.encode()).hexdigest()
        return hashed_pass == saved_password

    @staticmethod
    def get_user_id_by_cookie():
        CManager = CookieManager()
        USERNAME = CManager.get_cookie_manager().get('AUTH_USERNAME_COOKIE')
        db = DatabaseSession()
        session = db.get_session()
        try:
            user_id = session.execute(select(User.id).where(User.username == USERNAME)).scalar()
            return user_id
        except:
            session.rollback()
            traceback.print_exc()
            return None

    @staticmethod
    def logout():
        CManager = CookieManager()
        CManager.get_cookie_manager().delete('AUTH_COOKIE', key='delete-0')
        CManager.get_cookie_manager().delete('AUTH_USERNAME_COOKIE', key='delete-1')

    def get_name_from_cookie(self,return_user=False):
        CManager = CookieManager()
        username = CManager.get_cookie_manager().get('AUTH_USERNAME_COOKIE')
        try:
            user = self.session.execute(select(User).where(User.username == username)).scalar()
            if return_user:
                return user.username, user
            return user.username
        except:
            self.session.rollback()
            traceback.print_exc()
            return None
    
    def login(self, username: str, password: str):
        try:
            statement = select(User).where(User.username == username)
            user = self.session.scalar(statement)
            if not user:
                st.error(f":material/error: Usuário ou senha inválidos.")
                return [False, "Usuário ou senha inválidos."]
            if  self.check_password(password, user.password):
                cookie = self.create_login_cookie(user.username)
                CManager = CookieManager()
                CManager.get_cookie_manager().set('AUTH_COOKIE', cookie, key='set-0')
                CManager.get_cookie_manager().set('AUTH_USERNAME_COOKIE', user.username, key='set-1')
                st.success(f":material/check_circle: Login realizado com sucesso.")
                return [True, user]
            else:
                st.error(f":material/error: Usuário ou senha inválidos.")
                return [False, "Usuário ou senha inválidos."]
        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            st.error(f":material/error: Erro ao realizar login.")
            return [False, e]

    def register(self, username:str, email:str, password:str) -> list:
        try:
            statement = select(User).where(
                or_(
                    User.email == email,
                    User.username == username,
                )
            )
            user_exist = self.session.scalar(statement)
            if user_exist:
                matched = []
                if user_exist.email == email:
                    matched.append("email")
                if user_exist.username == username:
                    matched.append("usuário")

                return [False, "Já existe um usuário com esse(s) dado(s): " + ", ".join(matched)]
            senha_hashed = hashlib.sha256(password.encode()).hexdigest()
            user = User(
                username=username, 
                password=senha_hashed, 
                email=email, 
                is_active=True,
            )

            self.session.add(user)
            self.session.commit()
            return [True, user]
        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            st.error(f":material/error: Erro ao registrar usuário.")
            return [False, e]