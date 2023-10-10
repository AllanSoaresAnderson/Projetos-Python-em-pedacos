import streamlit as st

from config.config import allowed_emails
from services.send_email import SendEmail

import datetime

def sign_in(session_state):
    session_state['login'] = True

def sign_out(session_state):
    session_state['login'] = False
    session_state['validation'] = False
    session_state['start_time'] = None

def time_sign(session_state, date_time, code):
    session_state['start_time'] = date_time
    session_state['code'] = code

def validation(session_state):
    session_state['validation'] = True



def main():
    if st.session_state['login'] == False and st.session_state['validation'] == False:
        st.sidebar.title('Sistema de autenticação')
        with st.sidebar.form(key="login_form"):
            email = st.text_input('Email:')
            if st.form_submit_button('Login'):
                if email.strip() in allowed_emails:
                    try:
                        validation_email = SendEmail(email)
                        time_sign(st.session_state, validation_email.tempo_inicial, validation_email.codigo)
                        validation(st.session_state)
                        validation_email = None
                        st.rerun()
                    except Exception:
                        st.warning(f'Um erro aconteceu no seu acesso')
                else:
                    st.sidebar.error('Acesso Negado')
    
    elif st.session_state['validation'] and st.session_state['login'] == False:
        st.sidebar.title('Código de verificação')
        with st.sidebar.form(key="validation_form"):
            code = st.text_input('_ _ _ _ _ _')
            diferenca_tempo = st.session_state['start_time'] - datetime.datetime.now()
            if st.form_submit_button('Enviar'):
                if diferenca_tempo.total_seconds() / 60 <= 5:
                    print('tempo')
                    if st.session_state['code'] == code:
                        print('code')
                        sign_in(st.session_state)
                        st.rerun()
                else:
                    print('nao loguei')
                    sign_out(st.session_state)

    elif st.session_state['login']:
        st.sidebar.title('Entrou')

        if st.sidebar.button('Sair'):
            sign_out(st.session_state)
            st.rerun()




if __name__ == '__main__':
    if 'login' not in st.session_state:
        st.session_state['login'] = False
        st.session_state['validation'] = False
        st.session_state['start_time'] = None
        st.session_state['code'] = None
    main()

    