import streamlit as st
import pandas as pd
from filtrar_csv import filtrar_csv
import os

st.title('Filtrador de CSV para Analytics')

uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")
if uploaded_file is not None:
    # Guardar el archivo subido en el sistema de archivos temporal
    with open(os.path.join("temp",uploaded_file.name),"wb") as f:
        f.write(uploaded_file.getbuffer())
    # Procesar el archivo
    archivo_salida = os.path.join("temp","filtrado_" + uploaded_file.name)
    filtrar_csv(os.path.join("temp",uploaded_file.name), archivo_salida)
    
    st.success('¡Archivo procesado con éxito!')
    with open(archivo_salida, "rb") as file:
        btn = st.download_button(
            label="Descargar archivo filtrado",
            data=file,
            file_name="filtrado_" + uploaded_file.name,
            mime="text/csv",
        )
