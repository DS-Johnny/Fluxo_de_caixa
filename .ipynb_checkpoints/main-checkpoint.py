import subprocess
import pwinput
import os
import db_generator as db
import db_manager as dbm
import bcrypt

db_exist = os.path.exists("fluxo.db")


def calculadora():
        print("""             _____________________
            |  _________________  |
            | |              /  | |
            | |       /\    /   | |
            | |  /\  /  \  /    | |
            | | /  \/    \/     | |
            | |/             $$ | |
            | |_________________| |
            |  __ __ __ __ __ __  |
            | |__|__|__|__|__|__| |
            | |__|__|__|__|__|__| |
            | |__|__|__|__|__|__| |
            | |__|__|__|__|__|__| |
            | |__|__|__|__|__|__| |
            | |__|__|__|__|__|__| |
            |  ___ ___ ___   ___  |
            | | 7 | 8 | 9 | | + | |
            | |___|___|___| |___| |
            | | 4 | 5 | 6 | | - | |
            | |___|___|___| |___| |
            | | 1 | 2 | 3 | | x | |
            | |___|___|___| |___| |
            | | . | 0 | = | | / | |
            | |___|___|___| |___| |
            |_____________________|
            BEM VINDO AO SISTEMA DE FLUXO DE CAIXA
            """)






def primeiro_acesso():
    calculadora()
    print("Este é seu primeiro acesso. Crie uma senha. Essa senha não poderá ser alterada futuramente!")
    
    
    senha = pwinput.pwinput(prompt='Criar Senha: ')
    hashed = bcrypt.hashpw(bytes(senha, encoding='utf-8'), bcrypt.gensalt())
    dbm.adicionar_senha(hashed.decode('utf-8'))  # Salva a senha como string no banco de dados

if not db_exist:
    db.main()
    primeiro_acesso()
    subprocess.run(["streamlit", "run", "Home.py"])
else:
    result = dbm.consultar_senha()
    calculadora()
    while True:
        senha = pwinput.pwinput(prompt='Insira a senha para acessar o sistema: ')
        stored_password = result['password'].encode('utf-8')  # Converte a senha armazenada de volta para bytes
        if bcrypt.checkpw(bytes(senha, encoding='utf-8'), stored_password):
            subprocess.run(["streamlit", "run", "Home.py"])
        else:
            print("Senha incorreta. Tente novamente")
            
    









#if __name__ == "__main__":
#    subprocess.run(["streamlit", "run", "Home.py"])