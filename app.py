from flask import Flask, render_template, request
import scraper

app = Flask(__name__)

@app.route('/')
def index():
    print("[*] Cargando agenda desde scraper...")
    eventos = scraper.get_live_events()
    return render_template('index.html', eventos=eventos)

@app.route('/watch')
def watch():
    canal_url = request.args.get('url')
    title = request.args.get('title', 'Evento en Vivo')

    if not canal_url:
        print("[!] ERROR: Se recibió una petición /watch sin URL")
        return "URL no válida", 400

    print(f"[*] Resolviendo stream para: {title}")
    print(f"[*] URL a procesar: {canal_url}")

    stream_url = scraper.resolve_stream(canal_url)

    if stream_url:
        return render_template('player.html', stream_url=stream_url, title=title)
    else:
        return f"<h3>No se encontró stream.</h3><p>Probá con otra opción de canal.</p><a href='/'>Volver</a>", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
