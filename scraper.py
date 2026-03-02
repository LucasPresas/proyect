import requests
import re
from urllib.parse import urljoin

def robust_scraper_multi(url_base):
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    results = []
    
    try:
        r = session.get(url_base, headers=headers, timeout=10)
        candidatos = re.findall(r'src=["\'](.*?)["\']|href=["\'](.*?)["\']', r.text)
        
        urls_a_probar = [url_base]
        for c in candidatos:
            link = c[0] if c[0] else c[1]
            if any(x in link for x in ['player', 'option', 'canal', 'embed', 'watch']):
                urls_a_probar.append(urljoin(url_base, link))
        
        for t in list(set(urls_a_probar)):
            try:
                res = session.get(t, headers={'Referer': url_base}, timeout=5)
                # Buscar m3u8
                matches = re.findall(r'["\'](https?://[^\s"\']+\.m3u8[^\s"\']*)["\']', res.text)
                for m in matches:
                    found = m.replace('\\/', '/')
                    if found not in results: results.append(found)
            except: continue
        return results
    except: return []