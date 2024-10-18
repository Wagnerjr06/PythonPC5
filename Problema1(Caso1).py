### Filtrado de datos

## Caso 1:

# Cargar el dataset
import pandas as pd

df_airbnb = pd.read_csv("./data/airbnb.csv")

# 1. Filtrar alojamientos que tengan más de 10 críticas y una puntuación mayor a 4
df_filtrado = df_airbnb[(df_airbnb['reviews'] > 10) & (df_airbnb['overall_satisfaction'] > 4)]

# 2. Filtrar alojamientos con al menos 2 habitaciones (una para los padres y otra para los hijos)
df_filtrado = df_filtrado[df_filtrado['bedrooms'] >= 2]

# 3. Ordenar primero por puntuación de mayor a menor y luego por número de críticas
df_ordenado = df_filtrado.sort_values(by=['overall_satisfaction', 'reviews'], ascending=[False, False])

# 4. Mostrar las 3 mejores alternativas
mejores_opciones = df_ordenado.head(3)

# Mostrar los resultados relevantes: ID del alojamiento, tipo, barrio, número de opiniones, puntuación y precio
print("Las 3 mejores alternativas para Alicia son:")
print(mejores_opciones[['room_id', 'room_type', 'neighborhood', 'reviews', 'overall_satisfaction', 'bedrooms', 'price']])