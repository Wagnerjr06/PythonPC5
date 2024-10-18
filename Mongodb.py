from pymongo import MongoClient

# Conéctate a MongoDB
client = MongoClient('localhost', 27017)

# Verifica si puedes acceder a la base de datos
try:
    db = client.test
    print("Conexión exitosa a MongoDB.")
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
