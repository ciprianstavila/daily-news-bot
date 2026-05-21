import os
import requests
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Preluăm datele secrete din setările securizate ale GitHub (le configurăm la Pasul 3)
API_KEY = os.environ.get("NEWS_API_KEY")
EMAIL_EXPEDIATOR = os.environ.get("EMAIL_FROM")
EMAIL_PAROLA = os.environ.get("EMAIL_PASSWORD")
EMAIL_DESTINATAR = os.environ.get("EMAIL_TO")

ieri = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def obtine_stiri(interogare, categorie_nume):
    url = f"https://newsapi.org/v2/everything?q={interogare}&from={ieri}&sortBy=popularity&language=ro&apiKey={API_KEY}"
    raspuns = requests.get(url).json()
    structura_stiri = f"<h2>📰 Categoria: {categorie_nume}</h2><ul>"
    
    if "articles" in raspuns and len(raspuns["articles"]) > 0:
        for articol in raspuns["articles"][:3]:
            titlu = articol["title"]
            sursa = articol["source"]["name"]
            link = articol["url"]
            descriere = articol["description"] if articol["description"] else "Fără descriere disponibilă."
            structura_stiri += f"<li><a href='{link}'><b>{titlu}</b></a> <small>({sursa})</small><br>{descriere}</li>"
    else:
        structura_stiri += "<li>Nu s-au găsit știri importante în ultimele 24 de ore.</li>"
    
    structura_stiri += "</ul><hr style='border:0; border-top:1px solid #eee;'>"
    return structura_stiri

corp_email_html = "<html><body>"
corp_email_html += f"<h1>☕ Rezumatul tău de știri - {datetime.now().strftime('%d %B %Y')}</h1><br>"
corp_email_html += obtine_stiri("romania OR stiri", "Generale România")
corp_email_html += obtine_stiri("tehnologie OR gadget OR „it”", "Tech / Tehnologie")
corp_email_html += obtine_stiri("economie OR bursa OR bani OR afaceri", "Economie & Business")
corp_email_html += obtine_stiri("„inteligență artificială” OR ChatGPT OR „AI”", "Inteligență Artificială (IA)")
corp_email_html += "</body></html>"

msg = MIMEMultipart('alternative')
msg['Subject'] = f"📰 Briefing Zilnic: {datetime.now().strftime('%d/%m/%Y')}"
msg['From'] = EMAIL_EXPEDIATOR
msg['To'] = EMAIL_DESTINATAR
msg.attach(MIMEText(corp_email_html, 'html', 'utf-8'))

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_EXPEDIATOR, EMAIL_PAROLA)
    server.sendmail(EMAIL_EXPEDIATOR, EMAIL_DESTINATAR, msg.as_string())
    server.quit()
    print("Email trimis cu succes!")
except Exception as e:
    print(f"Eroare: {e}")
