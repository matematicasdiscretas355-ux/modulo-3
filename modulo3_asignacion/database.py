import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'smartroute_modulo3.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_bd():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Tabla de Vehiculos (RF-02)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                placa TEXT UNIQUE NOT NULL,
                cap_peso REAL NOT NULL,
                cap_vol REAL NOT NULL,
                estado TEXT DEFAULT 'Disponible'
            )
        ''')

        # 2. Tabla de Pedidos (RF-01)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id TEXT PRIMARY KEY,
                peso REAL NOT NULL,
                volumen REAL NOT NULL,
                zona TEXT NOT NULL,
                estado TEXT DEFAULT 'Pendiente',
                vehiculo_id INTEGER,
                FOREIGN KEY (vehiculo_id) REFERENCES vehiculos (id)
            )
        ''')

        # 3. Datos de prueba iniciales (incluye caso CP-03)
        cursor.execute("SELECT COUNT(*) FROM vehiculos")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO vehiculos (placa, cap_peso, cap_vol, estado) VALUES ('ABC-123', 500.0, 10.0, 'Disponible')")
            cursor.execute("INSERT INTO vehiculos (placa, cap_peso, cap_vol, estado) VALUES ('XYZ-789', 800.0, 15.0, 'Disponible')")

        cursor.execute("SELECT COUNT(*) FROM pedidos")
        if cursor.fetchone()[0] == 0:
            # 3 pedidos de 300kg para validar CP-03
            cursor.execute("INSERT INTO pedidos (id, peso, volumen, zona, estado) VALUES ('P-01', 300.0, 1.0, 'Norte', 'Pendiente')")
            cursor.execute("INSERT INTO pedidos (id, peso, volumen, zona, estado) VALUES ('P-02', 300.0, 1.0, 'Norte', 'Pendiente')")
            cursor.execute("INSERT INTO pedidos (id, peso, volumen, zona, estado) VALUES ('P-03', 300.0, 1.0, 'Norte', 'Pendiente')")
            # Pedidos adicionales para probar Criterio 2 (Zonas)
            cursor.execute("INSERT INTO pedidos (id, peso, volumen, zona, estado) VALUES ('P-04', 120.0, 1.5, 'Sur', 'Pendiente')")
            cursor.execute("INSERT INTO pedidos (id, peso, volumen, zona, estado) VALUES ('P-05', 180.0, 2.0, 'Sur', 'Pendiente')")
            cursor.execute("INSERT INTO pedidos (id, peso, volumen, zona, estado) VALUES ('P-06', 90.0, 0.8, 'Norte', 'Pendiente')")

        conn.commit()

if __name__ == '__main__':
    inicializar_bd()
    print("Base de datos de prueba local creada exitosamente.")