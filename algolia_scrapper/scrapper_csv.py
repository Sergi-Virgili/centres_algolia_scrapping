import requests
import json
import csv
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuración de la API de Algolia
ALGOLIA_APP_ID = os.getenv("ALGOLIA_APP_ID")
ALGOLIA_API_KEY = os.getenv("ALGOLIA_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME")

# Headers de la petición
HEADERS = {
    "x-algolia-application-id": ALGOLIA_APP_ID,
    "x-algolia-api-key": ALGOLIA_API_KEY,
    "Content-Type": "application/json"
}

# IDs de los centros a buscar
CENTRE_IDS = [
    99817, 99805, 99662, 99590, 99531, 99456, 99332, 99106, 99067, 98976, 98975, 98928, 98752, 98677, 98553, 98546, 98522,
  98510, 98401, 98249, 98233, 98227, 98187, 98184, 98178, 98172, 98169, 98137, 98134, 98015, 97928, 97904, 97878, 97874,
  97838, 97664, 97361, 97352, 97285, 97230, 97185, 97123, 97120, 97117, 97114, 97109, 97106, 97098, 97087, 97074, 96818,
  96805, 96645, 96641, 96576, 96532, 96488, 96343, 96270, 96003, 95955, 95913, 95832, 95653, 95452, 95446, 95295, 95198,
  95107, 95023, 95010, 94950, 94908, 94846, 94784, 94741, 94560, 94297, 94291, 94284, 94128, 94025, 94007, 93933, 93807,
  93120, 93117, 93114, 93067, 93064, 92929, 92866, 92765, 92636, 92522, 92468, 92217, 92121, 92121, 92062, 92039, 91759,
  91551, 91551, 90925, 90540, 90540, 90516, 90426, 90292, 90146, 89828, 89722, 89464, 88951, 88633, 88477, 88467, 88289,
  88221, 87986, 87903, 87706, 87706, 87600, 87600, 87531, 87057, 86773, 85814, 85768, 85110, 85077, 84873, 84873, 84276,
  84161, 84130, 84053, 83891, 83858, 83679, 83360, 83359, 83286, 83219, 82863, 82778, 82629, 81467, 81208, 81187, 80869,
  80347, 79453, 77784, 77636, 77577, 77314, 77150, 76816, 76637, 76637, 76632, 76411, 75852, 75525, 75516, 75337, 73735,
  73015, 72476, 72455, 72455, 72015, 71377, 71376, 70658, 70540, 69295, 69295, 67949, 67389, 67050, 66488, 66480, 66189,
  65932, 65777, 65129, 64974, 64869, 64845, 64769, 64429, 63868, 63862, 62349, 58949, 58947, 55836, 55489, 55376, 55109,
  54949, 52270, 48910, 48858, 47735, 47709, 47169, 46173, 46031, 45152, 45090, 44929, 44789, 44473, 44276, 43569, 43555,
  43014, 42866, 42865, 42209, 41862, 40830, 39070, 38970, 38312, 37108, 36951, 36249, 35536, 35214, 33917, 33912, 33912,
  33813, 33470, 33411, 33362, 33362, 33350, 33320, 32805, 32457, 32328, 32265, 31883, 31723, 31015, 30951, 30949, 30947,
  30946, 30891, 30859, 30845, 30833, 30748, 30722, 30717, 30706, 30705, 30676, 30659, 30653, 30640, 30573, 30559, 30558,
  30553, 30470, 30466, 30460, 30457, 30457, 30453, 30445, 30445, 30439, 30426, 30392, 30346, 30341, 30321, 30265, 30265,
  30260, 30252, 30232, 30211, 30181, 30169, 30141, 30140, 30139, 30138, 30137, 30135, 30110, 30097, 30051, 30050, 30018,
  29999, 29994, 29994, 29951, 29918, 29905, 29893, 29868, 29841, 29840, 29834, 29830, 29805, 29778, 29778, 29774, 29754,
  29680, 29680, 14481, 129016, 127415, 126013, 125713, 125113, 124412, 122812, 122511, 122110, 121910, 121710, 121509,
  121409, 121309, 121109, 120807, 119205, 118104, 118004, 117502, 116602, 116299, 116099, 115798, 112590, 109085, 108184,
  107280, 106379, 105779, 104276, 102675, 102475, 102309, 102277, 102027, 102012, 101944, 101749, 101693, 101633, 101554,
  101526, 101523, 101522, 101519, 101455, 101446, 101308, 101217, 101214, 101147, 101115, 100979, 100976, 100966, 100941,
  100884, 100865, 100852, 100722, 100702, 100626, 100600, 100395, 100244, 100215, 100108, 100092, 100089, 100055
]

