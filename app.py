import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Título de la aplicación
st.title("Análisis de comportamiento de los pitchers de mlb en la temporada 2022 ⚾")
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
st.write(df.head())

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
st.write(df_filtrado.shape)

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

# Clasificación de pitchers por edad

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
st.write(f"Has seleccionado el equipo: {equipo_seleccionado}")
st.write(f"Has seleccionado las estadísticas: {', '.join(columnas_seleccionadas)}")
st.write("---") 

# 📌 Filtrar DataFrame por equipo
df_equipo = df_limpio[df_limpio['Tm'] == equipo_seleccionado][['Name'] + columnas_seleccionadas]

# Mostrar resultados
st.subheader(f"Jugadores del equipo {equipo_seleccionado}")
st.dataframe(df_equipo.reset_index(drop=True))

# Indicador 
# Filtrar si lo deseas (ejemplo: pitchers con más de 50 IP)
df_filtrado = df[df['IP'] > 50]
st.write(f"Total de pitchers con más de 50 IP: {len(df_filtrado)}")

# Calcular métricas
era_promedio = round(df_filtrado['ERA'].mean(), 2)
fip_promedio = round(df_filtrado['FIP'].mean(), 2)
whip_promedio = round(df_filtrado['WHIP'].mean(), 2)
st.write(f"ERA Promedio: {era_promedio}")
st.write(f"FIP Promedio: {fip_promedio}")   
st.write(f"WHIP Promedio: {whip_promedio}") 

# Mostrar indicadores
st.subheader("Indicadores de Rendimiento")
col1, col2, col3 = st.columns(3)
col1.metric(label="ERA Promedio", value=era_promedio)
col2.metric(label="FIP Promedio", value=fip_promedio)
col3.metric(label="WHIP Promedio", value=whip_promedio)
st.write("---")

# Gráficos de análisis

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
#Grafico: Relacion Edad vs Innings Pitched (IP)
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


#Grafico: Relacion Innings Pitched (IP) vs Edad con linea de regresion
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
st.pyplot(plt)
st.markdown("**Conclusión Gráfico 2:** El gráfico de dispersión con línea de regresión muestra una ligera tendencia positiva entre las entradas lanzadas (IP) y la edad de los pitchers en la MLB 2022. Esto sugiere que, en general, los pitchers más experimentados tienden a lanzar más entradas, aunque la correlación no es muy fuerte.")

#Grafico: Rango de mejores pitchers por edad según su whip
df_fig2 = df[(df['Age'] > 20) & (df['WHIP'] < 1.5)]
# Crear gráfico de dispersión
plt.figure(figsize=(16, 7))
sns.scatterplot(data=df_fig2, x='Age', y='WHIP', color='green', s=100)
# Títulos y etiquetas
plt.title('Mejores Pitchers por Edad según su WHIP')
plt.xlabel('Edad')
plt.ylabel('WHIP')
plt.grid(True)
plt.xlim(20, 42)
# Mostrar
plt.show()
st.pyplot(plt)

st.markdown("**Conclusión Gráfico 3:** El gráfico de dispersión muestra que los pitchers más jóvenes tienden a tener un WHIP más bajo. A medida que la edad aumenta, se observa una ligera tendencia al alza en el WHIP, sugiriendo que los pitchers más veteranos pueden enfrentar más dificultades para mantener a los corredores fuera de las bases. Un whip por debajo de 1.00 se considera excelente, mientras que un whip que se encuentra cercano a 1.5 se considera promedio.  Se ve como entre 25 y 35 años se encuentran los pitchers con mejor whip.")

# Filtrar los peores pitchers respecto a su WHIP y edad
df_fig4 = df[(df['Age'] > 20) & (df['WHIP'] > 2.00)]

# Verificar si hay datos
if df_fig4.empty:
    print("No hay datos que cumplan con los criterios seleccionados.")
else:
    # Agrupar por edad y calcular el promedio de ERA
    df_grouped = df_fig4.groupby('Age')['WHIP'].mean().reset_index()

    # Crear gráfico de barras
    plt.figure(figsize=(10 , 4))
    sns.barplot(data=df_grouped, x='Age', y='WHIP', color='Green')

    # Títulos y etiquetas
    plt.title('Rango de peores Pitchers por Edad según su WHIP')
    plt.xlabel('Edad')
    plt.ylabel('WHip Promedio')
    plt.grid(True)

    plt.tight_layout()
    plt.show()
    st.pyplot(plt)

