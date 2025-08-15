import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style("whitegrid")

# Título de la aplicación
st.title('CARTAGO')

# Cargar el archivo CSV (debe estar en el mismo repositorio en Streamlit Cloud)
try:
    repro = pd.read_csv('CSV_Reproductivo.csv')
except FileNotFoundError:
    st.error("El archivo 'CSV_Reproductivo.csv' no fue encontrado. Asegúrate de subirlo a tu repositorio en Streamlit Cloud.")
    st.stop()


# Mostrar encabezado y descripción
st.subheader('ANALISIS REPRODUCTIVO ANUAL')

# Filtrar columnas
columnas_excluir = ['Finca', 'Vaca', 'Lact', 'E_par', 'T_par', 'Natimuertos', 'Concep', '#Celos',
                    '#Serv', 'IEP_esp', 'Unnamed:']
columnas_numericas = repro.select_dtypes(include='number').columns.tolist()
variables_filtradas = [col for col in columnas_numericas if col not in columnas_excluir]

# Evitar errores si no hay variables disponibles
if not variables_filtradas:
    st.warning("No hay variables numéricas disponibles para graficar.")
    st.stop()

# Selector de variable
variable = st.selectbox("Seleccione la variable a graficar", variables_filtradas)

# Descripción estadística de la variable por año
st.subheader(f'Descripción estadística de la variable: {variable}')

def estadisticas_por_ano(df, grupo_col, valor_col):
    return df.groupby(grupo_col)[valor_col].agg(
        count='count',
        mean='mean',
        std='std',
        min='min',
        q1=lambda x: np.percentile(x.dropna(), 25),
        median='median',
        q3=lambda x: np.percentile(x.dropna(), 75),
        max='max'
    ).reset_index()

repro['an_par'] = pd.to_numeric(repro['an_par'], errors='coerce').astype('Int64')

grupoAno = estadisticas_por_ano(repro, 'an_par', variable)
st.write(grupoAno)

anios_disponibles = sorted(repro['an_par'].dropna().unique())
if not anios_disponibles:
    st.warning("No hay años disponibles para graficar.")
    st.stop()

# Gráfico por año
for anio in sorted(repro['an_par'].dropna().unique()):
    st.subheader(f'Gráfico de {variable} - Año {anio}')
    datos_anio = repro[repro['an_par'] == anio]
    
    if datos_anio[variable].dropna().empty:
        st.write("No hay datos disponibles para este año.")
        continue

    fig, ax = plt.subplots()
    ax.hist(datos_anio[variable].dropna(), bins=20, color='skyblue', edgecolor='black')
    ax.set_title(f'{variable} en {anio}')
    ax.set_xlabel(variable)
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)