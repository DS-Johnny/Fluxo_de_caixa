import streamlit as st
import db_manager as dbm
import pandas as pd

st.sidebar.title("UPDATE")

st.title("UPDATE")

st.text('''    Antes de registrar uma transação:\n
                1 - Cadastrar um banco e saldo atual\n
                2 - Inserir Categorias de Entrada e Saída\n
                3 - Inserir limites/orçamentos para monitorar seus gastos
''')

st.markdown('''---''')

with st.container():
    mov, banc, cat, orcamento, movimentacao = st.tabs(['Inserir Transação', 'Inserir Conta', 'Inserir Categoria', 'Inserir Orçamento', 'Movimentação'])

    # -=-=-=-=-=-=-=-=-=-=-=-=- INSERIR TRANSAÇÃO
    with mov:
        st.markdown("Transações")

        col1, col2 = st.columns(2) # Divide a sessão de transação em duas colunas
        
        with col1:
            data = st.date_input("Data:", format="DD/MM/YYYY") # Input calendário
            
            contas = dbm.consultar_contas() # Query retorna a tabela de contas + saldo
            
            #VERIFICA a existência de contas no banco de dados
            if contas:
                contas_lista = [i['conta'] for i in contas]
            else:
                contas_lista = []
                st.error("Nenhuma conta encontrada. Adicione uma conta antes de prosseguir.")
            
            # Input dropdown com as contas presentes no banco de dados
            conta = st.selectbox(
                "Conta:",
                contas_lista, key='cont_lista'
            )

            
        with col2:
            # Iput dropdown com as opções Entrada ou Saída
            option = st.selectbox(
                "Tipo:",
                ("Entrada", "Saída"), key='tipo_mov'
            )
                
            categorias = dbm.consultar_categorias(option) # Query que retorna a tabela com as categorias
            
            #VERIFICA a existência das categorias no banco de dados
            if categorias:
                cat_lista = [i['categoria'] for i in categorias]
            else:
                cat_lista = []
                st.error(f"Nenhuma categoria encontrada para {option}. Adicione uma categoria antes de prosseguir.")
            
            #Input dropdown com as categorias presentes no banco de dados
            categoria = st.selectbox(
                "Categoria:",
                cat_lista, key='cat_lista'
            )
        # Caso houver a existência de ambos CONTA e CATEGORIA nos inputs, resgata o id de cada
        if conta and categoria:
            id_conta = dbm.id_conta(conta)
            id_categoria = dbm.id_categoria(categoria)
            
            #Apenas permite colocar o valor da movimentação e comentário se conta e categoria tiverem sido selecionadas
            if id_conta is None or id_categoria is None:
                st.error("Conta ou Categoria não encontrada. Por favor, verifique os dados e tente novamente.")
            else:
                valor = st.number_input("Valor:")
                descricao = st.text_area("Descrição:")
                
                # Se o botão for pressionado
                if st.button("Registrar", key='mov'):
                    st.write("Movimentação registrada")
                    st.write(data, option, id_categoria, id_conta, descricao, valor)
                    dbm.adicionar_transacao(data, option, id_categoria, id_conta, descricao, valor) # INSERE os dados no banco de dados
                    dbm.atualizar_saldo(option, valor, id_conta) # Atualiza o saldo na tabela de contas
                else:
                    st.write("Aperte o botão para registrar")
        else:
            st.warning("Selecione uma conta e uma categoria válidas.")

    # -=-=-=-=-=-=-=-=-=-=-=-=- INSERIR BANCO        
    with banc:
        contas = dbm.consultar_contas() # QUERY que contém as contas já registradas
        # VERIFICA a existência de contas no banco de dados
        if contas:
            contas_lista = [i['conta'] for i in contas] # Caso houver contas, separa apenas os nomes das contas em uma lista
        else:
            contas_lista = []
            st.error("Nenhuma conta encontrada.")
        
        st.markdown("Contas")
        df_contas = pd.DataFrame(contas_lista, columns=['Contas']) # Cria uma tabela com os nomes das contas
        st.dataframe(df_contas, use_container_width=True) # Exibe a tabela
        
        # Input de texto
        text_input = st.text_input(
            "Digite o nome da conta ou banco:",
            "Exemplo: Banco do Brasil",
        )
        # Input numérico
        saldo_inicial = st.number_input("Saldo inicial:")
        
        # Se o botão for pressioando
        if st.button("Registrar", key='conta'):
            if text_input: # Caso contenha informação de texto
                dbm.adicionar_conta(text_input, saldo_inicial) # INSERE a conta e saldo inicial no banco de dados
                st.write("Conta registrada")
            else:
                st.error("O nome da conta não pode estar vazio.")
        else:
            st.write("Aperte o botão para registrar")

    # -=-=-=-=-=-=-=-=-=-=-=-=- INSERIR CATEGORIAS            
    with cat:
        
        st.markdown("Categorias")
        # Dropdown com as opções de ENTRADA e Saída
        option = st.selectbox(
            "Tipo:",
            ("Entrada", "Saída")
        )

        consulta = dbm.consultar_categorias(option) # QUERY com as categorias já registradas
        
        # VERIFICA a existência de categorias no banco de dados
        if consulta:
            df = pd.DataFrame(consulta) # Transforma em tabela
            st.dataframe(df, use_container_width=True) # Exibe a tabela
        else:
            st.error(f"Nenhuma categoria encontrada para {option}.")
        
        # Text Input para nova categoria
        text_input = st.text_input(
            "Digite o nome da categoria:",
            "Exemplo: Aluguel",
        )

        
        # Se o botão for pressionado
        if st.button("Registrar", key='categoria'):
            # Se houver input de texto
            if text_input:
                dbm.adicionar_categoria(option, text_input) # INSERE no banco de dados a nova categoria
                st.write("Categoria registrada")
            else:
                st.error("O nome da categoria não pode estar vazio.")
        else:
            st.write("Aperte o botão para registrar")

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-= INSERIR ORCAMENTO
    
    with orcamento:
        #Exibe tabela com orcamentos já registrado se existir
        orcamentos = dbm.consultar_orcamentos()
        #VERIFICA A EXISTÊNCIA e exibe tabela
        if orcamentos:
            df = pd.DataFrame(orcamentos)
            st.dataframe(df[['categoria','limite']], use_container_width=True)
        else:
            st.error("Nenhum registro encontrado para Orçamento.")
        
        # Resgatar as categorias existentes caso existam, se não existirem, exibir mensagem de erro:
        
        categorias = dbm.consultar_categorias("Saída") # Query que retorna a tabela com as categorias
            
        #VERIFICA a existência das categorias no banco de dados
        if categorias:
            cat_lista = [i['categoria'] for i in categorias] # Coloca em uma lista apenas os nomes das categorias
        else:
            cat_lista = []
            st.error("Nenhuma categoria encontrada para Saída. Adicione uma despesa antes de prosseguir.")
            
        # Exibe opções de despesas em uma dropdown list
        
        #Input dropdown com as categorias presentes no banco de dados
        categoria = st.selectbox(
            "Categoria:",
            cat_lista, key='cat_lista_2'
        )
        
        # Resgatar id da categoria pelo nome
        if categoria:
            id_categoria = dbm.id_categoria(categoria)
            
            # INPUT NUMÉRICO para adicionar um limite de orçamento para essa categoria de despesa
            limite = st.number_input("Limite para essa categoria de despesa:")
            
            # Botão para registrar o novo orçamento
            if st.button("Registrar", key="orcamento"):
                dbm.adicionar_orcamento(id_categoria, categoria, limite)



