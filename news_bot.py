import os
import requests
from datetime import datetime, timedelta

# Preluăm doar cheia API (nu mai avem nevoie de parole de mail)
API_KEY = os.environ.get("NEWS_API_KEY")

ieri = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
data_azi = datetime.now().strftime('%Y-%m-%d')
nume_fisier = f"stiri-{data_azi}.md"

def obtine_stiri(interogare, categorie_nume):
    url = f"https://newsapi.org/v2/everything?q={interogare}&from={ieri}&sortBy=popularity&language=ro&apiKey={API_KEY}"
    raspuns = requests.get(url).json()
    
    text_stiri = f"### 📰 {categorie_nume}\n\n"
    
    if "articles" in raspuns and len(raspuns["articles"]) > 0:
        for articol in raspuns["articles"][:4]: # Luăm top 4 știri
            titlu = articol["title"]
            sursa = articol["source"]["name"]
            link = articol["url"]
            descriere = articol["description"] if articol["description"] else "Fără descriere disponibilă."
            
            text_stiri += f"- **[{titlu}]({link})** *({sursa})*\n"
            text_stiri += f"  {descriere}\n\n"
    else:
        text_stiri += "- Nu s-au găsit știri importante în ultimele 24 de ore.\n\n"
    
    return text_stiri

# Construim conținutul fișierului
continut_md = f"# ☕ Rezumatul tău de știri - {datetime.now().strftime('%d %B %Y')}\n"
continut_md += "*Generat automat în fiecare dimineață.*\n\n---\n\n"

continut_md += obtine_stiri("romania OR stiri", "Generale România")
continut_md += obtine_stiri("tehnologie OR gadget OR „it”", "Tech / Tehnologie")
continut_md += obtine_stiri("economie OR bursa OR bani OR afaceri", "Economie & Business")
continut_md += obtine_stiri("„inteligență artificială” OR ChatGPT OR „AI”", "Inteligență Artificială (IA)")

# Salvăm textul într-un fișier local pe serverul GitHub (va fi urcat în repository de către flux)
with open(nume_fisier, "w", encoding="utf-8") as f:
    f.write(continut_md)

print(f"Fișierul {nume_fisier} a fost creat cu succes local!")
