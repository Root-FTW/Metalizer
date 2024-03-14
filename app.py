import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.title('Filtrador de CSV para Analytics')

# Solicitar al usuario que cargue un archivo CSV
uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

# Solicitar al usuario que ingrese el rango de números
numero_inicial = st.number_input("Número inicial", min_value=0, value=0, step=1, format="%d")
numero_final = st.number_input("Número final", min_value=0, value=1000000, step=1, format="%d")

# Solicitar al usuario que seleccione el idioma para el filtrado o 'Todos' para no filtrar
opcion_idioma = st.selectbox('Selecciona el idioma para filtrar (o Todos para no filtrar):', ['Todos', '/es/', '/en/'])

if uploaded_file is not None and numero_inicial < numero_final:
    # Cargar el archivo CSV, asegurándose de saltar las líneas de metadatos y usar el delimitador correcto
    df = pd.read_csv(uploaded_file, skiprows=9, delimiter=',')

    # Filtrar por idioma si es necesario
    if opcion_idioma != 'Todos':
        df = df[df['Page path and screen class'].str.startswith(opcion_idioma)]

    # Función para filtrar las filas basadas en el rango de números dentro de las URLs
    def filtrar_por_rango(df, col, inicio, fin):
        patron = re.compile(r'/videos/(\d+)/')
        def coincide_con_rango(url):
            coincidencias = patron.search(url)
            if coincidencias:
                numero = int(coincidencias.group(1))
                return inicio <= numero <= fin
            return False
        return df[df[col].apply(coincide_con_rango)]

    # Aplicar el filtrado
    df_filtrado = filtrar_por_rango(df, "Page path and screen class", numero_inicial, numero_final)
    
    # Mostrar una vista previa de los datos filtrados
    st.write("Vista previa de los datos filtrados:")
    st.dataframe(df_filtrado)
    
    # Convertir el DataFrame filtrado a un archivo Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_filtrado.to_excel(writer, index=False)
    
    # Crear un botón de descarga para el archivo Excel filtrado
    st.download_button(
        label="Descargar datos filtrados como Excel",
        data=output.getvalue(),
        file_name='datos_filtrados.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
else:
    st.write("Por favor, carga un archivo y asegúrate de que el número inicial sea menor que el número final.")
