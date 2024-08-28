import streamlit as st
from DTO import consultas
from DTO.dados import compras, itens_nota
from utils import util


def app():
    st.write("Insira os dados")

    st.title("Cadastro das notas fiscais")

    formulario = st.form(key="Entrada de Dados", clear_on_submit=True)
    supermercados = consultas.busca_super()
    dados = False
    with formulario:
        input_link = st.text_input(
            "Nota Fiscal", placeholder="Insira o link da nota fiscal"
        )
        input_data_compra = st.date_input(
            label="Data Compra", value=None, format="DD/MM/YYYY"
        )
        input_supermercados = st.selectbox(
            label="Super Mercados", options=supermercados
        )

        btn_submit = formulario.form_submit_button("Confirma")

        if btn_submit:
            if not input_link:
                st.error("Informe o link")
            elif not input_data_compra:
                st.error("Informe a data da Compra")
            elif not input_supermercados:
                st.error("Informe o Super Mercado")
            else:
                resultado, status, error = util.valida_url(input_link)
                if status:
                    if consultas.busca_link_repetido(link=input_link):
                        st.error("Nota já cadastrada")
                    else:
                        dados = True
                        st.success("Dados Salvos")
                else:
                    st.error(f"Erro : {error}")
    if dados:
        df = itens_nota.busca_itens(resultado.text)
        itens_nota.itens(df)
        compras.compra(
            df_itens=df,
            link=input_link,
            data_compra=input_data_compra,
            super_mercado=input_supermercados,
        )
