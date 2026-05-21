import os
import requests
from datetime import datetime, timedelta

API_KEY = os.environ.get("NEWS_API_KEY", "").strip()

# Preluăm știri din ultimele 3 zile
zile_in_urma = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
data_azi = datetime.now().strftime('%Y-%m-%d')
nume_fisier = "index.html"
PAROLA_SECRETA = "Stiri2026"

def obtine_stiri(interogare, categorie_nume, limba=None):
    numar_articole = 0
    html_stiri = f"<div class='category-section'><h2>📰 {categorie_nume}</h2><div class='news-grid'>"
    
    url = f"https://newsapi.org/v2/everything?q={interogare}&from={zile_in_urma}&sortBy=popularity&apiKey={API_KEY}"
    if limba:
        url += f"&language={limba}"
        
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        raspuns = requests.get(url, headers=headers).json()
        if raspuns.get("status") == "error":
            return f"<div class='error'>Eroare API la {categorie_nume}: {raspuns.get('message')}</div>"
            
        if "articles" in raspuns and len(raspuns["articles"]) > 0:
            for articol in raspuns["articles"]:
                if numar_articole >= 6:
                    break
                titlu = articol.get("title")
                sursa = articol.get("source", {}).get("name", "Unknown")
                link = articol.get("url")
                descriere = articol.get("description")
                
                if titlu and titlu != "[Removed]" and descriere and descriere != "[Removed]":
                    html_stiri += f"""
                    <div class='news-card'>
                        <h3>{titlu}</h3>
                        <span class='source'>📍 {sursa}</span>
                        <p>{descriere}</p>
                        <a href='{link}' target='_blank' class='read-btn'>Citește articolul →</a>
                    </div>
                    """
                    numar_articole += 1
    except Exception as e:
        return f"<div class='error'>Eroare conexiune: {str(e)}</div>"
    
    if numar_articole == 0:
        html_stiri += "<p>Nu s-au găsit știri proaspete în acest moment.</p>"
        
    html_stiri += "</div></div>"
    return html_stiri

# Folosim un string normal, fără f în față, ca Python să ignore complet acoladele din CSS și JS
structura_baza = """<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ziarul Meu Personal</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 20px; display: none; }
        .container { max-width: 1100px; margin: 0 auto; }
        header { text-align: center; padding: 30px 0; border-bottom: 3px solid #3498db; margin-bottom: 30px; }
        h1 { margin: 0; color: #2c3e50; font-size: 2.5rem; }
        .date { color: #7f8c8d; margin-top: 5px; font-style: italic; }
        .category-section { margin-bottom: 40px; }
        h2 { color: #2c3e50; border-left: 5px solid #3498db; padding-left: 10px; margin-bottom: 20px; }
        .news-grid { display: block; }
        .news-card { background: white; padding: 20px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .news-card h3 { margin-top: 0; color: #2980b9; font-size: 1.3rem; }
        .source { font-size: 0.85rem; color: #e67e22; font-weight: bold; }
        .news-card p { color: #555; line-height: 1.5; font-size: 0.95rem; }
        .read-btn { display: inline-block; background-color: #3498db; color: white; padding: 8px 15px; text-decoration: none; border-radius: 4px; font-size: 0.9rem; font-weight: bold; }
        .read-btn:hover { background-color: #2980b9; }
        .error { background-color: #fde8e8; color: #e74c3c; padding: 15px; border-radius: 5px; }
    </style>
    <script>
        function verificaParola() {
            var parolaCorecta = "[PAROLA]";
            var incercare = prompt("🔒 Acest site este privat. Introdu parola pentru a citi știrile:");
            
            if (incercare === parolaCorecta) {
                document.documentElement.style.display = "block";
                document.body.style.display = "block";
            } else
