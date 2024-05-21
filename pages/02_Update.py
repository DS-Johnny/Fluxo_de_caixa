import streamlit as st
import db_manager as dbm
import pandas as pd

st.sidebar.title("UPDATE")

st.title("UPDATE")
st.markdown("""---""")

with st.container():
    mov, banc, cat = st.tabs(['Inserir Movimentação', 'Inserir Conta', 'Inserir Categoria'])
    
    
    
    
    
# -=-=-=-=-=-=-=-=-=-=-=-=- INSERIR MOVIMENTAÇÃO
    with mov:
        st.markdown("Movimentações")
        
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input("Data:", format="DD/MM/YYYY")
            contas = dbm.consultar_contas()
            contas_lista = []
            for i in contas:
                contas_lista.append(i['nome'])
            conta = st.selectbox(
            "Conta:",
            contas_lista, key='cont_lista'
            )
        
        with col2:
            
            option = st.selectbox(
            "Tipo:",
            ("Entrada", "Saída"), key='tipo_mov')
        
            categorias = dbm.consultar_categorias(option)
            cat_lista = []
            for i in categorias:
                cat_lista.append(i['nome'])

            categoria = st.selectbox(
            "Categoria:",
            cat_lista, key='cat_lista'
            )
        
        id_conta = dbm.id_conta(conta)
        id_categoria = dbm.id_categoria(categoria)
        
        valor = st.number_input("Valor:")
        comentario = st.text_area("Comentário:")
        
        
        if st.button("Adicionar", key='mov'):
            st.write("Movimentação registrada")
            st.write(data, option, id_categoria, id_conta, comentario, valor)
            dbm.adicionar_movimentacao(data, option, id_categoria, id_conta, comentario, valor)
        else:
            st.write("Aperte o botão para registrar")
            
        
            
        
        
        
#-=-=-=-=-=-=-=-=-=-=-=-=-=- INSERIR BANCO        
    with banc:
        contas = dbm.consultar_contas()
        contas_lista = []
        for i in contas:
            contas_lista.append(i['nome'])
        
        st.markdown("Contas")
        df = pd.DataFrame(contas_lista, columns=['Contas'])
        st.dataframe(df, use_container_width=True)

        
        
        text_input = st.text_input(
        "Digite o nome da conta ou banco:",
        "Exemplo: Banco do Brasil",
    )
        if st.button("Adicionar", key='conta'):
            dbm.adicionar_conta(text_input)
            st.write("Conta registrada")
        else:
            st.write("Aperte o botão para registrar")

            
            
            
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- INSERIR CATEGORIAS            
    with cat:
        st.markdown("Categorias")
        option = st.selectbox(
        "Tipo:",
        ("Entrada", "Saída"))
        
        consulta = dbm.consultar_categorias(option)
        df = pd.DataFrame(consulta)
        st.dataframe(df, use_container_width=True)
        
        #st.write(consulta)
        
        text_input = st.text_input(
        "Digite o nome da categoria:",
        "Exemplo: Aluguel",
    )
        
        if st.button("Adicionar", key='categoria'):
            dbm.adicionar_categoria(option, text_input)
            st.write("Categoria registrada")
        else:
            st.write("Aperte o botão para registrar")
