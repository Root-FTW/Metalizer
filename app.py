import streamlit as st
import pandas as pd

st.title('Filtrador de CSV para Analytics')

uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

if uploaded_file is not None:
    # Asegúrate de que Pandas use el delimitador correcto, en este caso, una coma
    df = pd.read_csv(uploaded_file, skiprows=9, delimiter=',')

    # Mostrar las columnas en un selectbox y permitir al usuario seleccionar una
    columna_seleccionada = st.selectbox('Selecciona la columna que quieres conservar:', df.columns)
    
    # Mostrar DataFrame completo antes de la selección para depuración
    st.write("Vista previa de los datos cargados:")
    st.dataframe(df)
    
    # Filtrar el DataFrame para conservar solo la columna seleccionada
    df_filtrado = df[[columna_seleccionada]]
    
    # Mostrar los datos filtrados con solo la columna seleccionada
    st.write(f"Aquí están tus datos filtrados en la columna '{columna_seleccionada}':")
    st.dataframe(df_filtrado)
    
    # Convertir el DataFrame filtrado a CSV para permitir la descarga
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Descargar archivo filtrado",
        data=csv,
        file_name=f'archivo_filtrado_{columna_seleccionada}.csv',
        mime='text/csv',
    )