# URL de la API de Algolia
URL = f"https://{ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/{INDEX_NAME}/query"


def fetch_data_from_algolia(centre_ids, hits_per_page=9):
    """
    Obtiene datos de Algolia paginando los resultados.
    """
    filters = " OR ".join([f"data.idCentre:'{id_centre}'" for id_centre in centre_ids])
    all_results = []
    page = 0

    while True:
        payload = {
            "params": f"filters={filters}&query=&page={page}&distinct=true&hitsPerPage={hits_per_page}"
        }

        response = requests.post(URL, headers=HEADERS, data=json.dumps(payload))
        data = response.json()

        if "hits" in data:
            all_results.extend(data["hits"])

        # Verificar si hay más páginas
        if page >= data.get("nbPages", 1) - 1:
            break

        page += 1

    return all_results

def extract_basic_data(results):
    """
    Extrae datos básicos de los centros, incluyendo especialidades y cursos.
    """
    extracted_data = []

    for item in results:
        data = item.get("data", {})
        especialidades = []
        cursos = []

        # Obtener especialidades y cursos
        for especialitat in item.get("especialitat", []):
            especialidades.append(f"{especialitat['codi']} - {especialitat['desc']['cas']}")  # Código + Nombre

            # Extraer cursos de la especialidad
            for curso in especialitat.get("cursos", []):
                cursos.append(f"{curso['codi']} - {curso['desc']['cas']} ({curso['hores']}h)")


        extracted_data.append({
            "ID Centro": data.get("idCentre", ""),
            "Entidad": data.get("raoSocial", ""),
            "CIF": data.get("cif", ""),
            "Código Centro": data.get("codiCentre", ""),
            "Email": data.get("email", ""),
            "Teléfono": data.get("telefon", ""),
            "Dirección": data.get("carrer", ""),
            "Municipio": data.get("municipi", ""),
            "Provincia": data.get("provincia", ""),
            "Código Postal": data.get("cp", ""),
            "Web": data.get("web", ""),
            "Número de Cursos": data.get("numCursos", 0),
            "Es CIFO": data.get("esCifo", "N"),
            "Para Discapacitados": data.get("perDiscapacitats", "N"),
            "Especialidades": ";\n".join(especialidades),  # Especialidades separadas por ";"
            "Cursos": ";\n".join(cursos)  # Cursos separados por ";"
        })

    return extracted_data


def save_to_csv(data, filename="centros_filtrados.csv"):
    """
    Guarda los datos extraídos en un archivo CSV.
    """
    if not data:
        print("No hay datos para guardar.")
        return

    fieldnames = data[0].keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Datos guardados en '{filename}'")


def main():
    """
    Ejecuta el proceso completo de extracción y guardado de datos.
    """
    print("📡 Obteniendo datos de Algolia...")
    results = fetch_data_from_algolia(CENTRE_IDS)

    print(f"📊 Se han obtenido {len(results)} registros.")
    
    print("🔍 Extrayendo datos básicos...")
    extracted_data = extract_basic_data(results)

    print(f"💾 Guardando datos en CSV...")
    save_to_csv(extracted_data)

    print("✅ Proceso completado.")


if __name__ == "__main__":
    main()
