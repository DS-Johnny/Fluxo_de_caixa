import streamlit as st
import pandas as pd
import db_manager as dbm

st.sidebar.title('Tabelas')


st.title('Tabelas')
st.markdown('''---''')

dados = dbm.consulta_base()
df = pd.DataFrame(dados)

moviment, contas = st.tabs(['Movimentações', 'Contas'])

with moviment:
    df = df[['data', 'tipo', 'categoria', 'conta', 'comentario', 'valor']]
    st.dataframe(df, use_container_width=True)

with contas:
    dados = dbm.consultar_contas()
    df = pd.DataFrame(dados)
    st.dataframe(df, use_container_width=True)