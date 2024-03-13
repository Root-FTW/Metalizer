import streamlit as st
import pandas as pd
import re  # Para expresiones regulares

st.title('Filtrador de CSV para Analytics')

# Solicitar al usuario que cargue un archivo CSV
uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

# Solicitar al usuario que ingrese el rango de números
numero_inicial = st.number_input("Número inicial", min_value=0, value=0, step=1, format="%d")
numero_final = st.number_input("Número final", min_value=0, value=1000000, step=1, format="%d")

if uploaded_file is not None and numero_inicial < numero_final:
    # Cargar el archivo CSV, asegurándose de saltar las líneas de metadatos y usar el delimitador correcto
    df = pd.read_csv(uploaded_file, skiprows=9, delimiter=',')

    # Función para filtrar las filas basadas en el rango de números dentro de las URLs
    def filtrar_por_rango(df, col, inicio, fin):
        # Compilar la expresión regular que coincide con el patrón /videos/{número}/
        patron = re.compile(r'/videos/(\d+)/')
        
        # Función para aplicar a cada valor de la columna
        def coincide_con_rango(url):
            coincidencias = patron.search(url)
            if coincidencias:
                numero = int(coincidencias.group(1))
                return inicio <= numero <= fin
            return False
        
        # Filtrar el DataFrame usando la función definida
        return df[df[col].apply(coincide_con_rango)]

    # Aplicar el filtrado
    df_filtrado = filtrar_por_rango(df, "Page path and screen class", numero_inicial, numero_final)
    
    # Mostrar una vista previa de los datos filtrados
    st.write("Vista previa de los datos filtrados:")
    st.dataframe(df_filtrado)
    
    # Opción para descargar el archivo CSV filtrado
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar archivo CSV filtrado",
        data=csv,
        file_name='datos_filtrados.csv',
        mime='text/csv',
    )
else:
    st.write("Por favor, carga un archivo y asegúrate de que el número inicial sea menor que el número final.")
