import streamlit as st
from sklearn import datasets
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

# Título de la aplicación
st.title('CARTAGO')

# Cargar un conjunto de datos de ejemplo (Iris)
repro = pd.read_csv('CSV_Reproductivo.csv')

repro = pd.read_csv("CSV_Reproductivo.csv")
repro['Par'] = pd.to_datetime(repro['Par'], format='%d/%m/%Y', errors='coerce')
repro['an_Par'] = repro['Par'].dt.year.astype('Int64')


# Mostrar los primeros registros del conjunto de datos
st.subheader('ANALISIS REPRODUCTIVO ANUAL')


# Mostrar descripción estadística del conjunto de datos
st.subheader('Descripción estadística del conjunto de datos:')


# Excluir columnas no deseadas
columnas_excluir = ['Finca', 'Vaca', 'Lact', 'E_par']
variables_numericas = repro.select_dtypes(include=['float64', 'int64']).columns
variables_filtradas = [col for col in variables_numericas if col not in columnas_excluir]

# Selector de variable
variable = st.selectbox("Seleccione la variable a graficar", variables_filtradas)
# Mostrar descripción estadística de la variable seleccionada
st.subheader(f'Descripción estadística de la variable: {variable}')
grupoAno = repro.groupby('an_Par')[variable].describe()
st.write(grupoAno)

# Recorremos cada año en el DataFrame
for anio in sorted(repro['an_Par'].unique()):
    st.subheader(f'Gráfico de {variable} - Año {anio}')
    
    # Filtramos por año
    datos_anio = repro[repro['an_Par'] == anio]
    
    # Creamos el gráfico
    fig, ax = plt.subplots()
    ax.hist(datos_anio[variable].dropna(), bins=20, color='skyblue', edgecolor='black')
    ax.set_title(f'{variable} en {anio}')
    ax.set_xlabel(variable)
    ax.set_ylabel('Frecuencia')
    
    st.pyplot(fig)