import urllib.request
import json
import re

print("Avvio aggiornamento Liste e Film...")

# ==========================================
# 1. AGGIORNAMENTO CANALI IN DIRETTA (M3U)
# ==========================================
url_canali = "https://raw.githubusercontent.com/Tundrak/IPTV-Italia/main/iptv-italia.m3u"
try:
    req = urllib.request.Request(url_canali, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        with open("lista.m3u", "wb") as f:
            f.write(response.read())
    print("Canali TV aggiornati con successo!")
except Exception as e:
    print(f"Errore download canali TV: {e}")

# ==========================================
# 2. SCRAPER FILM (AltaDefinizione / Cineblog)
# ==========================================
movies = []

# Sostituisci questo URL con il dominio attuale del sito che vuoi analizzare
url_sito_film = "https://altadefinizione.click/" # Esempio

try:
    req = urllib.request.Request(url_sito_film, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8', errors='ignore')

        # --- LOGICA DI ESTRAZIONE ---
        # Qui cerchiamo nel codice della pagina i titoli. 
        # (Questo è un parametro generico, andrà adattato all'HTML del sito reale)
        titoli_trovati = re.findall(r'<a href="(.*?)" class="title">(.*?)</a>', html)

        for link, titolo in titoli_trovati[:10]: # Prende i primi 10 per fare un test
            movies.append({
                "titolo": titolo.strip(),
                "categoria": "Film Estratti",
                "locandina": "https://via.placeholder.com/300x450.png?text=Locandina",
                "url_video": link 
            })
    print(f"Scraping completato! Trovati {len(movies)} film.")

except Exception as e:
    print(f"Errore durante lo scraping: {e}")

# Se il sito blocca la connessione, crea un finto film per evitare crash sulla TV
if len(movies) == 0:
    movies = [
        {
            "titolo": "Attesa Estrazione Film",
            "categoria": "Test",
            "locandina": "https://via.placeholder.com/300x450.png?text=Sistema+Attivo",
            "url_video": "https://www.w3schools.com/html/mov_bbb.mp4"
        }
    ]

# Salva tutto nel file per la TV
with open("film.json", "w", encoding="utf-8") as f:
    json.dump({"catalogo": movies}, f, indent=4, ensure_ascii=False)
print("File film.json salvato!")
