import altair as alt
import duckdb as db
import pandas as pd
import streamlit as st
from DTO import consultas


def app():

    todos_itens = consultas.busca_completa()
    valor_feira = consultas.busca_valor_feira()
    df_todos_itens = pd.DataFrame(todos_itens)
    df_valor_feira = pd.DataFrame(valor_feira)

    st.dataframe(data=df_todos_itens, hide_index=True)

    supermercados = db.sql(
        """ select latitude, longitude, count(*) as qtd from df_todos_itens group by latitude, longitude  """
    ).df()
    st.map(supermercados)

    filtro_valor_feira = db.sql(
        """ select * 
            from df_valor_feira 
            """
    ).df()

    filtro_qtd_itens = db.sql(
        """ select descricao_item, count(*) as qtd from df_todos_itens group by descricao_item HAVING COUNT(descricao_item) > 3 """
    ).df()

    chart_qtd_itens = (
        alt.Chart(filtro_qtd_itens)
        .mark_bar()
        .encode(
            x=alt.X("descricao_item", sort="-y", title="Itens"),
            y=alt.Y("qtd", title="Quantidade Itens"),
            color="descricao_item:N",
        )
        .properties(height=alt.Step(3))
    )
    st.altair_chart(chart_qtd_itens, use_container_width=True)

    chart_valor_feira = (
        alt.Chart(filtro_valor_feira)
        .mark_line(point=True, interpolate="natural")
        .encode(
            x=alt.X("data_compra", title="Data Compra"),
            y=alt.Y("total:Q", title="Valor Compra"),
        )
    )
    st.altair_chart(chart_valor_feira, use_container_width=True)
