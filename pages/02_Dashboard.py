import streamlit as st
import db_manager as dbm
import pandas as pd

transacoes = dbm.consulta_base()

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
    with st.container():
        st.markdown("### Entrada")
        ent_filtros, ent_graficos = st.columns(2)
        with ent_filtros:
            st.write("Filtros")
        with ent_graficos:
            st.write("Gráficos")
    
    #SAIDA
    with st.container():
        st.markdown("### Saída")
        sai_filtros, sai_graficos = st.columns(2)
        with sai_filtros:
            st.write("Filtros")
        with sai_graficos:
            st.write("Gráficos")
    
    
    
    
    
    
    
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
            else:
                st.sidebar.progress(orcamento, text=categoria) # Exibe o progresso de acordo com a porcentagem
    else:
        st.sidebar.warning("Não foram encontrados orçamentos para despesas.")
    
    
    #EXIBE  A TABELA DE TRANSAÇÕES NO FINAL
    st.dataframe(df[['data','tipo','categoria','conta','valor','descricao']], use_container_width=True)

else:
    st.warning("Não existem registros de transações ainda.")


