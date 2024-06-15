import streamlit as st
import datetime
import pandas as pd
import db_manager as dbm


data_atual = datetime.datetime.today() # Verifica a data atual

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


st.title('FLUXO DE CAIXA')

# Exibe a data atual formatada em Portugês
mes_atual = str(data_atual.month)
mes_atual = [mes_atual if len(mes_atual) == 2 else "0"+mes_atual]
mes_atual = mes(mes_atual[0])
st.write(f'{str(data_atual.day)} de {mes_atual} de {str(data_atual.year)}')


# -------------------- BANCO DE DADOS 

# Contas
contas = dbm.consultar_contas() # Query com a tabela de contas e saldo
df_conta = pd.DataFrame(contas) # Cria Dataframe

# Transacoes
transacoes = dbm.consulta_base() # QUERY com JOIN de todas as tabelas
df = pd.DataFrame(transacoes) # Cria Dataframe com os dados da query
df['mes'] = df['data'].apply(lambda x: mes(x[5:7]))
df = df[['data', 'tipo', 'categoria', 'valor', 'mes']]


# Lista de entradas recebidas
df_entradas =  df[(df['tipo'] == 'Entrada') & (df['mes'] == mes_atual)]



# Gastos por categoria
df_gastos = df[(df['tipo'] == 'Saída') & (df['mes'] == mes_atual)]
df_gastos = df_gastos.groupby('categoria', as_index=False).sum()

# Orcamentos
orcamentos = dbm.consultar_orcamentos()
df_orcamentos = pd.DataFrame(orcamentos)
total_orcamento = df_orcamentos['limite'].sum()


# -------------------- TOTAIS
col1, col2, col3 = st.columns(3)

# SALDO ATUAL
with col1:
    
    saldo_atual = df_conta['saldo'].sum()
    st.metric(
        label='SALDO ATUAL:',
        value=f'R$ {saldo_atual:.2f}'
    )   

# TOTAL ENTRADAS
with col2:
    
    entrada_total = df_entradas['valor'].sum()
    st.metric(
        label = 'Total Entradas',
        value = f'R$ {entrada_total:.2f}'
    )

# TOTAL SAÍDAS
with col3:
    
    gastos = df_gastos['valor'].sum()
    st.metric(
        label = 'Gasto total',
        value = f'R$ {gastos:.2f}'
    )


    
st.markdown('''---''')
# ------------------------- Barras de progresso

col4, col5 = st.columns(2)

with col4:
    st.write('Barra de progresso: Gastos X total entradas')
    progressao_gasto = gastos / entrada_total
    st.write(f'{progressao_gasto}%')
    #Exibir barra de progresso
    if progressao_gasto > 1.0:
        st.progress(1.0, text='Gastos x Total Entradas') # Se o gasto ultrapassar o orçamento, exibe a barra completa para evitar erro do widget
        st.markdown(f'Neste mês você gastou R&#36; {gastos:.2f} e recebeu R&#36; {entrada_total:.2f}')
    else:
        st.progress(progressao_gasto, text='Gastos x Total Entradas') # Exibe o progresso de acordo com a porcentagem
        st.markdown(f'Neste mês você gastou R&#36; {gastos:.2f} e recebeu R&#36; {entrada_total:.2f}')
 

with col5:
    st.write('Barra de progresso: Gastos X Soma Orçamentos')
    progressao_orcamento = gastos / total_orcamento
    #Exibir barra de progresso
    if progressao_orcamento > 1.0:
        st.progress(1.0, text='Gastos x Orçamento') # Se o gasto ultrapassar o orçamento, exibe a barra completa para evitar erro do widget
        st.markdown(f'Neste mês você gastou R&#36; {gastos:.2f} e recebeu R&#36; {total_orcamento:.2f}')
    else:
        st.progress(progressao_orcamento, text='Gastos x Orçamento') # Exibe o progresso de acordo com a porcentagem
        st.markdown(f'Neste mês você gastou R&#36; {gastos:.2f} e o limite estipulado é R&#36; {total_orcamento:.2f}')

st.markdown('''---''')
# --------------------------- Tabelas

col6, col7, col8 = st.columns(3)

with col6:
    st.write('Lista de Entradas.')
    st.dataframe(df_entradas[['data', 'valor']]) 

with col7:
    st.write('Gastos por Categoria')
    st.dataframe(df_gastos[['categoria', 'valor']])

with col8:
    st.write('Saldo por Conta')
    st.dataframe(df_conta[['conta', 'saldo']], use_container_width=True) # Exibe Dataframe