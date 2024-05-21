import streamlit as st
import db_manager as dbm
import pandas as pd

st.sidebar.title("UPDATE")

st.title("UPDATE")
st.markdown('''---''')

with st.container():
    mov, banc, cat = st.tabs(['Inserir Movimentação', 'Inserir Conta', 'Inserir Categoria'])

    # -=-=-=-=-=-=-=-=-=-=-=-=- INSERIR MOVIMENTAÇÃO
    with mov:
        st.markdown("Movimentações")

        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input("Data:", format="DD/MM/YYYY")
            
            contas = dbm.consultar_contas()
            if contas:
                contas_lista = [i['conta'] for i in contas]
            else:
                contas_lista = []
                st.error("Nenhuma conta encontrada. Adicione uma conta antes de prosseguir.")
            
            conta = st.selectbox(
                "Conta:",
                contas_lista, key='cont_lista'
            )

        with col2:
            option = st.selectbox(
                "Tipo:",
                ("Entrada", "Saída"), key='tipo_mov'
            )

            categorias = dbm.consultar_categorias(option)
            if categorias:
                cat_lista = [i['categoria'] for i in categorias]
            else:
                cat_lista = []
                st.error(f"Nenhuma categoria encontrada para {option}. Adicione uma categoria antes de prosseguir.")
            
            categoria = st.selectbox(
                "Categoria:",
                cat_lista, key='cat_lista'
            )

        if conta and categoria:
            id_conta = dbm.id_conta(conta)
            id_categoria = dbm.id_categoria(categoria)
            
            if id_conta is None or id_categoria is None:
                st.error("Conta ou Categoria não encontrada. Por favor, verifique os dados e tente novamente.")
            else:
                valor = st.number_input("Valor:")
                comentario = st.text_area("Comentário:")

                if st.button("Adicionar", key='mov'):
                    st.write("Movimentação registrada")
                    st.write(data, option, id_categoria, id_conta, comentario, valor)
                    dbm.adicionar_movimentacao(data, option, id_categoria, id_conta, comentario, valor)
                else:
                    st.write("Aperte o botão para registrar")
        else:
            st.warning("Selecione uma conta e uma categoria válidas.")

    # -=-=-=-=-=-=-=-=-=-=-=-=- INSERIR BANCO        
    with banc:
        contas = dbm.consultar_contas()
        if contas:
            contas_lista = [i['conta'] for i in contas]
        else:
            contas_lista = []
            st.error("Nenhuma conta encontrada.")

        st.markdown("Contas")
        df = pd.DataFrame(contas_lista, columns=['Contas'])
        st.dataframe(df, use_container_width=True)

        text_input = st.text_input(
            "Digite o nome da conta ou banco:",
            "Exemplo: Banco do Brasil",
        )
        if st.button("Adicionar", key='conta'):
            if text_input:
                dbm.adicionar_conta(text_input)
                st.write("Conta registrada")
            else:
                st.error("O nome da conta não pode estar vazio.")
        else:
            st.write("Aperte o botão para registrar")

    # -=-=-=-=-=-=-=-=-=-=-=-=- INSERIR CATEGORIAS            
    with cat:
        st.markdown("Categorias")
        option = st.selectbox(
            "Tipo:",
            ("Entrada", "Saída")
        )

        consulta = dbm.consultar_categorias(option)
        if consulta:
            df = pd.DataFrame(consulta)
            st.dataframe(df, use_container_width=True)
        else:
            st.error(f"Nenhuma categoria encontrada para {option}.")

        text_input = st.text_input(
            "Digite o nome da categoria:",
            "Exemplo: Aluguel",
        )

        if st.button("Adicionar", key='categoria'):
            if text_input:
                dbm.adicionar_categoria(option, text_input)
                st.write("Categoria registrada")
            else:
                st.error("O nome da categoria não pode estar vazio.")
        else:
            st.write("Aperte o botão para registrar")