#Rango de mejores pitchers por edad según su ERA
df_fig3 = df[(df['Age'] > 20) & (df['ERA'] < 4.00)]
# Crear gráfico de dispersión       
plt.figure(figsize=(16, 7))
sns.scatterplot(data=df_fig3, x='Age', y='ERA', color='red', s=100)
# Títulos y etiquetas
plt.title('Mejores Pitchers por Edad según su ERA')
plt.xlabel('Edad')
plt.ylabel('ERA')
plt.grid(True)
plt.xlim(20, 42)
# Mostrar
plt.show()
st.pyplot(plt)

# Filtrar los peores pitchers
df_fig5 = df[(df['Age'] > 20) & (df['ERA'] > 6.00)]

# Verificar si hay datos
if df_fig5.empty:
    print("No hay datos que cumplan con los criterios seleccionados.")
else:
    # Agrupar por edad y calcular el promedio de ERA
    df_grouped = df_fig5.groupby('Age')['ERA'].mean().reset_index()

    # Crear gráfico de barras
    plt.figure(figsize=(10, 3))
    sns.barplot(data=df_grouped, x='Age', y='ERA', color='red')

    # Títulos y etiquetas
    plt.title('Rango de peores Pitchers por Edad según su ERA')
    plt.xlabel('Edad')
    plt.ylabel('ERA Promedio')
    plt.grid(True)

    plt.tight_layout()
    plt.show()
    st.pyplot(plt)

# Grafico: Relacion Innings Pitched (IP) vs FIP
# Filtrar pitchers con mayor participación (por ejemplo, IP > 50)
df_mayor_participacion = df[df['IP'] > 50]

# Crear gráfico de dispersión
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_mayor_participacion, x='IP', y='FIP', color='blue', s=80)

# Títulos y etiquetas
plt.title('Relación entre IP y FIP de Pitchers con Mayor Participación')
plt.xlabel('Entradas Lanzadas (IP)')
plt.ylabel('Efectividad Independiente del Fildeo (FIP)')
plt.grid(True)

plt.tight_layout()
plt.show()
st.pyplot(plt)

# Gráfico: Caja: Distribución del FIP según Rangos de IP
# Filtrar pitchers con IP > 50
df_mayor_participacion = df[df['IP'] > 50]

# Crear rangos (bins) para IP
df_mayor_participacion['IP_rango'] = pd.cut(df_mayor_participacion['IP'], bins=[50, 70, 90, 110, 130, 150, 170])

# Crear gráfico de caja
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_mayor_participacion, x='IP_rango', y='FIP', color='orange')

# Títulos y etiquetas
plt.title('Gráfico de Caja: Distribución del FIP según Rangos de IP')
plt.xlabel('Rangos de Entradas Lanzadas (IP)')
plt.ylabel('FIP')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)
plt.show()

#Grafico: Top 10 pitchers por WHIP
# Filtrar los pitchers con mayor participación (IP más alto)
df_top_ip = df.sort_values(by='IP', ascending=False).head(30)  # puedes ajustar el número si lo deseas

# Ordenar por WHIP para encontrar los más eficientes entre los más duraderos
df_top_control = df_top_ip.sort_values(by='WHIP', ascending=True).head(10)

# Mostrar tabla con los pitchers más eficientes
print("Top 10 Pitchers con Mayor Participación y Mejor WHIP (MLB 2022):")
print(df_top_control[['Name', 'Tm', 'IP', 'WHIP']])

# Visualizar con gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(data=df_top_control, x='WHIP', y='Name', palette='viridis')
plt.title('Top 10 Pitchers con Mayor Participación y Mejor WHIP (MLB 2022)')
plt.xlabel('WHIP')
plt.ylabel('Pitcher')
plt.tight_layout()
plt.show()
st.pyplot(plt)

#Grafico: Top 10 pitchers por ERA
# Filtrar los pitchers con mayor participación (IP más alto)
df_top_ip = df.sort_values(by='IP', ascending=False).head(30)  # puedes ajustar el número si lo deseas

# Ordenar por ERA para encontrar los más efectivos entre los más duraderos
df_top_efectivos = df_top_ip.sort_values(by='ERA', ascending=True).head(10)

# Mostrar tabla con los pitchers más efectivos
print("Top 10 Pitchers con Mayor Participación y Mejor ERA (MLB 2022):")
print(df_top_efectivos[['Name', 'Tm', 'IP', 'ERA']])

# Visualizar con gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(data=df_top_efectivos, x='ERA', y='Name', palette='mako')
plt.title('Top 10 Pitchers con Mayor Participación y Mejor ERA (MLB 2022)')
plt.xlabel('ERA')
plt.ylabel('Pitcher')
plt.tight_layout()
plt.show()
st.pyplot(plt)
