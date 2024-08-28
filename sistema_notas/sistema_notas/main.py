import streamlit as st
from DTO import consultas
from pages.cadastros import notas
from pages.indicadores import dashboards

st.set_page_config(
    page_title="Seja muito bem vindo!", page_icon=":bar_chart:", layout="wide"
)


def authenticate_user(username, password):

    if consultas.busca_login(username=username, password=password):
        return 1
    return 0


@st.dialog("Tela de Login", width="small")
def login():
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário/Senha inválidos.")


def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.rerun()


def home_page():

    st.header(
        "Sistema criado para cadastro e consulta dos seus indicadores!", divider="green"
    )


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    st.sidebar.title("Menu")
    menu_option = st.sidebar.selectbox(
        "Escolha a página", ["Home", "Indicadores", "Insere dados", "Logout"]
    )

    if menu_option == "Home":
        home_page()
    elif menu_option == "Indicadores":
        dashboards.app()
    elif menu_option == "Insere dados":
        notas.app()
    elif menu_option == "Logout":
        logout()

else:
    login()
