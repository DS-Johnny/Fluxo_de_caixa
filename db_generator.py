import sqlite3
from sqlite3 import Error

class ConexaoDb:
    """
    Classe para gerenciar a conexão e criação de tabelas em um banco de dados SQLite.
    """
    def __init__(self, database) -> None:
        self.database = database
    
    def generate_conn(self):
        """
        Cria uma conexão com o banco de dados SQLite.

        :return: Objeto de conexão ou None em caso de erro.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.database)
            return conn
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def create_table(self, conn, sql):
        """
        Cria uma tabela no banco de dados.

        :param conn: Objeto de conexão com o banco de dados.
        :param sql: Comando SQL para criar a tabela.
        """
        try:
            cur = conn.cursor()
            cur.execute(sql)
        except Error as e:
            print(e)

def main():
    """
    Função principal que define os comandos SQL para criar tabelas e executa a criação.
    """
    # Inicializa a conexão com o banco de dados
    db = ConexaoDb('database.db')
    # Comandos SQL para criar as tabelas
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
                                conta_debito TEXT NOT NULL,
                                conta_credito TEXT NOT NULL,
                                valor REAL NOT NULL
                                );"""
    
    # Lista de comandos SQL para criar todas as tabelas
    scripts = [sql_create_transacoes_table, sql_create_conta_table, sql_create_categoria, sql_create_password, sql_create_orcamento, sql_create_movimentacao]
    # Gera a conexão com o banco de dados e cria as tabelas
    with db.generate_conn() as conn:
        for script in scripts:
            db.create_table(conn, script)

if __name__ == "__main__":
    main()