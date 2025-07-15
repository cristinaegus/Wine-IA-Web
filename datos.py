from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from flask import Flask, render_template, request, jsonify

# Configuración de Selenium para Chrome en modo headless
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')

# Cambia la ruta si tienes chromedriver en otro lugar
service = Service('/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.vivino.com/"
driver.get(url)
time.sleep(3)  # Espera para cargar la página
html_content = driver.page_source

driver.quit()

soup = BeautifulSoup(html_content, "html.parser")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/datos", methods=["GET"])
def obtener_datos():
    # Aquí puedes procesar los datos obtenidos con BeautifulSoup
    datos = {"mensaje": "Datos obtenidos correctamente"}
    return jsonify(datos)

if __name__ == "__main__":
    app.run(debug=True)

# Ejemplo: Extraer todos los enlaces (etiquetas <a>)
for link in soup.find_all('a'):
    href = link.get('href')
    text = link.text
    print(f"Enlace: {href}, Texto: {text}")

# Ejemplo: Extraer datos de una tabla
table = soup.find('table', {'class': 'mi-tabla'})
if table:
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if cells:
            # Procesa las celdas de la fila
            data = [cell.text.strip() for cell in cells]
            print(data)