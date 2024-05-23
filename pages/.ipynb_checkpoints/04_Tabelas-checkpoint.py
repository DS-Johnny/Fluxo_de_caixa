import streamlit as st
import pandas as pd
import db_manager as dbm


st.title('Tabelas')
st.markdown('''---''')

dados = dbm.consulta_base() # QUERY com JOIN de todas as tabelas
df = pd.DataFrame(dados) # Cria Dataframe com os dados da query

def mes(data : str):
    meses = {
        "01" : "Janeiro",
        "02" : "Fevereiro",
        "03" : "Março",
        "04" : "Abril",
        "05" : "Maio",
        "06" : "Junho",
        "07" : "Julho",
        "08" : "Agosto",
        "09" : "Setembro",
        "10" : "Outubro",
        "11" : "Novembro",
        "12" : "Dezembro"}
    
    return meses[data]

if dados:
    df['mes'] = df['data'].apply(lambda x: mes(x[5:7])) # Cria uma coluna com o nome dos meses
    mes = st.sidebar.multiselect(
    "Mês:",
    df['mes'].unique(),
    default=df['mes'].unique()
    )
    df_mes = df[df['mes'].isin(mes)]
    df = df_mes





trans, contas = st.tabs(['Transações', 'Contas']) # Divide em duas guias

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=  GUIA DE TRANSAÇÕES
with trans: 
    
    col1, col2 = st.columns(2) # DUAS COLUNAS PARA OS FILTROS
    
    with col1:
        # FILTRO DO TIPO
        tipo = st.multiselect(
        "Tipo:", ['Entrada','Saída'],
        default=['Entrada', 'Saída']
        )
        
        #FILTRO DE DATA, SELECIONA UM PERÍODO E RETORNA DOIS VALORES, UMA VARIÁVEL DA DATA DE INÍCIO E OUTRA DE FIM
        start_date, end_date = st.select_slider(
        "Selecione o período:",
        options=pd.Series(df['data'].unique()).sort_values(),
        value=(df['data'].min(), df['data'].max())
        )
    with col2:
        
        # FILTRO DE CONTA
        conta = st.multiselect(
            "Conta:",
            df['conta'].unique().tolist(),
            default=df['conta'].unique().tolist()
        )
        
        # FILTRO DE CATEGORIA
        categoria = st.multiselect(
            "Categoria:",
            df['categoria'].unique().tolist(),
            default=df['categoria'].unique().tolist()
        )
        
    #APLICA TODOS OS FILTROS EM UM NOVO DATAFRAME
    df_filtrado = df[(df['conta'].isin(conta)) & (df['tipo'].isin(tipo)) & (df['categoria'].isin(categoria)) & (df['data'] >= start_date) & (df['data'] <= end_date)]
    
    #SELECIONA E EXIBE APENAS AS COLUNAS NECESSÁRIAS
    df = df_filtrado[['data', 'tipo', 'categoria', 'conta', 'descricao', 'valor']] # Seleciona as colunas do DataFrame a serem exibidas
    st.dataframe(df, use_container_width=True) # Exibe dataframe
    
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-== GUIA DE CONTAS
with contas:
    dados = dbm.consultar_contas() # Query com a tabela de contas e saldo
    df_conta = pd.DataFrame(dados) # Cria Dataframe
    st.dataframe(df_conta, use_container_width=True) # Exibe Dataframe
    
    

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- SIDEBAR

st.sidebar.title("Totais")

# MÉTRICAS Estatísticas
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
    label='QUANTIDADE DE TRANSAÇÕES:',
    value=qt_mov
)

st.sidebar.markdown('''---''')
st.sidebar.metric(
    label='SALDO ATUAL:',
    value=f'R$ {saldo_atual}'
)
