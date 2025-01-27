import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# 🔹 Recupero le variabili d'ambiente (che configureremo su GitHub)
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = "INSERISCI_IL_TUO_DATABASE_ID"
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")

# 🔹 Configurazione Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(GOOGLE_SHEETS_CREDENTIALS), scope)
client = gspread.authorize(creds)
sheet = client.open("INSERISCI_NOME_DEL_FOGLIO").sheet1  # Nome del foglio Google Sheets

# 🔹 Funzione per ottenere dati da Notion
def get_notion_data():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# 🔹 Estrarre i dati da Notion
def parse_notion_data(data):
    rows = []
    for result in data["results"]:
        properties = result["properties"]
        row = [
            properties["Nome"]["title"][0]["text"]["content"] if properties["Nome"]["title"] else "",
            properties["Data"]["date"]["start"] if "date" in properties["Data"] else "",
            properties["Note"]["rich_text"][0]["text"]["content"] if properties["Note"]["rich_text"] else "",
        ]
        rows.append(row)
    return rows

# 🔹 Scrivere i dati su Google Sheets
def update_google_sheets(rows):
    sheet.clear()
    sheet.append_row(["Nome", "Data", "Note"])
    for row in rows:
        sheet.append_row(row)
    print("✅ Dati aggiornati con successo su Google Sheets!")

# 🔹 Eseguire il processo
if __name__ == "__main__":
    notion_data = get_notion_data()
    rows = parse_notion_data(notion_data)
    update_google_sheets(rows)
