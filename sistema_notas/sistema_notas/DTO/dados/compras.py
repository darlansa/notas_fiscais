import pandas as pd
from DTO import conexao, consultas
from sqlalchemy.types import DECIMAL, DOUBLE, FLOAT, INTEGER

engine = conexao.get_db_connection()


def remove_desc_itens(df_itens):
    return df_itens.drop("item", axis=1)


def insert_compra(link, data_compra, super_mercado):
    dados = [[link, data_compra, super_mercado]]
    print(dados)
    df_compra = pd.DataFrame(dados, columns=["link", "data_compra", "supermercado"])
    print(df_compra)
    df_compra.to_sql(if_exists="append", index=False, name="compra", con=engine)


def compra(link, data_compra, df_itens, super_mercado):
    insert_compra(link=link, data_compra=data_compra, super_mercado=super_mercado)
    seq = consultas.busca_val_sequence()
    df_itens = remove_desc_itens(df_itens=df_itens)

    insert_itens_compra(df_itens=df_itens, seq=seq)


def insert_itens_compra(df_itens, seq):
    df_itens["id_compra"] = seq[0]
    df_itens = df_itens.rename(
        columns={"codigo": "id_item", "valor": "valor_item", "id_compra": "id_compra"}
    )
    df_itens["valor_item"] = df_itens["valor_item"].str.replace(",", ".")
    df_itens["valor_item"] = df_itens["valor_item"].astype(float)
    df_itens.to_sql(
        if_exists="append",
        index=False,
        name="compra_item",
        con=engine,
        dtype={"id_item": INTEGER, "valor_item": FLOAT, "id_compra": INTEGER},
    )
