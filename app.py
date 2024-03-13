import streamlit as st
import pandas as pd

st.title('Filtrador de CSV para Analytics')

uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

if uploaded_file is not None:
    # Cargar el archivo CSV, asegurándose de saltar las líneas de metadatos y usar el delimitador correcto
    df = pd.read_csv(uploaded_file, skiprows=9, delimiter=',')

    # Mostrar una vista previa de todos los datos cargados
    st.write("Vista previa de los datos cargados:")
    st.dataframe(df)
    
    # Opción para descargar el archivo CSV originalmente cargado
    # Si necesitas realizar algún filtrado u operación antes de la descarga, puedes ajustar el DataFrame aquí
    csv = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Descargar archivo CSV",
        data=csv,
        file_name='datos_cargados.csv',
        mime='text/csv',
    )
