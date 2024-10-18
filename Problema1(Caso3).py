import pandas as pd

# Cargar el dataset
df_airbnb = pd.read_csv("./data/airbnb.csv")

# Filtrar propiedades: habitaciones compartidas y precio <= 50
filtered_properties = df_airbnb[(df_airbnb['room_type'] == 'Shared room') & (df_airbnb['price'] <= 50)]

# Ordenar por puntuación (overall_satisfaction) de mayor a menor y luego por precio de menor a mayor
sorted_properties = filtered_properties.sort_values(by=['overall_satisfaction', 'price'], ascending=[False, True])

# Seleccionar las 10 propiedades más baratas
top_10_properties = sorted_properties.head(10)

# Mostrar las propiedades seleccionadas
print("Las 10 propiedades más baratas para Diana:")
print(top_10_properties[['room_id', 'host_id', 'neighborhood', 'reviews', 'overall_satisfaction', 'accommodates', 'bedrooms', 'price']])
