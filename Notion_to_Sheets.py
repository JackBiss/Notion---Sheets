name: Aggiornamento Notion a Google Sheets

on:
  schedule:
    - cron: '0 6 * * *'  # Esegue ogni giorno alle 6:00 UTC

jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.9'

      - name: Install Dependencies
        run: pip install requests gspread oauth2client pandas

      - name: Esegui lo script
        env:
          NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
          GOOGLE_SHEETS_CREDENTIALS: ${{ secrets.GOOGLE_SHEETS_CREDENTIALS }}
        run: python notion_to_sheets.py
