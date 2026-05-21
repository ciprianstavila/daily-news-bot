import os
import requests
from datetime import datetime, timedelta

# Preluăm cheia API curată
API_KEY = os.environ.get("NEWS_API_KEY", "").strip()

# Setăm fereastra de timp pe ultimele 3 zile pentru volum maxim de știri
zile_in_urma = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
data_azi = datetime.now().strftime('%Y-%m-%d')
nume_fisier = f"stiri-{data_azi}.md"

def obtine_stiri(interogare, categorie_nume, limba=None):
    numar_articole = 0
    text_stiri = f"## 📰 {categorie_nume}\n\n"
    
    # Construim URL-ul în funcție de limbă (dacă e specificată)
    url = f"https://newsapi.org/v2/everything?q={interogare}&from={zile_in_urma}&sortBy=popularity&apiKey={API_KEY}"
    if limba:
        url += f"&language={limba}"
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        raspuns_raw = requests.get(url, headers=headers)
        raspuns = raspuns_raw.json()
        
        if raspuns.get("status") == "error":
            return f"## 📰 {categorie_nume}\n\n⚠️ *Eroare API: {raspuns.get('message')}*\n\n"
            
        if "articles" in raspuns and len(raspuns["articles"]) > 0:
            for articol in raspuns["articles"]:
                if numar_articole >= 7:  # Îți pune top 7 știri pe categorie ca să fie un rezumat consistent
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
        return f"## 📰 {categorie_nume}\n\n⚠️ *Eroare conexiune: {str(e)}*\n\n"
    
    if numar_articole == 0:
        text_stiri += "- Nu s-au găsit știri importante în acest moment.\n\n"
        
    return text_stiri

# Construim conținutul fișierului ziarului digital
continut_md = f"# ☕ Briefing Zilnic de Știri - {datetime.now().strftime('%d %B %Y')}\n"
continut_md += "*Automatizat și livrat în fiecare dimineață pe PC-ul tău.*\n\n---\n\n"

# 1. Categoria România (căutare în surse românești cu cuvinte cheie generale)
continut_md += obtine_stiri("romania OR bucuresti OR stiri", "Știri din România", limba="ro")

continut_md += "---\n\n" # Linie de separare între categorii

# 2. Categoria Internațional (căutare globală pe subiecte majore de actualitate)
continut_md += obtine_stiri("world OR breaking OR technology OR economy", "Știri Internaționale")

with open(nume_fisier, "w", encoding="utf-8") as f:
    f.write(continut_md)

print("Actualizare finalizată cu succes!")
