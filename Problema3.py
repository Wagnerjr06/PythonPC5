import requests
import zipfile
import os
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

# Paso 1: Descargar el archivo .zip
url = 'https://netsg.cs.sfu.ca/youtubedata/0302.zip'
zip_path = '0302.zip'

# Descargar el archivo
try:
    response = requests.get(url)
    response.raise_for_status()  # Verifica si la solicitud fue exitosa
    with open(zip_path, 'wb') as file:
        file.write(response.content)
    print("Archivo .zip descargado exitosamente.")
except Exception as e:
    print(f"Error al descargar el archivo: {e}")

# Paso 2: Descomprimir el archivo en una carpeta
output_dir = 'youtubedata_0302'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    print(f'Datos descomprimidos en la carpeta: {output_dir}')
except zipfile.BadZipFile:
    print("Error: El archivo zip está corrupto o no es un zip válido.")

# Listar los archivos descomprimidos en la carpeta
extracted_files = os.listdir(output_dir)
print(f'Archivos descomprimidos: {extracted_files}')

# Paso 3: Entrar en la subcarpeta '0302' y listar archivos
subfolder_path = os.path.join(output_dir, extracted_files[0])
subfolder_files = os.listdir(subfolder_path)
print(f'Archivos dentro de la subcarpeta: {subfolder_files}')

# Usar uno de los archivos en la subcarpeta, por ejemplo, '0.txt'
file_path = os.path.join(subfolder_path, '0.txt')

# Verificar si el archivo existe antes de abrirlo
if os.path.exists(file_path):
    # Inspección manual de las primeras líneas del archivo para verificar su estructura
    with open(file_path, 'r') as f:
        print("Primeras líneas del archivo:")
        for _ in range(10):
            print(f.readline())
else:
    print(f"Error: El archivo {file_path} no existe.")

# Paso 4: Leer los datos con pandas, ignorando líneas problemáticas
try:
    df = pd.read_csv(file_path, sep='\s+', header=None, on_bad_lines='warn')  # Cambiar el separador a espacios
    print("Datos leídos exitosamente.")
    
    # Inspeccionar la forma del DataFrame
    print(f"Número de columnas leídas: {df.shape[1]}")
except Exception as e:
    print(f"Error al leer el archivo: {e}")

# Paso 5: Asignar nombres de columnas si la lectura fue exitosa
if 'df' in locals() and not df.empty:  # Verificar si el DataFrame se cargó correctamente y no está vacío
    # Verificar la longitud de las columnas
    column_names = ['VideoID', 'Uploader', 'Age', 'Category', 'Length', 'Views', 'Rate', 'Ratings', 'Comments']
    if len(column_names) == df.shape[1]:
        df.columns = column_names
    else:
        print(f"Advertencia: Se esperaban {len(column_names)} columnas, pero se leyeron {df.shape[1]}.")

    # Filtrar las columnas que nos interesan
    df_filtered = df[['VideoID', 'Age', 'Category', 'Views', 'Rate']]

    # Filtrar por categoría, por ejemplo, 'Sports'
    df_sports = df_filtered[df_filtered['Category'] == 'Sports']
    print("Datos filtrados para la categoría 'Sports':")
    print(df_sports.head())

    # Exportar los datos a MongoDB
    try:
        client = MongoClient('localhost', 27017)  # Conectar a MongoDB
        db = client['youtube_data']                 # Seleccionar la base de datos
        collection = db['videos']                   # Seleccionar la colección

        # Convertir el DataFrame a diccionario e insertar en MongoDB
        data_dict = df_filtered.to_dict("records")
        collection.insert_many(data_dict)
        print("Datos exportados a MongoDB.")
    except Exception as e:
        print(f"Error al exportar datos a MongoDB: {e}")

    # Crear gráficos
    try:
        # Gráfico 1: Distribución de vistas por edad
        plt.figure(figsize=(10, 6))
        plt.hist(df_filtered['Age'], bins=20, color='skyblue', edgecolor='black')
        plt.title('Distribución de Vistas por Edad')
        plt.xlabel('Edad')
        plt.ylabel('Cantidad de Videos')
        plt.grid(True)
        plt.show()

        # Gráfico 2: Vistas totales por categoría
        category_views = df_filtered.groupby('Category')['Views'].sum()

        plt.figure(figsize=(10, 6))
        category_views.plot(kind='bar', color='orange', edgecolor='black')
        plt.title('Vistas Totales por Categoría')
        plt.xlabel('Categoría')
        plt.ylabel('Vistas Totales')
        plt.grid(True)
        plt.show()

        # Exportar los datos filtrados a un archivo CSV
        df_filtered.to_csv('filtered_youtube_data.csv', index=False)
        print("Datos exportados a 'filtered_youtube_data.csv'.")
    except Exception as e:
        print(f"Error al crear gráficos o exportar datos: {e}")
else:
    print("No se pudo cargar el DataFrame. Verifica la lectura del archivo.")








