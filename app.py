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
    df = pd.read_csv('datap.csv', sep=';', encoding='latin-1')
    return df
    df = load_data().dropna()  # Eliminar filas con valores nulos
    return df
data = load_data()
df = data.copy()

print(len(df.columns))
df.columns.tolist()  
 
# Limpieza de datos
# Verificamos si hay valores nulos
st.write(df.isnull().sum())
# Eliminamos filas con valores nulos
df.dropna(inplace=True)
st.write(df.isnull().sum())
st.write(df.shape)
# Reiniciamos el índice después de eliminar filas
df.reset_index(drop=True, inplace=True)
st.write(df.shape)
st.write(df.head())

# Seleccionar solo las columnas que necesitas
columnas_necesarias = ['Name', 'Tm', 'IP', 'ERA', 'WHIP', 'Age']
df_filtrado = df[columnas_necesarias]

# Mostrar las primeras filas para verificar
print(df_filtrado.head())

#Filtro de rango de edad con innings lanzados mayor a 50
df_limpio = df_filtrado[
    (df_filtrado['Age'] >= 20) &
    (df_filtrado['Age'] <= 50) &
    (df_filtrado['IP'] > 50)
]
df.reset_index(drop=True, inplace=True)
df_limpio

df['Categoria'] = df['Age'].apply(lambda x: 'Veterano' if x > 30 else 'Joven')
df.to_csv('2022 MLB Player Stats - Pitching.csv', index=False)
df['Categoria']
# resumen de cuantos pitchers hay en cada categoria
(df['Categoria'].value_counts())


#Barra lateral de streamlit para seleccionar equipo y columnas estadísticas
st.title("📊 Estadísticas de Jugadores por Equipo")

# 🎯 Selección de equipo
equipos = df_limpio['Tm'].unique()
equipo_seleccionado = st.sidebar.selectbox("Selecciona un equipo", equipos)

# 🧩 Selección de columnas estadísticas
columnas_disponibles = df_limpio.columns.drop(['Name', 'Tm'])  # Excluye nombre y equipo
columnas_seleccionadas = st.sidebar.multiselect(
    "Selecciona estadísticas a mostrar",
    columnas_disponibles,
    default=columnas_disponibles  # Opcional: mostrar todas por defecto
)

# 📌 Filtrar DataFrame por equipo
df_equipo = df_limpio[df_limpio['Tm'] == equipo_seleccionado][['Name'] + columnas_seleccionadas]

# Mostrar resultados
st.subheader(f"Jugadores del equipo {equipo_seleccionado}")
st.dataframe(df_equipo.reset_index(drop=True))

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

markdown = """Graficos por objetivos:
-Determinar si existe una correlación estadísticamente significativa entre participación (medida en IP) y la edad de los pitchers con mayor participación (con un IP > 50) en la temporada 2022 de la MLB.
-Identificar y comparar las métricas de efectividad (ERA y WHIP) y edad del grupo de pitchers con mayor volumen de IP frente al promedio de la liga en 2022.
-Evaluar la relación entre la participación (IP) y la efectividad independiente en el “fildeo” (FIP) para garantizar un análisis completo del rendimiento individual de los pitchers con mayor participación.
-Evaluar la relación de efectividad (ERA) con la métrica de durabilidad/participación (IP) para identificar la eficiencia.
-Clasificar el top 10 de los pitchers con mayor participación en la MLB 2022, ordenándolos según su Whip.
-Clasificar el top 10 de los pitchers con mayor participación en la MLB 2022, ordenándolos según su ERA.
"""
st.markdown(markdown)
st.title("📈 Análisis Gráfico de Pitchers de la MLB 2022"
         )
#Grafico objetivo: Relacion Edad vs Innings Pitched (IP)
df_fig1 = df[(df['Age'] > 20) & (df['IP'] > 50)]

# Crear gráfico de dispersión
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_fig1, x='Age', y='IP', color='blue', s=100)

# Títulos y etiquetas
plt.title('Relación entre Edad y Innings Pitched (IP)')
plt.xlabel('Edad')
plt.ylabel('Innings Pitched (IP)')

# Estética
plt.grid(True)
plt.xlim(20, 42)

# Mostrar
plt.show()
st.pyplot(plt)

#Grafico objetivo: Relacion Innings Pitched (IP) vs Edad con linea de regresion
df_filtrado = df[df['IP'] > 50]

# Crear gráfico de dispersión con línea de regresión
plt.figure(figsize=(10, 6))
sns.regplot(data=df_filtrado, x='IP', y='Age', scatter_kws={'s': 60}, line_kws={'color': 'red'})

# Títulos y etiquetas
plt.title('Relación entre IP y Edad en Pitchers MLB 2022 (IP > 50)')
plt.xlabel('Entradas Lanzadas (IP)')
plt.ylabel('Edad')
plt.grid(True)
plt.tight_layout()
plt.show()
