import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect('analytixa.db')

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()
    # Creamos una tabla para las auditorías
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auditorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            account_id TEXT,
            nombre_campana TEXT,
            metricas_json TEXT,
            reporte_texto TEXT
        )
    ''')
    conn.commit()
    conn.close()

def guardar_auditoria(account_id, nombre_campana, metricas, reporte):
    conn = conectar()
    cursor = conn.cursor()
    fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO auditorias (fecha, account_id, nombre_campana, metricas_json, reporte_texto)
        VALUES (?, ?, ?, ?, ?)
    ''', (fecha_hoy, account_id, nombre_campana, str(metricas), reporte))
    conn.commit()
    conn.close()

# ESTA ES LA FUNCIÓN QUE TENÍA EL ERROR DE INDENTACIÓN
def obtener_todas_las_auditorias():
    conn = conectar()
    cursor = conn.cursor()
    # Traemos las auditorías ordenadas por la más reciente
    cursor.execute('SELECT id, fecha, account_id, nombre_campana, reporte_texto FROM auditorias ORDER BY id DESC')
    filas = cursor.fetchall()
    conn.close()
    return filas

# El bloque __main__ debe ir al final y solo para tareas de mantenimiento
if __name__ == "__main__":
    crear_tablas()
    print("✅ Base de datos Analytixa preparada.")