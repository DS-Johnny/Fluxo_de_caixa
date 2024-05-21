import sqlite3
from sqlite3 import Error

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
        
def id_conta(conta : str):
    database = "fluxo.db"
    conn = create_connection(database)
    conn.row_factory = dict_factory
    
    sql = "SELECT id_conta FROM conta WHERE nome = ?"
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (conta,))
            consulta = cur.fetchone()
            
            return consulta['id_conta']
            
        except Error as e:
            return e

        
def id_categoria(categoria : str):
    database = "fluxo.db"
    conn = create_connection(database)
    conn.row_factory = dict_factory
    
    sql = "SELECT id_categoria FROM categoria WHERE nome = ?"
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (categoria,))
            consulta = cur.fetchone()
            
            return consulta['id_categoria']
            
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

        
def adicionar_conta(nome : str):
    database = "fluxo.db"
    conn = create_connection(database)
    sql = ''' INSERT INTO conta(nome)
              VALUES(?)'''
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (nome,))
            conn.commit()
            return cur.lastrowid
        
        except Error as e:
            return e
        
        
def adicionar_categoria(tipo : str, nome : str):
    database = "fluxo.db"
    conn = create_connection(database)
    sql = ''' INSERT INTO categoria(tipo, nome)
              VALUES(?,?)'''
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (tipo, nome))
            conn.commit()
            return cur.lastrowid
        
        except Error as e:
            return e
        
def adicionar_movimentacao(data, tipo, id_categoria, id_conta, comentario, valor):
    database = "fluxo.db"
    conn = create_connection(database)
    sql = ''' INSERT INTO movimentacoes(data, tipo, id_categoria, id_conta, comentario, valor)
            values(?,?,?,?,?,?)'''
    
    with conn:
        try:
            cur = conn.cursor()
            cur.execute(sql, (data, tipo, id_categoria, id_conta, comentario, valor))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            return e