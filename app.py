import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Título de la aplicación
st.title("Análisis de comportamiento de los pitchers de mlb en la temporada 2022⚾")
st.author = "Alvaro Goncalves & Yonelvis Gonzalez"
st.markdown("""
Somos un grupo de scouts que busca analizar a los pitchers con mayor efectividad de la temporada 2022 de la MLB. El rendimiento de los jugadores es la base del analisis de cualquier equipo y por lo tanto queremos observar si existen alguna relación entre la efectividad y la participación de un jugador con respecto a su edad. 
""")

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Análisis de comportamiento de Pitchers",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded",
)

#---Carga de datos optimizada---
@st.cache_data # Cache para optimizar la carga de datos
def load_data():
    df = pd.read_csv('pitcheo.csv', encoding='latin-1', sep=';')
    df = load_data().dropna()  # Eliminar filas con valores nulos
    return df
data = load_data()
df = data.copy()
# barra lateral para filtrar por noombre de jugador
# Título principal
st.title("📊 Estadísticas de Jugadores")

# 🎯 Barra lateral de streamlit para seleccionar equipo y columnas estadísticas
st.title("📊 Estadísticas de Jugadores por Equipo")

# 🎯 Selección de equipo
equipos = df_limpio['Team'].unique()
equipo_seleccionado = st.sidebar.selectbox("Selecciona un equipo", equipos)

# 🧩 Selección de columnas estadísticas
columnas_disponibles = df_limpio.columns.drop(['Name', 'Team'])  # Excluye nombre y equipo
columnas_seleccionadas = st.sidebar.multiselect(
    "Selecciona estadísticas a mostrar",
    columnas_disponibles,
    default=columnas_disponibles  # Opcional: mostrar todas por defecto
)
# Indicador 
# Filtrar si lo deseas (ejemplo: pitchers con más de 50 IP)
df_filtrado = df[df['IP'] > 50]

# Calcular métricas
era_promedio = round(df_filtrado['ERA'].mean(), 2)
fip_promedio = round(df_filtrado['FIP'].mean(), 2)
whip_promedio = round(df_filtrado['WHIP'].mean(), 2)

# Mostrar indicadores
st.subheader("Indicadores de Rendimiento")
col1, col2, col3 = st.columns(3)
col1.metric(label="ERA Promedio", value=era_promedio)
col2.metric(label="FIP Promedio", value=fip_promedio)
col3.metric(label="WHIP Promedio", value=whip_promedio)
