import streamlit as st
import pandas as pd

# Título de la aplicación en Streamlit
st.title('Filtrador de CSV para Analytics')

# Widget de carga de archivo CSV
uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

# Procesamiento después de que el archivo es cargado
if uploaded_file is not None:
    # Lectura del archivo CSV, saltando las primeras 9 líneas de metadatos
    df = pd.read_csv(uploaded_file, skiprows=9)
    
    # Permitir al usuario seleccionar la columna de interés a través de un dropdown
    columna_seleccionada = st.selectbox('Selecciona la columna que quieres conservar:', df.columns)
    
    # Asegurarse de que la columna seleccionada sea de tipo string
    df[columna_seleccionada] = df[columna_seleccionada].astype(str)
    
    # Filtrar filas que contengan '/es/videos/' o '/en/videos/' en la columna seleccionada
    filtro = '/es/videos/|/en/videos/'
    df_filtrado = df[df[columna_seleccionada].str.contains(filtro, na=False)]
    
    # Conservar solo la columna seleccionada por el usuario
    df_filtrado = df_filtrado[[columna_seleccionada]]
    
    # Mostrar los datos filtrados en la interfaz de Streamlit
    st.write("Aquí están tus datos filtrados:")
    st.dataframe(df_filtrado)
    
    # Convertir el DataFrame filtrado a CSV para permitir la descarga
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    
    # Botón de descarga para el archivo CSV filtrado
    st.download_button(
        label="Descargar archivo filtrado",
        data=csv,
        file_name='archivo_filtrado.csv',
        mime='text/csv',
    )
