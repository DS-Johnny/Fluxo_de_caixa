import streamlit as st
import db_manager as dbm
import pandas as pd

#Consulta o banco de dados
transacoes = dbm.consulta_base()

#Cor dos plots gráficos
cor = '#386ee0'

# Função para ser utilizada no lambda com o objetivo de criar uma coluna com os meses nomeados em português
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

if transacoes:
    df = pd.DataFrame(transacoes)
    df['mes'] = df['data'].apply(lambda x: mes(x[5:7])) # Cria uma coluna com o nome dos meses
    
    mes = st.sidebar.selectbox(
    "Selecione o mês:",
    df['mes'].unique(),
    key='mes'
    )
    
    df_mes = df[df['mes'] == mes]
    df = df_mes
    # =-=--=-=-=-=--=-=-=-=-=-=-=-=-=- CORPO DA PÁGINA
    st.title("Dashboard")
    st.markdown('''---''')
    
    #ENTRADA
    df_entrada = df[df['tipo'] == 'Entrada']
    
    with st.container():
        st.markdown("### Entrada")

        st.write("Gráficos")
        # Agrupar os dados pela categoria e somar os valores dos gastos
        entradas_por_categoria = df_entrada.groupby('categoria')['valor'].sum().reset_index()

        # Ordenar os valores para uma visualização melhor
        entradas_por_categoria = entradas_por_categoria.sort_values(by='valor')
        
        # Plota o gráfico
        st.bar_chart(data=entradas_por_categoria, x='valor', y='categoria', color=[cor], width=400, height=300, use_container_width=True)

        # Converter a coluna 'data' para datetime (caso não esteja)
        df_entrada['data'] = pd.to_datetime(df['data'])

        # Agrupar os dados por data e somar os valores dos gastos
        entrada_por_data = df_entrada.groupby('data')['valor'].sum().reset_index()
        
        # Plota o gráfico
        st.line_chart(data=entrada_por_data, x='data', y='valor', color=[cor])

    #SAIDA
    st.markdown('''---''')
    df_saida = df[df['tipo'] == 'Saída']
    with st.container():
        st.markdown("### Saída")

        st.write("Gráficos")
            # Agrupar os dados pela categoria e somar os valores dos gastos
        gastos_por_categoria = df_saida.groupby('categoria')['valor'].sum().reset_index()

        # Ordenar os valores para uma visualização melhor
        gastos_por_categoria = gastos_por_categoria.sort_values(by='valor')

        # Plota o gráfico
        st.bar_chart(data=gastos_por_categoria, x='valor', y='categoria', color=[cor], width=400, height=300, use_container_width=True)
    
        # Converter a coluna 'data' para datetime (caso não esteja)
        df_saida['data'] = pd.to_datetime(df['data'])

        # Agrupar os dados por data e somar os valores dos gastos
        gastos_por_data = df_saida.groupby('data')['valor'].sum().reset_index()

        # Plota o gráfico
        st.line_chart(data=gastos_por_data, x='data', y='valor', color=[cor])
    
    # =-=--=-=-=-=--=-=-=-=-=-=-=-=-=- Barras de Progresso
    st.sidebar.title("Orçamento:")
    
    # Identificar orcamentos
    orcamentos = dbm.consultar_orcamentos() # QUERY tabela orçamentos
    # Se houver registros na tabela de orçamento faz o cálculo e exibe a barra de progresso
    if orcamentos:
        # Fazer o cálculo do progresso para cada despesa
        for i in range(len(orcamentos)):
            categoria = orcamentos[i]['categoria']
            despesa = df[df['categoria'] == categoria]["valor"].sum() # Soma o gasto total por categoria
            limite = orcamentos[i]['limite']
            orcamento = despesa/limite # Calcula a porcentagem do progresso

            #Exibir barra de progresso
            if orcamento > 1.0:
                st.sidebar.progress(1.0, text=categoria) # Se o gasto ultrapassar o orçamento, exibe a barra completa para evitar erro do widget
                st.sidebar.markdown(f'R&#36; {despesa:.2f} de R&#36; {limite:.2f}')
            else:
                st.sidebar.progress(orcamento, text=categoria) # Exibe o progresso de acordo com a porcentagem
                st.sidebar.markdown(f'R&#36; {despesa:.2f} de R&#36; {limite:.2f}')
 
    else:
        st.sidebar.warning("Não foram encontrados orçamentos para despesas.")
    

else:
    st.warning("Não existem registros de transações ainda.")


