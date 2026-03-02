import sqlite3

DB_PATH = 'database.db'

def get_db():
    """Establece la conexión y configura el factory para devolver diccionarios."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa las tablas y carga los datos semilla (Seeders)."""
    with get_db() as db:
        # 1. Tabla de Categorías (necesaria para el protocolo Xtream)
        db.execute('''CREATE TABLE IF NOT EXISTS categories 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
        
        # 2. Tabla de Canales (Streams)
        db.execute('''CREATE TABLE IF NOT EXISTS streams 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name TEXT, 
                       target_url TEXT, 
                       category_id INTEGER)''')
        
        # 3. Tabla de Usuarios (Clientes para la API de Smarters)
        db.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       username TEXT, 
                       password TEXT)''')
        
        # Datos iniciales para pruebas (Solo se insertan si no existen)
        if not db.execute('SELECT * FROM categories WHERE id=1').fetchone():
            db.execute('INSERT INTO categories (id, name) VALUES (1, "Deportes")')
        
        if not db.execute('SELECT * FROM users WHERE username="lucas"').fetchone():
            db.execute('INSERT INTO users (username, password) VALUES ("lucas", "1234")')
            
        db.commit()

def fetch_all(query, params=()):
    """Ejecuta una consulta y devuelve todas las filas como una lista de diccionarios."""
    with get_db() as db:
        rows = db.execute(query, params).fetchall()
        return [dict(row) for row in rows]

def fetch_one(query, params=()):
    """Ejecuta una consulta y devuelve una sola fila como diccionario."""
    with get_db() as db:
        row = db.execute(query, params).fetchone()
        return dict(row) if row else None

def execute_query(query, params=()):
    """Ejecuta una operación de escritura (INSERT, UPDATE, DELETE)."""
    with get_db() as db:
        db.execute(query, params)
        db.commit()