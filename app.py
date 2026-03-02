from flask import Flask
from database import init_db
from routes_admin import admin_bp
from routes_api import api_bp

app = Flask(__name__)

# Registrar Blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    init_db()
    print("[*] Xtream-Lite Iniciado. Host: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)