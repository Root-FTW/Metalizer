import streamlit as st
import pandas as pd
import re
from io import BytesIO
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import requests

# Función para cargar stopwords desde un enlace
def cargar_stopwords(url):
    response = requests.get(url)
    stopwords = set(response.text.splitlines())
    return stopwords

# Cargar las listas de stopwords
spanish_stopwords_url = "https://raw.githubusercontent.com/Alir3z4/stop-words/master/spanish.txt"
english_stopwords_url = "https://raw.githubusercontent.com/Alir3z4/stop-words/master/english.txt"

spanish_stopwords = cargar_stopwords(spanish_stopwords_url)
english_stopwords = cargar_stopwords(english_stopwords_url)

stopwords = spanish_stopwords.union(english_stopwords)

# Configuración de la página
st.set_page_config(page_title="BuscaLizer", page_icon=":metal:", layout="wide")

# Mostrar el logo de BuscaLizer como un enlace
st.markdown("""
<a href="https://busca.media/">
    <img src="https://buscamedia.mx/assets/images/image14.svg" alt="BuscaMedia Logo" width="449">
</a>
""", unsafe_allow_html=True)

# Estilos personalizados y título grande
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 160px;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 5px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%; /* Position the tooltip above the text */
        left: 50%;
        margin-left: -80px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown('<p class="big-font">BuscaLizer</p>', unsafe_allow_html=True)

# Descripción actualizada
st.write("Descubre insights poderosos en los datos de tráfico de BuscaMedia con BuscaLizer, tu analizador de GA4.")

# Solicitar al usuario que cargue un archivo CSV y seleccione opciones
col1, col2, col3 = st.columns(3)
with col1:
    uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")
with col2:
    numero_inicial = st.number_input("Número inicial", min_value=0, value=0, step=1, format="%d")