# ---------------------- Movimentação
with movimentacao:
    dados = dbm.consultar_contas() # Query com a tabela de contas e saldo
    df_conta = pd.DataFrame(dados) # Cria Dataframe
    st.dataframe(df_conta, use_container_width=True) # Exibe Dataframe
    debit, cred = st.columns(2)

    with debit:
        st.write('Escolha a conta de débito:')
        conta_deb = st.selectbox(
                    "Conta:",
                    contas_lista, key='cont_cred')

    with cred:
        st.write('Escolha a conta de crétido:')
        conta_cred = st.selectbox(
                "Conta:",
                contas_lista, 
                key='cont_deb')

    valor_mov = st.number_input("Valor:", key='movimentacao')
    dados = dbm.consultar_contas() # Query com a tabela de contas e saldo
    df_conta = pd.DataFrame(dados) # Cria Dataframe
    

    saldo_conta_deb = df_conta[df_conta['conta'] == conta_deb]['saldo'].iloc[0]
    saldo_conta_cred = df_conta[df_conta['conta'] == conta_cred]['saldo'].iloc[0]

    novo_saldo_deb = saldo_conta_deb - valor_mov
    novo_saldo_cred = saldo_conta_cred + valor_mov

    f'De {saldo_conta_deb = } para {saldo_conta_cred = }'
    
    if st.button("Transferir", key="movimento"):
        #dbm.update_saldo(novo_saldo_deb, conta_deb)
        #dbm.update_saldo(novo_saldo_cred, df_conta)
        dbm.movimentacao(conta_deb, conta_cred, novo_saldo_deb, novo_saldo_cred)


# ----------------- SIDEBAR
try:
    st.sidebar.markdown("## Saldos:")
    for i in range(len(contas)):
        st.sidebar.markdown(f'### {contas[i]['conta']}')
        st.sidebar.metric(
        label=f'Saldo:',
        value=f'R$ {contas[i]['saldo']:.2f}'
    )
except:
    st.sidebar.warning("Não há dados para exibir.")