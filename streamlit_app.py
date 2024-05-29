import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Cargar los datos
@st.cache
def cargar_datos('IMDB-Movie-Data.csv'):
    data = pd.read_csv('IMDB-Movie-Data.csv')
    return data

# Función de búsqueda
def buscar_peliculas(df, titulo=None, genero=None, año=None):
    if titulo:
        df = df[df['Title'].str.contains(titulo, case=False, na=False)]
    if genero:
        df = df[df['Genre'].str.contains(genero, case=False, na=False)]
    if año:
        df = df[df['Year'] == año]
    return df

# Visualización de datos
def visualizar_datos(df_filtrado):
    # Gráfico de ingresos por año
    ingresos_filtrados = df_filtrado.groupby('Year')['Revenue (Millions)'].sum()
    plt.figure(figsize=(12, 6))
    plt.bar(ingresos_filtrados.index, ingresos_filtrados.values, color='skyblue')
    plt.title('Ingresos Totales por Año (en millones de dólares)')
    plt.xlabel('Año')
    plt.ylabel('Ingresos Totales (Millones de dólares)')
    plt.grid(True)
    st.pyplot(plt)

    # Tablas de top 20
    top_20_ingresos = df_filtrado.sort_values(by='Revenue (Millions)', ascending=False).head(20)
    top_20_rating = df_filtrado.sort_values(by='Rating', ascending=False).head(20)
    top_20_votos = df_filtrado.sort_values(by='Votes', ascending=False).head(20)

    # Actores más repetidos
    actores_lista = ','.join(df_filtrado['Actors']).split(',')
    actores_contados = Counter([actor.strip() for actor in actores_lista])
    actores_top = actores_contados.most_common(20)
    actores_top_df = pd.DataFrame(actores_top, columns=['Actor', 'Apariciones'])

    # Mostrar tablas
    st.write("Top 20 Películas por Ingresos", top_20_ingresos)
    st.write("Top 20 Películas por Rating", top_20_rating)
    st.write("Top 20 Películas por Votos", top_20_votos)
    st.write("Actores Más Repetidos", actores_top_df)

# Interfaz de usuario
def main():
    st.title("Aplicación de Búsqueda de Películas")
    filepath = st.text_input("Ingrese el path del archivo CSV de películas:")
    if filepath:
        df = cargar_datos(filepath)
        titulo = st.text_input("Filtrar por título:")
        genero = st.text_input("Filtrar por género:")
        año = st.number_input("Filtrar por año:", min_value=1900, max_value=2100, step=1, format="%d")
        df_filtrado = buscar_peliculas(df, titulo, genero, año)
        visualizar_datos(df_filtrado)

if __name__ == "__main__":
    main()
