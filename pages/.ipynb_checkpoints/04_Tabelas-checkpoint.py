import streamlit as st
import pandas as pd
import db_manager as dbm


st.title('Tabelas')
st.markdown('''---''')

dados = dbm.consulta_base() # QUERY com JOIN de todas as tabelas
df = pd.DataFrame(dados) # Cria Dataframe com os dados da query

moviment, contas = st.tabs(['Movimentações', 'Contas']) # Divide em duas guias

with moviment:
    col1, col2 = st.columns(2)
    with col1:
        tipo = st.multiselect(
        "Tipo:", ['Entrada','Saída'],
        default=['Entrada', 'Saída']
        )
        
        start_date, end_date = st.select_slider(
        "Selecione o período:",
        options=pd.Series(df['data'].unique()).sort_values(),
        value=(df['data'].min(), df['data'].max())
        )
    with col2:

        conta = st.multiselect(
            "Conta:",
            df['conta'].unique().tolist(),
            default=df['conta'].unique().tolist()
        )
        
        categoria = st.multiselect(
            "Categoria:",
            df['categoria'].unique().tolist(),
            default=df['categoria'].unique().tolist()
        )
        
    
    df_filtrado = df[(df['conta'].isin(conta)) & (df['tipo'].isin(tipo)) & (df['categoria'].isin(categoria)) & (df['data'] >= start_date) & (df['data'] <= end_date)]
    
    df = df_filtrado[['data', 'tipo', 'categoria', 'conta', 'comentario', 'valor']] # Seleciona as colunas do DataFrame a serem exibidas
    st.dataframe(df, use_container_width=True) # Exibe dataframe
    

with contas:
    dados = dbm.consultar_contas() # Query com a tabela de contas e saldo
    df_conta = pd.DataFrame(dados) # Cria Dataframe
    st.dataframe(df_conta, use_container_width=True) # Exibe Dataframe
    
    

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- SIDEBAR

st.sidebar.title("Totais")

saldo_atual = df_conta['saldo'].sum()
valor_total = df_filtrado['valor'].sum()
media = df_filtrado['valor'].mean()
qt_mov = df_filtrado['valor'].count()

st.sidebar.metric(
    label='TOTAL MOVIMENTADO:',
    value=f'R$ {valor_total}'
)

st.sidebar.metric(
    label='MÉDIA:',
    value=f'R$ {media:.2f}'
)

st.sidebar.metric(
    label='QUANTIDADE MOVIMENTAÇÕES:',
    value=qt_mov
)

st.sidebar.markdown('''---''')
st.sidebar.metric(
    label='SALDO ATUAL:',
    value=f'R$ {saldo_atual}'
)