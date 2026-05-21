import os
import requests
from datetime import datetime, timedelta

API_KEY = os.environ.get("NEWS_API_KEY")

# Mergem pe ultimele 3 zile pentru volum maxim de date
zile_in_urma = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
data_azi = datetime.now().strftime('%Y-%m-%d')
nume_fisier = f"stiri-{data_azi}.md"

def obtine_stiri(interogare, categorie_nume):
    # Schimbare critică: Căutăm global (fără language=ro restrictionat) și sortăm după popularitate
    url = f"https://newsapi.org/v2/everything?q={interogare}&from={zile_in_urma}&sortBy=popularity&apiKey={API_KEY}"
    raspuns = requests.get(url).json()
    
    text_stiri = f"### 📰 {categorie_nume}\n\n"
    
    if "articles" in raspuns and len(raspuns["articles"]) > 0:
        numar_articole = 0
        for articol in raspuns["articles"]:
            if numar_articole >= 4:  # Ne oprim la top 4 articole relevante
                break
                
            titlu = articol["title"]
            sursa = articol["source"]["name"]
            link = articol["url"]
            descriere = articol["description"]
            
            # Filtrăm erorile sau articolele șterse din baza lor de date
            if titlu and titlu != "[Removed]" and descriere and descriere != "[Removed]":
                text_stiri += f"- **[{titlu}]({link})** *({sursa})*\n"
                text_stiri += f"  {descriere}\n\n"
                numar_articole += 1
    
    if numar_articole == 0:
        text_stiri += "- Nu s-au găsit știri importante în acest moment.\n\n"
    
    return text_stiri

# Construim conținutul fișierului Markdown
continut_md = f"# ☕ Rezumatul tău Global de Știri - {datetime.now().strftime('%d %B %Y')}\n"
continut_md += "*Generat automat de robotul tău personal.*\n\n---\n\n"

# Interogări optimizate pe cele mai fierbinți subiecte din ultimele ore
continut_md += obtine_stiri("romania OR bucharest", "Generale & România (Global Perspective)")
continut_md += obtine_stiri("technology OR gadget OR nvidia OR apple", "Tech / Tehnologie & Hardware")
continut_md += obtine_stiri("economy OR stocks OR crypto OR bitcoin", "Economie, Business & Crypto")
continut_md += obtine_stiri('"artificial intelligence" OR ChatGPT OR OpenAI OR "AI bot"', "Inteligență Artificială (IA)")

with open(nume_fisier, "w", encoding="utf-8") as f:
    f.write(continut_md)

print(f"Fișierul {nume_fisier} a fost populat cu fluxul global!")
