import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://www.tarjetarojatv.blog/'
}

def get_live_events():
    url = "https://www.tarjetarojatv.blog/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        eventos = []
        # Buscamos los bloques de partidos segun el HTML que me pasaste
        menu_items = soup.select('ul.menu > li')
        for item in menu_items:
            main_link = item.find('a', recursive=False)
            if not main_link: continue
            
            full_text = main_link.get_text(strip=True)
            hora_tag = main_link.find('span', class_='t')
            hora = hora_tag.get_text(strip=True) if hora_tag else "LIVE"
            title = full_text.replace(hora, "").strip()

            canales = []
            options = item.select('ul li a')
            for opt in options:
                canal_url = opt['href']
                # Si el link es relativo, lo completamos
                if canal_url.startswith('/'): canal_url = "https://www.tarjetarojatv.blog" + canal_url
                canales.append({'name': opt.get_text(strip=True), 'url': canal_url})
            
            if canales:
                eventos.append({'time': hora, 'title': title, 'options': canales})
        return eventos
    except: return []

def resolve_stream(canal_url):
    """Extrae únicamente la URL del iFrame para mostrarlo en nuestra app limpia."""
    print(f"[*] Buscando iFrame en: {canal_url}")
    try:
        r = requests.get(canal_url, headers=HEADERS, timeout=10)
        # Buscamos el src del iframe oficial (CapoPlay, etc)
        iframe_match = re.search(r'<iframe.*?src=["\'](.*?)["\']', r.text)
        
        if iframe_match:
            target_url = iframe_match.group(1)
            if target_url.startswith('//'): target_url = 'https:' + target_url
            print(f"[SUCCESS] iFrame encontrado: {target_url}")
            return target_url
            
        return None
    except Exception as e:
        print(f"[!] Error: {e}")
        return None