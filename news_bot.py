import os
import requests
from datetime import datetime, timedelta

# Preluăm cheia API
API_KEY = os.environ.get("NEWS_API_KEY")

# REZOLVARE: Schimbăm de la 1 zi la 3 zile în urmă pentru a avea rezultate stabile în RO
zile_in_urma = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
data_azi = datetime.now().strftime('%Y-%m-%d')
nume_fisier = f"stiri-{data_azi}.md"

def obtine_stiri(interogare, categorie_nume):
    # Folosim sortare după data publicării (publishedAt) sau relevanță ca să prindem cele mai proaspete știri
    url = f"https://newsapi.org/v2/everything?q={interogare}&from={zile_in_urma}&sortBy=publishedAt&language=ro&apiKey={API_KEY}"
    raspuns = requests.get(url).json()
    
    text_stiri = f"### 📰 {categorie_nume}\n\n"
    
    if "articles" in raspuns and len(raspuns["articles"]) > 0:
        # Luăm top 4 articole
        for articol in raspuns["articles"][:4]:
            titlu = articol["title"]
            sursa = articol["source"]["name"]
            link = articol["url"]
            descriere = articol["description"] if articol["description"] else "Fără descriere disponibilă."
            
            # Curățăm titlurile care vin uneori șterse sau goale de la surse defecte
            if titlu and titlu != "[Removed]":
                text_stiri += f"- **[{titlu}]({link})** *({sursa})*\n"
                text_stiri += f"  {descriere}\n\n"
    else:
        text_stiri += "- Nu s-au găsit știri importante în ultimele zile.\n\n"
    
    return text_stiri

# Construim conținutul fișierului
continut_md = f"# ☕ Rezumatul tău de știri - {datetime.now().strftime('%d %B %Y')}\n"
continut_md += "*Generat automat în fiecare dimineață.*\n\n---\n\n"

# Optimizăm interogările (folosim cuvinte mai generale acceptate mai ușor de motorul lor de căutare)
continut_md += obtine_stiri("romania OR bucuresti", "Generale România")
continut_md += obtine_stiri("tehnologie OR „it” OR smartphone OR science", "Tech / Tehnologie")
continut_md += obtine_stiri("economie OR bani OR afaceri OR euro", "Economie & Business")
continut_md += obtine_stiri("artificiala OR ChatGPT OR AI OR inteligență", "Inteligență Artificială (IA)")

with open(nume_fisier, "w", encoding="utf-8") as f:
    f.write(continut_md)

print(f"Fișierul {nume_fisier} a fost actualizat!")
