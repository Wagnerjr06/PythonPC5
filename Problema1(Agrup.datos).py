import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
df_airbnb = pd.read_csv("./data/airbnb.csv")

# 1. Agrupamiento por tipo de habitación
grouped_by_room_type = df_airbnb.groupby('room_type').agg(
    avg_price=('price', 'mean'),
    avg_satisfaction=('overall_satisfaction', 'mean'),
    count=('room_id', 'count')
).reset_index()

print("Agrupamiento por tipo de habitación:")
print(grouped_by_room_type)

# Gráfico del agrupamiento por tipo de habitación
plt.figure(figsize=(12, 6))
sns.barplot(data=grouped_by_room_type, x='room_type', y='avg_price', palette='viridis')
plt.title('Precio Promedio por Tipo de Habitación')
plt.xlabel('Tipo de Habitación')
plt.ylabel('Precio Promedio (€)')
plt.xticks(rotation=45)
plt.show()

# Gráfico de satisfacción promedio por tipo de habitación
plt.figure(figsize=(12, 6))
sns.barplot(data=grouped_by_room_type, x='room_type', y='avg_satisfaction', palette='viridis')
plt.title('Satisfacción Promedio por Tipo de Habitación')
plt.xlabel('Tipo de Habitación')
plt.ylabel('Satisfacción Promedio')
plt.xticks(rotation=45)
plt.show()

# 2. Agrupamiento por barrio
grouped_by_neighborhood = df_airbnb.groupby('neighborhood').agg(
    total_properties=('room_id', 'count'),
    avg_price=('price', 'mean')
).reset_index()

print("Agrupamiento por barrio:")
print(grouped_by_neighborhood)

# Gráfico del agrupamiento por barrio
plt.figure(figsize=(15, 6))
sns.barplot(data=grouped_by_neighborhood.sort_values(by='total_properties', ascending=False).head(10), 
            x='neighborhood', y='total_properties', palette='viridis')
plt.title('Total de Propiedades por Barrio (Top 10)')
plt.xlabel('Barrio')
plt.ylabel('Total de Propiedades')
plt.xticks(rotation=45)
plt.show()

# Gráfico del precio promedio por barrio
plt.figure(figsize=(15, 6))
sns.barplot(data=grouped_by_neighborhood.sort_values(by='avg_price', ascending=False).head(10), 
            x='neighborhood', y='avg_price', palette='viridis')
plt.title('Precio Promedio por Barrio (Top 10)')
plt.xlabel('Barrio')
plt.ylabel('Precio Promedio (€)')
plt.xticks(rotation=45)
plt.show()
