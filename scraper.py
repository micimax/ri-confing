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
# 2. SCRAPER FILM (CINEBLOG01)
# ==========================================
movies = []
url_sito_film = "https://cineblog01.delivery/film/"

try:
    # Intestazioni finte per far credere al sito che siamo un browser umano (Chrome)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, come Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://www.google.com/'
    }
    req = urllib.request.Request(url_sito_film, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8', errors='ignore')

        # Ricerca della "Serratura": Link, Locandina e Titolo nella grafica attuale di Cineblog
        blocchi = re.findall(r'<a href="([^"]+)".*?<img.*?src="([^"]+)".*?alt="([^"]+)"', html, re.IGNORECASE | re.DOTALL)
        
        visti = set()
        for link, img, titolo in blocchi:
            # Assicuriamoci che sia un link valido
            if link.startswith("http") and link not in visti:
                visti.add(link)
                movies.append({
                    "titolo": titolo.strip().replace(" streaming", ""),
                    "categoria": "Film - Cineblog01",
                    "locandina": img,
                    "url_video": link
                })
                if len(movies) >= 15: # Ci fermiamo a 15 film per non sovraccaricare il sistema
                    break

    print(f"Scraping Cineblog completato! Trovati {len(movies)} film.")

except Exception as e:
    print(f"Errore durante lo scraping di Cineblog: {e}")

# ==========================================
# FALLBACK: SE IL SITO CI BLOCCA
# ==========================================
if len(movies) == 0:
    movies = [
        {
            "titolo": "Cineblog ha bloccato il bot (Cloudflare)",
            "categoria": "Errore",
            "locandina": "https://via.placeholder.com/300x450.png?text=Blocco+Sito",
            "url_video": "https://www.w3schools.com/html/mov_bbb.mp4"
        }
    ]

with open("film.json", "w", encoding="utf-8") as f:
    json.dump({"catalogo": movies}, f, indent=4, ensure_ascii=False)
print("File film.json salvato con successo!")
