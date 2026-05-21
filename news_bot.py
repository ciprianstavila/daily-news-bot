import os
import requests
from datetime import datetime, timedelta

# Curățăm cheia API de eventuale spații invizibile luate la copy-paste
API_KEY = os.environ.get("NEWS_API_KEY", "").strip()

zile_in_urma = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
data_azi = datetime.now().strftime('%Y-%m-%d')
nume_fisier = f"stiri-{data_azi}.md"

def obtine_stiri(interogare, categorie_nume):
    numar_articole = 0
    text_stiri = f"### 📰 {categorie_nume}\n\n"
    
    url = f"https://newsapi.org/v2/everything?q={interogare}&from={zile_in_urma}&sortBy=popularity&apiKey={API_KEY}"
    
    # CRUCIAL PENTRU GITHUB: Adăugăm un User-Agent ca NewsAPI să nu blocheze serverul de Cloud
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        raspuns_raw = requests.get(url, headers=headers)
        raspuns = raspuns_raw.json()
        
        # Dacă API-ul ne dă o eroare specifică (ex: cheie greșită), o scriem în fișier ca să o vedem
        if raspuns.get("status") == "error":
            return f"### 📰 {categorie_nume}\n\n⚠️ *Eroare API: {raspuns.get('message', 'Eroare necunoscută')}*\n\n"
            
        if "articles" in raspuns and len(raspuns["articles"]) > 0:
            for articol in raspuns["articles"]:
                if numar_articole >= 4:
                    break
                    
                titlu = articol.get("title")
                sursa = articol.get("source", {}).get("name", "Unknown")
                link = articol.get("url")
                descriere = articol.get("description")
                
                if titlu and titlu != "[Removed]" and descriere and descriere != "[Removed]":
                    text_stiri += f"- **[{titlu}]({link})** *({sursa})*\n"
                    text_stiri += f"  {descriere}\n\n"
                    numar_articole += 1
    except Exception as e:
        return f"### 📰 {categorie_nume}\n\n⚠️ *Eroare conexiune: {str(e)}*\n\n"
    
    if numar_articole == 0:
        text_stiri += "- Nu s-au găsit știri importante în acest moment.\n\n"
        
    return text_stiri

continut_md = f"# ☕ Rezumatul tău Global de Știri - {datetime.now().strftime('%d %B %Y')}\n"
continut_md += "*Generat automat de robotul tău personal.*\n\n---\n\n"

# Interogări globale clare
continut_md += obtine_stiri("apple OR nvidia OR google", "Tech / Tehnologie & Hardware")
continut_md += obtine_stiri("bitcoin OR crypto OR fed", "Economie, Business & Crypto")
continut_md += obtine_stiri("chatgpt OR openai OR ai", "Inteligență Artificială (IA)")

with open(nume_fisier, "w", encoding="utf-8") as f:
    f.write(continut_md)

print("Proces finalizat.")
