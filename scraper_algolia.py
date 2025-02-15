import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuración de la API de Algolia
ALGOLIA_APP_ID = os.getenv("ALGOLIA_APP_ID")
ALGOLIA_API_KEY = os.getenv("ALGOLIA_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME")

# Headers de la petición
headers = {
    "x-algolia-application-id": ALGOLIA_APP_ID,
    "x-algolia-api-key": ALGOLIA_API_KEY,
    "Content-Type": "application/json"
}

# Filtro por los IDs de centro (extraídos de la petición que enviaste)
filters = " OR ".join([f"data.idCentre:'{id_centre}'" for id_centre in [
   97361
]])

# URL de la API de Algolia
url = f"https://{ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/{INDEX_NAME}/query"

# Variables para paginación
all_results = []
page = 0
hits_per_page = 9  # Como se ve en la respuesta de Algolia

while True:
    # Payload con la paginación
    payload = {
        "params": f"filters={filters}&query=&page={page}&distinct=true&hitsPerPage={hits_per_page}"
    }

    # Realizar la petición
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()

    # Almacenar los resultados obtenidos
    all_results.extend(data.get("hits", []))

    # Verificar si hay más páginas
    if page >= data.get("nbPages", 1) - 1:
        break  # No hay más páginas, salimos del loop

    # Pasamos a la siguiente página
    page += 1

# Guardar resultados en un archivo JSON
with open("centros_filtrados.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=4, ensure_ascii=False)

print(f"✅ Se han obtenido {len(all_results)} centros filtrados y guardado en 'centros_filtrados.json'")
