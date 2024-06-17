import sqlite3
from sqlite3 import Error

# Cria conexão com o banco de dados
def create_connection(arquivo_db):
    """ Cria conexão com o banco de dados SQLite
        especificado por arquivo_db
        :param arquivo_db: diretório do banco de dados
        :return : Objeto de conexão ou None
    """
    conn = None
    try:
        conn = sqlite3.connect(arquivo_db)
        return conn
    except Error as e:
        print(e)
    
    return conn

# Função para que as consultas SQL retornem uma lista de dicionários ao invés de uma lista de tuplas
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


#=-=-=-=-=-=-=-==-=-=-=-=-=--==-- CONSULTAS

#CONSULTAR SENHA
def consultar_senha():
    database = "fluxo.db"
    conn = create_connection(database)
    conn.row_factory = dict_factory
    
    sql = "SELECT * FROM password"
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql)
            consulta = cur.fetchone()
            
            return consulta
            
        except Error as e:
            return e

#Consultar Contas
def consultar_contas():
    database = "fluxo.db"
    conn = create_connection(database)
    conn.row_factory = dict_factory
    
    sql = "SELECT * FROM conta"
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql)
            consulta = cur.fetchall()
            
            return consulta
            
        except Error as e:
            return e
        
#Consultar categorias por tipo ENTRADA OU SAÍDA    
def consultar_categorias(tipo : str):
    database = "fluxo.db"
    conn = create_connection(database)
    conn.row_factory = dict_factory
    
    sql = "SELECT * FROM categoria WHERE tipo = ?"
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (tipo,))
            consulta = cur.fetchall()
            
            return consulta
            
        except Error as e:
            return e

# Consultar o id de uma conta por nome
def id_conta(conta : str):
    database = "fluxo.db"
    conn = create_connection(database)
    conn.row_factory = dict_factory
    
    sql = "SELECT id_conta FROM conta WHERE conta = ?"
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (conta,))
            consulta = cur.fetchone()
            
            return consulta['id_conta']
            
        except Error as e:
            return e

#Consultar o id de uma categoria por nome      
def id_categoria(categoria : str):
    database = "fluxo.db"
    conn = create_connection(database)
    conn.row_factory = dict_factory
    
    sql = "SELECT id_categoria FROM categoria WHERE categoria = ?"
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (categoria,))
            consulta = cur.fetchone()
            
            return consulta['id_categoria']
            
        except Error as e:
            return e

# Consultar o saldo de uma conta por id da conta        
def saldo_conta(id_conta):
    database = "fluxo.db"
    conn = create_connection(database)
    conn.row_factory = dict_factory
    
    sql = "SELECT saldo FROM conta WHERE id_conta = ?"
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (id_conta,))
            consulta = cur.fetchone()
            
            return consulta['saldo']
            
        except Error as e:
            return e


def consultar_orcamentos():
    database = "fluxo.db"
    conn = create_connection(database)
    conn.row_factory = dict_factory
    
    sql = "SELECT * FROM orcamento"
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql)
            consulta = cur.fetchall()
            
            return consulta
            
        except Error as e:
            return e    
    

def consulta_base():
    database = "fluxo.db"
    conn = create_connection(database)
    conn.row_factory = dict_factory
    
    sql = """
        SELECT 
             *
        FROM transacoes m LEFT JOIN conta c ON(c.id_conta = m.id_conta)
        LEFT JOIN categoria c2 ON (c2.id_categoria = m.id_categoria) 
        """
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql)
            consulta = cur.fetchall()
            
            return consulta
            
        except Error as e:
            return e
        
        
#=-=-=-=-=-=-=-==-=-=-=-=-=--==-- INSERT

def adicionar_senha(senha : str):
    database = "fluxo.db"
    conn = create_connection(database)
    sql = ''' INSERT INTO password(password)
              VALUES(?)'''
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (senha,))
            conn.commit()
            return cur.lastrowid
        
        except Error as e:
            return e

        
def adicionar_conta(conta : str, saldo : float):
    database = "fluxo.db"
    conn = create_connection(database)
    sql = ''' INSERT INTO conta(conta, saldo)
              VALUES(?,?)'''
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (conta, saldo))
            conn.commit()
            return cur.lastrowid
        
        except Error as e:
            return e
        
        
def adicionar_categoria(tipo : str, categoria : str):
    database = "fluxo.db"
    conn = create_connection(database)
    sql = ''' INSERT INTO categoria(tipo, categoria)
              VALUES(?,?)'''
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (tipo, categoria))
            conn.commit()
            return cur.lastrowid
        
        except Error as e:
            return e


def adicionar_transacao(data, tipo, id_categoria, id_conta, descricao, valor):
    database = "fluxo.db"
    conn = create_connection(database)
    sql = ''' INSERT INTO transacoes(data, tipo, id_categoria, id_conta, descricao, valor)
            values(?,?,?,?,?,?)'''
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (data, tipo, id_categoria, id_conta, descricao, valor))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            return e
        
def adicionar_orcamento(id_categoria : int, categoria : str, limite : float):
    database = "fluxo.db"
    conn = create_connection(database)
    sql = ''' INSERT INTO orcamento(id_categoria, categoria, limite)
              VALUES(?,?,?)'''
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (id_categoria, categoria, limite))
            conn.commit()
            return cur.lastrowid
        
        except Error as e:
            return e
        
# -------=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=- UPDATE
def atualizar_saldo(tipo, valor, id_conta):
    saldo = saldo_conta(id_conta)
    
    if tipo == 'Entrada':
        saldo += valor
    elif tipo == 'Saída':
        saldo -= valor
    
    database = "fluxo.db"
    conn = create_connection(database)
    sql = ''' UPDATE conta
                SET saldo = ?
                WHERE id_conta = ?'''
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (saldo, id_conta))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            return e

    
def movimentacao(conta_deb, conta_cred, novo_saldo_deb, novo_saldo_cred):
    database = "fluxo.db"
    conn = create_connection(database)
    sql = '''UPDATE conta
                SET saldo = ?
                WHERE conta = ?'''
    
    with conn:
        try:
            cur = conn.cursor()
            
            cur.execute(sql, (novo_saldo_deb, conta_deb))
            conn.commit()

            cur.execute(sql, (novo_saldo_cred, conta_cred))
            conn.commit()

            return cur.lastrowid
        except Error as e:
            return e
        
def update_saldo(conta, novo_saldo):
    database = "fluxo.db"
    conn = create_connection(database)
    sql = '''UPDATE conta
                SET saldo = ?
                WHERE conta = ?'''
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (novo_saldo, conta))
            conn.commit()

            return cur.lastrowid
        except Error as e:
            return e
