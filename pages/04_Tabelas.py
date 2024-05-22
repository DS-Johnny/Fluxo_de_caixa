import streamlit as st
import pandas as pd
import db_manager as dbm

st.sidebar.title('Tabelas')


st.title('Tabelas')
st.markdown('''---''')

dados = dbm.consulta_base() # QUERY com JOIN de todas as tabelas
df = pd.DataFrame(dados) # Cria Dataframe com os dados da query

moviment, contas = st.tabs(['Movimentações', 'Contas']) # Divide em duas guias

with moviment:
    df = df[['data', 'tipo', 'categoria', 'conta', 'comentario', 'valor']] # Seleciona as colunas do DataFrame a serem exibidas
    st.dataframe(df, use_container_width=True) # Exibe dataframe

with contas:
    dados = dbm.consultar_contas() # Query com a tabela de contas e saldo
    df = pd.DataFrame(dados) # Cria Dataframe
    st.dataframe(df, use_container_width=True) # Exibe Dataframe