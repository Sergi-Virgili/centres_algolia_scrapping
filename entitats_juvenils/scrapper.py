import requests
import json, time
from bs4 import BeautifulSoup
from typing import List

# for i in range(1, 400):
#     url = "https://entitatsjuvenilsbcn.cat/cens_entitats/cens3.php?id=" + str(i)
#     print(url)

json_result = []
    
# url2 = "https://entitatsjuvenilsbcn.cat/cens_entitats/cens3.php?id=1"

def get_data(url: str) -> List[str]:
    res = requests.get(url, timeout=5)  # ⏱️ timeout de 5 segundos
    soup = BeautifulSoup(res.text, "html.parser")
    data = soup.find_all("td")
    return data


# data = get_data(url2)
# print(data)

def extact_name(data: List[str]) -> str:
    return data[0].td.text

def extract_adress(data: List[str]) -> str:
    for td in data:
        if "Adreça" in td.text:
            # Extraer el contenido después de "Adreça"
            address_parts = td.decode_contents().split("<br/>")
            address = " ".join(part.strip() for part in address_parts if "Adreça" not in part and "Veure a Google Maps" not in part)
            return address.strip()
    return "Address not found"

# for i in range(1, 20):
#     print(str(i) + " " + data[i].text)

# print(extact_name(data))
# print(extract_adress(data))
# print(data[4].text)


def extract_email(data: List[str]) -> str:
    try:
        link = data[15].find("a")
        if link and "mailto:" in link.get("href", ""):
            return link.text.strip()
        return "No email found"
    except Exception as e:
        return "No email found"

def extract_web(data: List[str]) -> str:
    try:
        link = data[17].find("a")
        if link and link.get("href"):
            return link.get("href").strip()
        return "No web found"
    except Exception as e:
        return "No web found"

def extract_telefon(data: List[str]) -> str:
    try:
        telefon = data[13].text.strip()
        if telefon:
            return telefon
        return "No phone found"
    except Exception as e:
        return "No phone found"
def extract_horari(data: List[str]) -> str:
    try:
        horari = data[11].text.strip()
        if horari:
            return horari
        return "Sense horari especificat"
    except Exception as e:
        return "Sense horari especificat"

for i in range(1, 400):
    url = "https://entitatsjuvenilsbcn.cat/cens_entitats/cens3.php?id=" + str(i)
    data = get_data(url)
    
    if len(data) == 0 or data[0].text == "No hi ha dades per aquest ID":
        print("No data found for ID:", i)
        continue

    json_data = {
        "id": i,
        "Name": extact_name(data),
        "Adress": extract_adress(data),
        # "Categoría": data[5].text,
        # "Tipologia": data[3].text,
        # "Districte": data[7].text,
        # "Barrio": data[9].text,
        "Horari": extract_horari(data),
        "Telèfon": extract_telefon(data),
        "Email": extract_email(data),
        "Web": extract_web(data),
    }
    print(json_data)
    json_result.append(json_data)
    time.sleep(1) # Pausa de 0.5 segons entre peticions

def convert_jsonToCsv(json_result):
    with open("entitats_juvenils.csv", "w", encoding="utf-8") as f:
        # Escribir encabezados
        f.write("id$Name$Adress$Horari$Telèfon$Email$Web\n")
        for item in json_result:
            f.write(f"{item['id']}${item['Name']}${item['Adress']}${item['Horari']}${item['Telèfon']}${item['Email']}${item['Web']}\n")

convert_jsonToCsv(json_result)