import requests
import json, time
from bs4 import BeautifulSoup
from typing import List


json_result = []


def get_data(url: str) -> List[str]:
    res = requests.get(url, timeout=5) 
    soup = BeautifulSoup(res.text, "html.parser")
    data = soup.find_all("td")
    return data

def extact_name(data: List[str]) -> str:
    return data[0].td.text

def extract_adress(data: List[str]) -> str:
    for td in data:
        if "Adreça" in td.text:
            address_parts = td.decode_contents().split("<br/>")
            address = " ".join(part.strip() for part in address_parts if "Adreça" not in part and "Veure a Google Maps" not in part)
            return address.strip()
    return "Address not found"

def get_info_table(data):
    for td in data:
        table = td.find("table")
        if table:
            return table.find_all("tr")
    return None

def get_tr_by_label(rows, label: str):
    for tr in rows:
        tds = tr.find_all("td")
        if len(tds) >= 2 and label in tds[0].text:
            return tr
    return None

def extract_email(data: List[str]) -> str:
    return extract_field_by_label(get_info_table(data), "E-mail")

def extract_field_by_label(rows, label: str) -> str:
    for tr in rows:
        tds = tr.find_all("td")
        if len(tds) >= 2 and label in tds[0].text:
            second_td = tds[1]
            # Si hay un <a>, lo usamos; si no, devolvemos el texto plano
            return second_td.get_text(strip=True)
    return f"{label} not found"

def extract_web(data: List[str]) -> str:
    try:
        link = data[17].find("a")
        if link and link.get("href"):
            return link.get("href").strip()
        return "No web found"
    except Exception as e:
        return "No web found"


def extract_horari(data: List[str]) -> str:
    try:
        horari = data[11].text.strip()
        if horari:
            return horari
        return "Sense horari especificat"
    except Exception as e:
        return "Sense horari especificat"

def escribir_cabecera():
    with open("entitats_juvenils.csv", "w", encoding="utf-8") as f:
        # Escribir encabezados
        f.write("id$Name$Adress$Categoria$Tipologia$Districte$Barri$Horari$Tel$Email$Web\n")

def convert_jsonToCsv(item):
    with open("entitats_juvenils.csv", "a", encoding="utf-8") as f:
        f.write(f"{item['id']}${item['Name']}${item['Adress']}${item['Categoria']}${item['Tipologia']}${item['Districte']}${item['Barri']}${item['Horari']}${item['Tel']}${item['Email']}${item['Web']}\n")


# escribir_cabecera()

for i in range(3000, 4000):
    url = "https://entitatsjuvenilsbcn.cat/cens_entitats/cens3.php?id=" + str(i)
    data = get_data(url)
    
    if len(data) == 0 or data[0].text == "No hi ha dades per aquest ID":
        print("No data found for ID:", i)
        time.sleep(1)
        continue

    if extact_name(data) == "":
        print("No name found for ID:", i)
        time.sleep(1)
        continue

    json_data = {
        "id": i,
        "Name": extact_name(data),
        "Adress": extract_adress(data),
        "Categoria": extract_field_by_label(get_info_table(data), "Categoria"),
        "Tipologia": extract_field_by_label(get_info_table(data), "Tipologia"),
        "Districte": extract_field_by_label(get_info_table(data), "Districte"),
        "Barri": extract_field_by_label(get_info_table(data), "Barri"),
        "Horari": extract_field_by_label(get_info_table(data), "Horari"),
        "Tel": extract_field_by_label(get_info_table(data), "Tel."),
        "Email": extract_email(data),
        "Web": extract_field_by_label(get_info_table(data), "Web"),
    }
    print(json_data)
    convert_jsonToCsv(json_data)
    time.sleep(1) # Pausa de 0.5 segons entre peticions

