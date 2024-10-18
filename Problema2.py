import pandas as pd
import sqlite3
from pymongo import MongoClient
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # Importa MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Cargar los datos
df = pd.read_csv('winemag-data-130k-v2.csv')

# Explorar el DataFrame
print(df.info())
print(df.head())

# Renombrar columnas
df.rename(columns={
    'country': 'Country',
    'description': 'Description',
    'points': 'Points',
    'price': 'Price'
}, inplace=True)

# Crear nuevas columnas
# 1. Añadir columna 'Continent' según el país
country_to_continent = {
    'Italy': 'Europe', 'France': 'Europe', 'Spain': 'Europe',
    'USA': 'North America', 'Argentina': 'South America',
    'Australia': 'Oceania', 'South Africa': 'Africa',
    # Agrega más países y continentes según sea necesario
}
df['Continent'] = df['Country'].map(country_to_continent)

# 2. Añadir columna 'Price Category' según el precio
df['Price Category'] = pd.cut(df['Price'], bins=[0, 10, 20, 50, 100, float('inf')],
                               labels=['Cheap', 'Moderate', 'Expensive', 'Luxury', 'Very Expensive'])

# 3. Añadir columna 'Review Length' según la longitud de la descripción
df['Review Length'] = df['Description'].str.len()

# Reporte 1: Vinos mejor puntuados por continente
report1 = df.groupby('Continent').agg({'Points': 'max'}).reset_index()
report1.to_csv('best_wines_by_continent.csv', index=False)

# Reporte 2: Promedio de precio de vino y cantidad de reviews según país
report2 = df.groupby('Country').agg({'Price': 'mean', 'Description': 'count'}).reset_index()
report2.rename(columns={'Description': 'Review Count'}, inplace=True)
report2 = report2.sort_values(by='Price', ascending=False)
report2.to_excel('average_price_reviews_by_country.xlsx', index=False)

# Reporte 3: Vinos con puntuación y precio
report3 = df[['Country', 'Price', 'Points']].sort_values(by='Points', ascending=False)
report3.to_sql('wines_points_price', sqlite3.connect('wines.db'), index=False, if_exists='replace')

# Reporte 4: Conteo de vinos por categoría de precio
report4 = df['Price Category'].value_counts().reset_index()
report4.columns = ['Price Category', 'Count']
client = MongoClient('mongodb://localhost:27017/')
db = client['wine_database']
db.wine_reports.insert_many(report4.to_dict('records'))

print("Reportes generados y exportados correctamente.")

def send_email(report_path):
    from_address = 'juniordracildrago921@gmail.com'
    to_address = 'w.pacheco@pucp.edu.pe'
    subject = 'Reporte de Vinos'
    body = 'Adjunto se encuentra el reporte de vinos.'

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))  # Asegúrate de que MIMEText esté importado

    attachment = open(report_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={report_path}')
    msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_address, 'Xivina13579246810')  # Asegúrate de usar tu contraseña
        server.send_message(msg)

    print("Correo enviado correctamente.")

# Llamar a la función de envío
send_email('best_wines_by_continent.csv')

