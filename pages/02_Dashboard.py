import streamlit as st
import db_manager as dbm
import pandas as pd

transacoes = dbm.consulta_base()

if transacoes:
    df = pd.DataFrame(transacoes)
    st.dataframe(df[['data','tipo','categoria','conta','valor','descricao']], use_container_width=True)
    
    # Barras de Progresso
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

else:
    st.warning("Não existem registros de transações ainda.")


