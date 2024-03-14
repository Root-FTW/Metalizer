# Metalizer: Análisis Avanzado de Tráfico para Metatube

## Introducción

Bienvenidos a **Metalizer**, la herramienta definitiva diseñada para transformar el análisis de tráfico web de Metatube en una tarea sencilla, intuitiva y profundamente informativa. Metalizer nace de la fusión entre Metatube, una plataforma líder en contenido digital, y la necesidad de analizar de manera eficiente los datos que Google Analytics 4 (GA4) proporciona.

## ¿Qué es Metalizer?

Metalizer es una herramienta de análisis de tráfico web específicamente diseñada para Metatube. Permite a los usuarios cargar datos de tráfico en formato CSV exportados desde Google Analytics 4 (GA4) y filtrar esos datos basándose en criterios específicos como rangos numéricos en URLs y selección de idioma. La herramienta presenta los datos filtrados de manera clara y ofrece la posibilidad de descargarlos en formato Excel para un análisis más detallado.

## Características Principales

- **Carga de Archivos CSV**: Metalizer permite a los usuarios cargar fácilmente archivos CSV exportados desde GA4.
  
- **Filtrado Avanzado**: Los usuarios pueden filtrar los datos basándose en un rango numérico específico, que representa identificadores únicos en las URLs de Metatube, y también por idioma (español o inglés) o ver todos los datos sin filtrar.
  
- **Exportación de Datos**: Después del filtrado, Metalizer ofrece la posibilidad de descargar los datos filtrados en un archivo Excel, facilitando el análisis posterior o la presentación de reportes.

## Requisitos del Sistema

Para utilizar Metalizer, necesitarás:

- Python 3.6 o superior.
- Streamlit, pandas y openpyxl instalados en tu entorno Python.
- Acceso a archivos CSV exportados desde Google Analytics 4 (GA4).

## Instalación

### Paso 1: Configuración del Entorno Python

Asegúrate de tener Python 3.6 o superior instalado. Puedes verificar tu versión de Python ejecutando:

```sh
python --version
```

### Paso 2: Clonar el Repositorio de Metalizer

Clona el repositorio de Metalizer en tu máquina local utilizando Git:

```sh
git clone https://github.com/tu_usuario/metalizer.git
cd metalizer
```

### Paso 3: Instalar Dependencias

Instala las dependencias necesarias utilizando pip:

```sh
pip install streamlit pandas openpyxl
```

## Uso de Metalizer

Para iniciar Metalizer, navega al directorio donde clonaste el repositorio y ejecuta:

```sh
streamlit run app.py
```

### Cargar Archivo CSV

- Haz clic en "Elige un archivo CSV" y selecciona el archivo CSV exportado desde GA4.

### Especificar Criterios de Filtrado

- Ingresa el **Número inicial** y **Número final** para filtrar las URLs por un rango numérico específico.
- Selecciona el **idioma** para filtrar los datos o elige "Todos" para no aplicar filtrado por idioma.

### Visualizar y Descargar Datos Filtrados

- Revisa la "Vista previa de los datos filtrados" para asegurarte de que los datos coinciden con tus criterios de filtrado.
- Haz clic en "Descargar datos filtrados como Excel" para obtener un archivo Excel con los datos filtrados.

---

Por supuesto, para hacer el README aún más detallado y accesible para todos, desde desarrolladores novatos hasta personas no técnicas, profundicemos en la explicación del código y su funcionamiento. 

## Descripción Detallada del Código

El corazón de Metalizer es un script de Python diseñado para ser ejecutado con Streamlit, una herramienta que convierte scripts de Python en aplicaciones web interactivas. A continuación, se detalla cada parte del código y su propósito:

### Configuración Inicial

```python
import streamlit as st
import pandas as pd
import re
from io import BytesIO
```

- `streamlit` (alias `st`): Usado para crear la interfaz web. Nos permite añadir widgets como cargadores de archivos, entradas de texto y botones.
- `pandas`: Una biblioteca para manipulación y análisis de datos. Utilizada para cargar y filtrar datos del archivo CSV.
- `re`: Módulo de expresiones regulares de Python, utilizado para buscar patrones específicos en las URLs.
- `BytesIO`: Parte del módulo `io`, permite manejar archivos en memoria, útil para crear el archivo Excel a descargar.

### Configuración de la Página y Visualización del Logo

```python
st.set_page_config(page_title="Metalizer", page_icon=":metal:", layout="wide")
st.markdown("<a href='https://metatube.com/'>...</a>", unsafe_allow_html=True)
```

Establece el título de la página, el icono (usando un emoji de "metal") y el layout. También incluye el logo de Metatube como un enlace clickeable, mejorando la identidad visual de la aplicación.

### Interfaz de Usuario

```python
st.markdown('<p class="big-font">Metalizer</p>', unsafe_allow_html=True)
st.write("Descubre insights poderosos en los datos de tráfico de Metatube con Metalizer, tu analizador de GA4.")
```

Presenta el nombre de la herramienta con un estilo personalizado y proporciona una descripción clara de su propósito.

### Carga de Archivos y Selección de Opciones

```python
uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")
numero_inicial = st.number_input("Número inicial", min_value=0, value=0, step=1, format="%d")
numero_final = st.number_input("Número final", min_value=0, value=1000000, step=1, format="%d")
opcion_idioma = st.selectbox('Selecciona el idioma para filtrar...', ['Todos', '/es/', '/en/'])
```

Estos widgets permiten al usuario cargar un archivo CSV, especificar un rango numérico para filtrar URLs y seleccionar un idioma o la opción de ver todos los datos.

### Filtrado de Datos

```python
if uploaded_file is not None and numero_inicial < numero_final:
    df = pd.read_csv(uploaded_file, skiprows=9, delimiter=',')
    ...
```

Carga el archivo CSV, omitiendo las primeras 9 líneas de metadatos. Luego, aplica filtros basados en el rango numérico y el idioma seleccionado.

### Exportación de Datos Filtrados

```python
output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_filtrado.to_excel(writer, index=False)
```

Crea un archivo Excel en memoria con los datos filtrados, listo para ser descargado.

### Botón de Descarga

```python
st.download_button(
    label="Descargar datos filtrados como Excel",
    data=output.getvalue(),
    file_name='datos_filtrados.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
```

Ofrece al usuario un botón para descargar los datos filtrados en formato Excel.
