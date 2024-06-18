import sqlite3
from sqlite3 import Error


#CRIA A CONEXÃO COM O BANCO DE DADOS
def create_connection(db_file):
    """ Cria conexão com o banco de dados SQLite
        especificado por arquivo_db
        :param arquivo_db: diretório do banco de dados
        :return : Objeto de conexão ou None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        return e


# CRIA UMA FUNÇÃO GERADORA DE TABELAS
def create_table(conn, create_table_sql):

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        return e
    

def main():
    database = "fluxo.db"

    sql_create_transacoes_table = """CREATE TABLE IF NOT EXISTS transacoes(
                                    id_transacao INTEGER primary key autoincrement,
                                    data DATE not null,
                                    tipo TEXT(50) not null,
                                    id_categoria INTEGER not null,
                                    id_conta INTEGER not null,
                                    descricao TEXT(300),
                                    valor REAL not null
                                ); """
    

    sql_create_conta_table = """CREATE TABLE IF NOT EXISTS conta(
                                id_conta INTEGER primary key autoincrement,
                                conta TEXT(100) not null,
                                saldo REAL
                                ); """
    
    sql_create_categoria = """CREATE TABLE IF NOT EXISTS categoria(
                                id_categoria INTEGER primary key autoincrement,
                                tipo TEXT(50) not null,
                                categoria TEXT(50) not null
                                );"""
    
    sql_create_password = """CREATE TABLE IF NOT EXISTS password(
                                password 
                                );"""
    
    sql_create_orcamento = """CREATE TABLE IF NOT EXISTS orcamento(
                                id_orcamento INTEGER PRIMARY KEY autoincrement,
                                id_categoria INTEGER NOT NULL,
                                categoria TEXT(50) NOT NULL,
                                limite REAL NOT NULL
                                );"""
    
    sql_create_movimentacao = """CREATE TABLE IF NOT EXISTS movimentacao(
                                id_movimentacao INTEGER PRIMARY KEY autoincrement,
                                data_movimentacao DATE NOT NULL,
                                conta_debito TEXT NOT NULL
                                conta_credito TEXT NOT NULL,
                                valor REAL NOT NULL
                                );"""
    

    # Cria a conexão com o banco de dados
    conn = create_connection(database)

    # Cria as tabelas
    if conn is not None:
        
        # cria a tabela transacoes
        create_table(conn, sql_create_transacoes_table)

        # cria a tabela conta
        create_table(conn, sql_create_conta_table)
        
        # cria a tabela categoria
        create_table(conn, sql_create_categoria)
        
        # cria a tabela password
        create_table(conn, sql_create_password)
        
        # cria a tabela orcamento
        create_table(conn, sql_create_orcamento)

        # cria a tabela movimentação
        create_table(sql_create_movimentacao)
        
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()