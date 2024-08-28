import bcrypt
from DTO import conexao
from sqlalchemy.sql.expression import text

engine = conexao.get_db_connection()


def busca_login(username, password):
    resultado = ""
    with engine.connect() as conn:
        query = f"""select senha
                    from usuarios 
                    WHERE 
                    ativo = true
                    and USUARIO = '{username}'"""
        result = conn.execute(text(query))
        resultado = result.one_or_none()

    passwordBytes = password.encode("utf-8")
    return bcrypt.checkpw(passwordBytes, resultado[0].encode())


def busca_super():
    resultado = ""
    lista_super = []
    with engine.connect() as conn:
        query = """select NOME from supermercados"""
        result = conn.execute(text(query))
        resultado = result.all()

    for super in resultado:
        lista_super.append(super[0])
    return lista_super


def busca_item(desc_item):
    resultado = ""
    with engine.connect() as conn:
        query = f"""select * from itens where descricao like '{desc_item}'"""
        result = conn.execute(text(query))
        resultado = result.all()

    return resultado


def busca_val_sequence():
    resultado = ""
    with engine.connect() as conn:
        query = """SELECT last_value FROM compra_id_seq """
        result = conn.execute(text(query))
        resultado = result.one_or_none()

    return resultado


def busca_link_repetido(link):
    resultado = ""
    with engine.connect() as conn:
        query = f"""SELECT 1 FROM compra where link = '{link}' """
        result = conn.execute(text(query))
        resultado = result.all()

    return resultado


def busca_completa():
    resultado = ""
    with engine.connect() as conn:
        query = """select
                c.supermercado as supermercado_descricao,
                c.data_compra,
                ci.id_compra ,
                ci.valor_item ,
                i.descricao as descricao_item,
                s.latitude ,
                s.longitude
            from
                compra c
            join compra_item ci on
                ci.id_compra = id_compra
            join itens i on
                i.id = ci.id_item
            join supermercados s on
                c.supermercado = s.nome"""
        result = conn.execute(text(query))
        resultado = result.all()

    return resultado


def busca_valor_feira():
    resultado = ""
    with engine.connect() as conn:
        query = """select
	c.data_compra ,
	sum(ci.valor_item) as total
from
 compra_item ci
 join compra c on ci.id_compra = c.id 
group by 	c.data_compra """
        result = conn.execute(text(query))
        resultado = result.all()

    return resultado


def busca_valor_item():
    resultado = ""
    with engine.connect() as conn:
        query = """select
	c.data_compra ,
	i.descricao ,
	sum(ci.valor_item) as valor_total
from
 compra_item ci
 join compra c on ci.id_compra = c.id
 join itens i on ci.id_item = i.id 
group by 	c.data_compra,i.descricao
"""
        result = conn.execute(text(query))
        resultado = result.all()

    return resultado
