import urllib.request
import json

# 1. SCARICA LA LISTA LIVE (M3U) AGGIRANDO I BLOCCHI
m3u_url = "https://forgejo.it/peppenamir/iptv_italia/raw/branch/main/lista.m3u"
try:
    req = urllib.request.Request(m3u_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req) as response:
        m3u_data = response.read().decode('utf-8')
    
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_data)
    print("Lista Live (M3U) salvata con successo!")
except Exception as e:
    print(f"Errore scaricamento Live: {e}")

# 2. CREA IL CATALOGO FILM
# (Questo è un catalogo di base pronto, lo espanderemo se funziona)
film_data = {
    "catalogo": [
        {
            "titolo": "Film di Test per la TV",
            "categoria": "Film",
            "locandina": "https://via.placeholder.com/300x450.png?text=Test+Film",
            "url_video": "https://www.w3schools.com/html/mov_bbb.mp4"
        }
    ]
}

with open("film.json", "w", encoding="utf-8") as f:
    json.dump(film_data, f, indent=4)
print("Catalogo Film creato con successo!")
