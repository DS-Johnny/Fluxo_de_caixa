import streamlit as st

st.title("Fluxo de caixa")


    
else:
    st.warning("Não existem registros de transações ainda.")


bars = [{
    "categoria" : "Lazer",
    "limite" : 200
},
{
    "categoria" : "Alimentação",
    "limite" : 300
}
]

gasto = 270


for i in range(len(bars)):
    categoria = "Limite " + bars[i]['categoria']
    orcament = gasto/bars[i]['limite']
    
    if orcament > 1.0:
        my_bar = st.sidebar.progress(1.0, text=categoria)
    else:
        my_bar = st.sidebar.progress(orcament, text=categoria)
    
# BARRAS DE PROGRESSO

#CONSULTA 