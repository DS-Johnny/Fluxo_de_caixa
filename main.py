import subprocess
import pwinput


password = "johnny*03"


request = pwinput.pwinput(prompt='Insira a senha para acessar o sistema: ')


if request == password:
    print("Senha correta!")
else:
    print("Senha incorreta!")


#if __name__ == "__main__":
#    subprocess.run(["streamlit", "run", "Home.py"])