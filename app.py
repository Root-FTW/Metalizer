import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Metalizer", page_icon=":metal:", layout="wide")

# Mostrar el logo de Metatube
logo_url = "https://www.metatube.com/assets/layout/css/img/LogoFooter.svg"
st.image(logo_url, width=449)

# Estilos personalizados y título grande
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown('<p class="big-font">Metalizer</p>', unsafe_allow_html=True)

st.write("Descubre insights poderosos en los datos de tráfico de Metatube con Metalizer, tu analizador de GA4.")

# Solicitar al usuario que cargue un archivo CSV y seleccione opciones
col1, col2, col3 = st.columns(3)
with col1:
    uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")
with col2:
    numero_inicial = st.number_input("Número inicial", min_value=0, value=0, step=1, format="%d")
with col3:
    numero_final = st.number_input("Número final", min_value=0, value=1000000, step=1, format="%d")

opcion_idioma = st.selectbox('Selecciona el idioma para filtrar (o Todos para no filtrar):', ['Todos', '/es/', '/en/'])

# Función principal para filtrar los datos
if uploaded_file is not None and numero_inicial < numero_final:
    df = pd.read_csv(uploaded_file, skiprows=9, delimiter=',')

    if opcion_idioma != 'Todos':
        df = df[df['Page path and screen class'].str.startswith(opcion_idioma)]
    
    def filtrar_por_rango(df, col, inicio, fin):
        patron = re.compile(r'/videos/(\d+)/')
        def coincide_con_rango(url):
            coincidencias = patron.search(url)
            if coincidencias:
                numero = int(coincidencias.group(1))
                return inicio <= numero <= fin
            return False
        return df[df[col].apply(coincide_con_rango)]
    
    df_filtrado = filtrar_por_rango(df, "Page path and screen class", numero_inicial, numero_final)
    
    st.write("Vista previa de los datos filtrados:")
    st.dataframe(df_filtrado)
    
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
    st.write("Por favor, carga un archivo y asegúrate de que el número inicial sea menor que el número final.")