with col3:
    numero_final = st.number_input("Número final", min_value=0, value=1000000, step=1, format="%d")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, delimiter=',')

    # Función para extraer el tema de la URL
    def extraer_tema(url):
        try:
            if isinstance(url, str):  # Verificar si la URL es una cadena
                match = re.match(r'/[^/]+/([^/]+)/\d+/', url)
                if match:
                    return match.group(1)
        except Exception as e:
            st.write(f"Error procesando la URL: {url} - {e}")
        return None

    # Aplicar la función al DataFrame
    df['Tema'] = df['Page path and screen class'].apply(extraer_tema)

    # Extraer todos los temas únicos
    temas_unicos = df['Tema'].dropna().unique()

    opcion_tema = st.multiselect('Selecciona el tema para filtrar:', temas_unicos, default=temas_unicos)

    opcion_idioma = st.selectbox('Selecciona el idioma para filtrar (o Todos para no filtrar):', ['Todos', '/es/', '/en/'])

    # Solicitar al usuario que seleccione un rango de usuarios
    col4, col5 = st.columns(2)
    with col4:
        users_min = st.number_input("Cantidad mínima de usuarios", min_value=0, value=0, step=1, format="%d")
    with col5:
        users_max = st.number_input("Cantidad máxima de usuarios", min_value=0, value=1000000, step=1, format="%d")

    # Función principal para filtrar los datos
    if numero_inicial < numero_final and users_min < users_max:

        # Filtrar por tema
        df_filtrado = df[df['Tema'].isin(opcion_tema)]

        # Filtrar por idioma
        if opcion_idioma != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Page path and screen class'].str.startswith(opcion_idioma)]

        # Filtrar por rango de números en las URLs
        def filtrar_por_rango(df, col, inicio, fin):
            patron = re.compile(r'/[^/]+/([^/]+)/(\d+)/')
            def coincide_con_rango(url):
                url_str = str(url)  # Convertir explícitamente el valor a string
                coincidencias = patron.search(url_str)
                if coincidencias:
                    numero = int(coincidencias.group(2))
                    return inicio <= numero <= fin
                return False
            return df[df[col].apply(coincide_con_rango)]

        df_filtrado = filtrar_por_rango(df_filtrado, "Page path and screen class", numero_inicial, numero_final)

        # Filtrar por cantidad de usuarios
        df_filtrado = df_filtrado[(df_filtrado['Total users'] >= users_min) & (df_filtrado['Total users'] <= users_max)]

        st.write("Vista previa de los datos filtrados:")
        col6, col7 = st.columns([2, 1])
        with col6:
            st.dataframe(df_filtrado)

        # Calcular las estadísticas de la columna "Total users"
        if 'Total users' in df_filtrado.columns:
            suma_total_users = df_filtrado['Total users'].sum()
            suma_total_users_formateada = "{:,}".format(suma_total_users)
            promedio_total_users = df_filtrado['Total users'].mean()
            promedio_total_users_formateado = "{:.2f}".format(promedio_total_users)
            mediana_total_users = df_filtrado['Total users'].median()
            min_total_users = df_filtrado['Total users'].min()
            max_total_users = df_filtrado['Total users'].max()
            cantidad_urls_filtradas = len(df_filtrado)

            with col7:
                st.markdown(f"""
                <div class="tooltip">Cantidad de URLs filtradas: {cantidad_urls_filtradas}
                    <span class="tooltiptext">El número total de URLs después de aplicar los filtros.</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="tooltip">Suma de 'Total users' en los datos filtrados: {suma_total_users_formateada}
                    <span class="tooltiptext">La suma total de todos los usuarios en los datos filtrados.</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="tooltip">Promedio de 'Total users' en los datos filtrados: {promedio_total_users_formateado}
                    <span class="tooltiptext">El promedio de usuarios por página en los datos filtrados.</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="tooltip">Mediana de 'Total users' en los datos filtrados: {mediana_total_users}
                    <span class="tooltiptext">El valor central de usuarios cuando los datos están ordenados.</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="tooltip">Valor mínimo de 'Total users' en los datos filtrados: {min_total_users}
                    <span class="tooltiptext">El menor número de usuarios en los datos filtrados.</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="tooltip">Valor máximo de 'Total users' en los datos filtrados: {max_total_users}
                    <span class="tooltiptext">El mayor número de usuarios en los datos filtrados.</span>
                </div>
                """, unsafe_allow_html=True)

        # Crear gráfica de pastel para mostrar proporción de usuarios por idioma
        df_filtrado['Idioma'] = df_filtrado['Page path and screen class'].apply(lambda x: 'es' if '/es/' in x else ('en' if '/en/' in x else 'Otros'))
        usuarios_por_idioma = df_filtrado.groupby('Idioma')['Total users'].sum()

        fig_pie, ax_pie = plt.subplots(figsize=(5, 5))
        ax_pie.pie(usuarios_por_idioma, labels=usuarios_por_idioma.index, autopct='%1.1f%%', startangle=90)
        ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        fig_pie.suptitle('Proporción de Usuarios por Idioma')

        # Generar nube de palabras
        text = " ".join(df_filtrado['Page path and screen class'])
        wordcloud = WordCloud(width=400, height=400, background_color='white', stopwords=stopwords).generate(text)

        # Mostrar la nube de palabras
        fig_wordcloud, ax_wordcloud = plt.subplots(figsize=(5, 5))
        ax_wordcloud.imshow(wordcloud, interpolation='bilinear')
        ax_wordcloud.axis('off')
        fig_wordcloud.suptitle('Nube de Palabras de URLs Filtradas')

        col8, col9 = st.columns(2)
        with col8:
            st.pyplot(fig_pie)
        with col9:
            st.pyplot(fig_wordcloud)

        # Botones para descargar las gráficas como PNG
        pie_img = BytesIO()
        fig_pie.savefig(pie_img, format='png')
        pie_img.seek(0)

        wordcloud_img = BytesIO()
        fig_wordcloud.savefig(wordcloud_img, format='png')
        wordcloud_img.seek(0)

        st.download_button(
            label="Descargar gráfica de pastel como PNG",
            data=pie_img,
            file_name='grafica_pastel.png',
            mime='image/png'
        )

        st.download_button(
            label="Descargar nube de palabras como PNG",
            data=wordcloud_img,
            file_name='nube_palabras.png',
            mime='image/png'
        )

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_filtrado.to_excel(writer, index=False)

        st.download_button(
            label="Descargar datos filtrados como Excel",
            data=output.getvalue(),
            file_name='datos_filtrados.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
else:
    st.write("Por favor, carga un archivo y asegúrate de que el número inicial y la cantidad mínima de usuarios sean menores que el número final y la cantidad máxima de usuarios, respectivamente.")
