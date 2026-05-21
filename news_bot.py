import os
import requests
from datetime import datetime, timedelta

API_KEY = os.environ.get("NEWS_API_KEY", "").strip()

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
                    html_stiri += f"<div class='news-card'>"
                    html_stiri += f"<h3>{titlu}</h3>"
                    html_stiri += f"<span class='source'>📍 {sursa}</span>"
                    html_stiri += f"<p>{descriere}</p>"
                    html_stiri += f"<a href='{link}' target='_blank' class='read-btn'>Citește articolul →</a>"
                    html_stiri += f"</div>"
                    numar_articole += 1
    except Exception as e:
        return f"<div class='error'>Eroare conexiune: {str(e)}</div>"
    
    if numar_articole == 0:
        html_stiri += "<p>Nu s-au găsit știri proaspete în acest moment.</p>"
        
    html_stiri += "</div></div>"
    return html_stiri

# Construim header-ul paginii puf cu puf folosind string-uri simple, sigure
html_antet = "<!DOCTYPE html>\n<html lang='ro'>\n<head>\n<meta charset='UTF-8'>\n"
html_antet += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
html_antet += "<title>Ziarul Meu Personal</title>\n<style>\n"
html_antet += "body { font-family: 'Segoe UI', sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 20px; display: none; }\n"
html_antet += ".container { max-width: 1100px; margin: 0 auto; }\n"
html_antet += "header { text-align: center; padding: 30px 0; border-bottom: 3px solid #3498db; margin-bottom: 30px; }\n"
html_antet += "h1 { margin: 0; color: #2c3e50; font-size: 2.5rem; }\n"
html_antet += ".date { color: #7f8c8d; margin-top: 5px; font-style: italic;
