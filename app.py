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


