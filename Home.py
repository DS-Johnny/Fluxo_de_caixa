import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Supondo que df já foi criado e contém os dados com colunas 'categoria' e 'valor'
# Para fins de exemplo, vamos criar um DataFrame de exemplo:
data = {
    'categoria': ['Alimentação', 'Transporte', 'Saúde', 'Educação', 'Lazer', 'Outros'],
    'valor': [250, 120, 300, 200, 150, 100]
}
df = pd.DataFrame(data)

# Agrupar os dados pela categoria e somar os valores dos gastos
gastos_por_categoria = df.groupby('categoria')['valor'].sum().reset_index()

# Ordenar os valores para uma visualização melhor
gastos_por_categoria = gastos_por_categoria.sort_values(by='valor')

# Plotar o gráfico de barras horizontais usando Plotly Express
fig = px.bar(gastos_por_categoria, x='valor', y='categoria', orientation='h', 
             labels={'valor': 'Total de Gastos', 'categoria': 'Categoria'},
             title='Gastos por Categoria')

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig)


st.markdown('''___''')

data = {
    'data': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'valor': np.random.randint(100, 500, size=100)
}
df = pd.DataFrame(data)

# Converter a coluna 'data' para datetime (caso não esteja)
df['data'] = pd.to_datetime(df['data'])

# Agrupar os dados por data e somar os valores dos gastos
gastos_por_data = df.groupby('data')['valor'].sum().reset_index()

# Plotar o gráfico de linhas usando Plotly Express
fig = px.line(gastos_por_data, x='data', y='valor', 
              labels={'data': 'Data', 'valor': 'Total de Gastos'},
              title='Progressão dos Gastos ao Longo do Tempo')

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig)