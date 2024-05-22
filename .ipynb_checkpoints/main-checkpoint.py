import subprocess
import pwinput
import os
import db_generator as db 
import db_manager as dbm
import bcrypt

#Verifica se o banco de dados já existe
db_exist = os.path.exists("fluxo.db")

#Capa que é exibida no terminal antes de iniciar a aplicação streamlit
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

#Pede para o usuário cadastrar uma senha caso seja o primeiro acesso
def primeiro_acesso():
    calculadora() # chama a capa do terminal
    print("Este é seu primeiro acesso. Crie uma senha. Essa senha não poderá ser alterada futuramente!")
    
    #PWINPUT exibe asteriscos (*) ao digitar a senha no terminal
    senha = pwinput.pwinput(prompt='Criar Senha: ')
    hashed = bcrypt.hashpw(bytes(senha, encoding='utf-8'), bcrypt.gensalt()) #Gera o hash da senha
    dbm.adicionar_senha(hashed.decode('utf-8'))  # Salva a senha como string no banco de dados

    
if not db_exist:
    db.main() #Cria o banco de dados caso ele não exista
    primeiro_acesso() #Chama função de primeiro acesso
    subprocess.run(["streamlit", "run", "Home.py"]) #Inicia aplicação streamlit
else:
    result = dbm.consultar_senha() #Consulta a senha no banco de dados caso não seja o primeiro acesso do usuário
    calculadora()# Chama a capa do terminal
    
    while True: # Continua pedindo senha caso o usuário não digite a senha correta
        senha = pwinput.pwinput(prompt='Insira a senha para acessar o sistema: ')# Pede o input da senha, exibe (*) no lugar da senha
        stored_password = result['password'].encode('utf-8')  # Converte a senha armazenada de volta para bytes
        if bcrypt.checkpw(bytes(senha, encoding='utf-8'), stored_password): # Compara os hashs da senha do input com a do banco de dados
            subprocess.run(["streamlit", "run", "Home.py"]) # Inicia o app streamlit caso as senhas correspondam
        else:
            print("Senha incorreta. Tente novamente")
            
