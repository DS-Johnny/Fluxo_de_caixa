import subprocess
import pwinput
import os
import db_generator as db
import db_manager as dbm
import bcrypt

db_exist = os.path.exists("fluxo.db")


def primeiro_acesso():
    print("Este é seu primeiro acesso. Crie uma senha. Essa senha não poderá ser alterada futuramente!")
    senha = pwinput.pwinput(prompt='Criar Senha: ')
    hashed = bcrypt.hashpw(senha, bcrypt.gensalt())
    dbm.adicionar_senha(str(hashed))
    


if db_exist == False:
    db.main()
    primeiro_acesso()
    subprocess.run(["streamlit", "run", "Home.py"])
else:
    result = dbm.consultar_senha()
    while True:
        senha = pwinput.pwinput(prompt='Insira a senha para acessar o sistema: ')
        if bcrypt.checkpw(senha['password'], result):
            subprocess.run(["streamlit", "run", "Home.py"])
        else:
            print("Senha incorreta. Tente novamente")
            
    





#Input de senha com * no lugar dos caracteres
#request = pwinput.pwinput(prompt='Insira a senha para acessar o sistema: ')




#if __name__ == "__main__":
#    subprocess.run(["streamlit", "run", "Home.py"])