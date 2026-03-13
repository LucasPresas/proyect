import requests
from bs4 import BeautifulSoup
import re
import base64

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def get_live_events():
    url = "https://www.tarjetarojatv.blog/"
    try:
        # Usamos una sesión para mantener cookies si el sitio las requiere
        session = requests.Session()
        r = session.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        eventos = []
        
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
                if canal_url.startswith('/'): 
                    canal_url = "https://www.tarjetarojatv.blog" + canal_url
                canales.append({'name': opt.get_text(strip=True), 'url': canal_url})
            
            if canales:
                eventos.append({'time': hora, 'title': title, 'options': canales})
        return eventos
    except Exception as e: 
        print(f"Error en get_live_events: {e}")
        return []

def resolve_stream(canal_url):
    print(f"[*] Buscando iFrame en: {canal_url}")
    try:
        session = requests.Session()
        # Importante: Algunos sitios validan que el Referer sea su propia home
        headers = HEADERS.copy()
        headers['Referer'] = 'https://www.tarjetarojatv.blog/'
        
        r = session.get(canal_url, headers=headers, timeout=10)
        
        # Buscamos el src del iframe
        iframe_match = re.search(r'<iframe.*?src=["\'](.*?)["\']', r.text)
        
        if iframe_match:
            target_url = iframe_match.group(1)
            if target_url.startswith('//'): target_url = 'https:' + target_url
            
            # Si el link del iframe apunta a otro scrapper/player (ej. CapoPlay)
            # a veces es mejor devolver el link base para que el sandbox haga el resto
            print(f"[SUCCESS] iFrame encontrado: {target_url}")
            return target_url
            
        return None
    except Exception as e:
        print(f"[!] Error: {e}")
        return None