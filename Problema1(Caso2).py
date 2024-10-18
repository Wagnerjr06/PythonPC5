## Caso 2:

import pandas as pd

# Cargar el dataset
df_airbnb = pd.read_csv("./data/airbnb.csv")

# IDs de las propiedades de Roberto y Clara
roberto_id = 97503
clara_id = 90387

# Filtrar las propiedades de Roberto y Clara
df_roberto_clara = df_airbnb[df_airbnb['room_id'].isin([roberto_id, clara_id])]

# Mostrar el DataFrame creado
print("Datos de las propiedades de Roberto y Clara:")
print(df_roberto_clara)

# Guardar el DataFrame como un archivo de Excel
df_roberto_clara.to_excel("roberto.xlsx", index=False)