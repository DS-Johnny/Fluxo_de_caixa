from sqlite3 import Error
import db_generator

class GerenciadorDB:
    def __init__(self):
        self.database = db_generator.ConexaoDb('fluxo.db')


dbm = GerenciadorDB()

# Função para que as consultas SQL retornem uma lista de dicionários ao invés de uma lista de tuplas
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

# =-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=- CONSULTAS

# CONSULTAR SENHA
def consultar_senha():
    with dbm.database.generate_conn() as conn:
        conn.row_factory = dict_factory
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM password')
            consulta = cur.fetchone()

            return consulta
        except Error as e:
            print(e)


# CONSULTAR CONTAS
def consultar_contas():
    with dbm.database.generate_conn() as conn:
        conn.row_factory = dict_factory
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM conta')
            consulta = cur.fetchall()

            return consulta
        
        except Error as e:
            print(e)

 
# CONSULTAR CATEGORIAS POR TIPO (ENTRADA,SAÍDA)
def consultar_categorias(tipo :str):
    with dbm.database.generate_conn() as conn:
        conn.row_factory = dict_factory
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM categoria WHERE tipo = ?', [tipo])
            consulta = cur.fetchall()

            return consulta
        
        except Error as e:
            print(e)

# CONSULTAR O ID DE UMA CONTA POR NOME
def id_conta(conta : str):
    with dbm.database.generate_conn() as conn:
        conn.row_factory = dict_factory
        try:
            cur = conn.cursor()
            cur.execute('SELECT id_conta FROM conta WHERE conta = ?', [conta])
            consulta = cur.fetchone()

            return consulta['id_conta']
        
        except Error as e:
            print(e)

# CONSULTAR O SALDO DE UMA CONTA POR ID DA CONTA  
def saldo_conta(id_conta : int):
    with dbm.database.generate_conn() as conn:
        conn.row_factory = dict_factory
        try:
            cur = conn.cursor()
            cur.execute('SELECT saldo FROM conta WHERE id_conta = ?', [id_conta])
            consulta = cur.fetchone()

            return consulta['saldo']
        
        except Error as e:
            print(e)

# CONSULTAR ORÇAMENTOS
def consultar_orcamentos():
    with dbm.database.generate_conn() as conn:
        conn.row_factory = dict_factory
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM orcamento')
            consulta = cur.fetchall()

            return consulta
        
        except Error as e:
            print(e)

# CONSULTA GERAL
def consulta_base():
    with dbm.database.generate_conn() as conn:
        conn.row_factory = dict_factory
        try:
            cur = conn.cursor()
            cur.execute(""" SELECT 
                                *
                            FROM transacoes m LEFT JOIN conta c ON(c.id_conta = m.id_conta)
                            LEFT JOIN categoria c2 ON (c2.id_categoria = m.id_categoria)""")
            consulta = cur.fetchall()
            
            return consulta
            
        except Error as e:
            print(e)

# =-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=- INSERT

# CADASTRAR SENHA
def adicionar_senha(senha : str):
    with dbm.database.generate_conn() as conn:
        try:
            cur = conn.cursor()
            cur.execute(''' INSERT INTO password(password)
              VALUES(?)''', [senha])
            conn.commit()

        except Error as e:
            print(e)

# ADICIONAR CONTA
def adicionar_conta(conta : str, saldo : float):
    with dbm.database.generate_conn() as conn:
        try:
            cur = conn.cursor()
            cur.execute(''' INSERT INTO conta(conta, saldo)
                            VALUES(?,?)''', [conta, saldo])
            conn.commit()

        except Error as e:
            print(e)

# ADICIONAR CATEGORIA 
def adicionar_categoria(tipo : str, categoria : str):
    with dbm.database.generate_conn() as conn:
        try:
            cur = conn.cursor()
            cur.execute(''' INSERT INTO categoria(tipo, categoria)
                            VALUES(?,?)''', [tipo, categoria])
            conn.commit()

        except Error as e:
            print(e)

# Adicionar Transação
def adicionar_transacao(data, tipo, id_categoria, id_conta, descricao, valor):
    with dbm.database.generate_conn() as conn:
        try:
            cur = conn.cursor()
            cur.execute(''' INSERT INTO transacoes(data, tipo, id_categoria, id_conta, descricao, valor)
                            values(?,?,?,?,?,?)''', [data, tipo, id_categoria, id_conta, descricao, valor])
            conn.commit()

        except Error as e:
            print(e)

# ADICIONAR ORCAMENTO
def adicionar_orcamento(id_categoria : int, categoria : str, limite : float):
    with dbm.database.generate_conn() as conn:
        try:
            cur = conn.cursor()
            cur.execute(''' INSERT INTO orcamento(id_categoria, categoria, limite)
              VALUES(?,?,?)''', [id_categoria, categoria, limite])
            conn.commit()

        except Error as e:
            print(e)

# ADICIONAR MOVIMENTAÇÃO
def adicionar_movimentacao(conta_debito, conta_credito, valor):
    with dbm.database.generate_conn() as conn:
        from datetime import datetime
        data_atual = datetime.today()
        data_atual = data_atual.strftime('%Y-%m-%d')

        try:
            cur = conn.cursor()
            cur.execute('''INSERT INTO movimentacao(data_movimentacao, conta_debito, conta_credito, valor)
                            VALUES(?,?,?,?)''', [data_atual, conta_debito, conta_credito, valor])
            conn.commit()

        except Error as e:
            print(e)


# ------------------------------------------- UPDATE

# Atualizar Saldo
def atualizar_saldo(tipo, valor, id_conta):
    saldo = saldo_conta(id_conta)

    if tipo == 'Entrada':
        saldo += valor
    elif tipo == 'Saída':
        saldo -= valor

    with dbm.database.generate_conn() as conn:
        try:
            cur = conn.cursor()
            cur.execute(''' UPDATE conta
                            SET saldo = ?
                            WHERE id_conta = ?''', [saldo, id_conta])
            conn.commit()
            
        except Error as e:
            print(e)

# Movimentação de Saldo
def movimentacao(conta_deb, conta_cred, novo_saldo_deb, novo_saldo_cred):
    with dbm.database.generate_conn() as conn:
        try:
            cur = conn.cursor()
            cur.execute('''UPDATE conta
                            SET saldo = ?
                            WHERE conta = ?''', [novo_saldo_deb, conta_deb])
            conn.commit()

            cur.execute('''UPDATE conta
                            SET saldo = ?
                            WHERE conta = ?''', [novo_saldo_cred, conta_cred])
            conn.commit()

        except Error as e:
            print(e)
