import pandas as pd
from DTO import conexao


def insert_item(itens):
    engine = conexao.get_db_connection()
    itens.to_sql(if_exists="append", index=False, name="itens", con=engine)
