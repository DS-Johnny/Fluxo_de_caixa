import streamlit as st

st.sidebar.title("UPDATE")

st.title("UPDATE")
st.markdown("""---""")

with st.container():
    mov, banc, cat = st.tabs(['Inserir Movimentações', 'Inserir Conta', 'Inserir Categoria'])
