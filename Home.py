import streamlit as st
import datetime

data_atual = datetime.datetime.today()

def mes(data : str):
    meses = {
        "1" : "Janeiro",
        "2" : "Fevereiro",
        "3" : "Março",
        "4" : "Abril",
        "5" : "Maio",
        "6" : "Junho",
        "7" : "Julho",
        "8" : "Agosto",
        "9" : "Setembro",
        "10" : "Outubro",
        "11" : "Novembro",
        "12" : "Dezembro"}

    return meses[data]


st.title('FLUXO DE CAIXA')

st.write(f'{str(data_atual.day)} de {mes(str(data_atual.month))} de {str(data_atual.year)}')
