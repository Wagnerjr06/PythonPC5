### Analisis exploratorio
import pandas as pd

df_airbnb = pd.read_csv("./data/airbnb.csv")

print("Shape (dimensiones):", df_airbnb.shape)

print("\nPrimeras 5 filas del dataset:")
print(df_airbnb.head())

print("\nColumnas del dataset:")
print(df_airbnb.columns)

print("\nTipos de datos de cada columna:")
print(df_airbnb.dtypes)

print("\nValores faltantes por columna:")
print(df_airbnb.isnull().sum())

print("\nResumen estadístico de las variables numéricas:")
print(df_airbnb.describe())

print("\nTipos de propiedades (room_type) únicos:")
print(df_airbnb['room_type'].unique())

print("\nBarrios (neighborhood) únicos:")
print(df_airbnb['neighborhood'].unique())




