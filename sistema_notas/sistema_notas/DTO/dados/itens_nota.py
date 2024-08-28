import duckdb as db
import pandas as pd
from DTO import consultas
from DTO.dados import insert_dados
from parsel import Selector


def busca_itens(text):
    sel = Selector(text=text)
    codigos = sel.css("span.RCod::text").getall()
    itens = sel.css("span.txtTit::text").getall()
    valor = sel.css("span.valor::text").getall()
    lista_codigos = []
    for codigo in codigos:
        lista_codigos.append(codigo.strip().split()[1])
    lista_completa = []
    for i in range(len(itens)):
        lista_completa.append((lista_codigos[i], itens[i], valor[i]))

    df = pd.DataFrame(lista_completa, columns=["codigo", "item", "valor"])

    return df


def itens(df_itens):
    df_itens = db.sql(
        """select distinct codigo, item, 
                    from df_itens
                    """
    ).df()
    itens = []
    for id, desc in df_itens.values:
        if not consultas.busca_item(desc_item=desc):
            itens.append((id, desc))
    if len(itens) > 0:
        df = pd.DataFrame(itens, columns=["id", "descricao"])
        insert_dados.insert_item(df)
