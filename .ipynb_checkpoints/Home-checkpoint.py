import streamlit as st

st.title("Fluxo de caixa")


bars = [{
    "categoria" : "Lazer",
    "limite" : 200
},
{
    "categoria" : "Alimentação",
    "limite" : 300
}
]

gasto = 75


for i in range(len(bars)):
    categoria = "Limite " + bars[i]['categoria']
    orcament = gasto/bars[i]['limite']
    st.sidebar.progress(orcament, text=categoria)
    
