from datetime import datetime
import sqlite3


class BaseDatos:
    def __init__(self, nombre_bd="proyecto_bio.db"):
        self.nombre_bd = nombre_bd
        self.crear_tablas()

    def conectar(self):
        return sqlite3.connect(self.nombre_bd)

    def crear_tablas(self):
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE,
                password TEXT,
                nombre TEXT,
                rol TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ingresos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                nombre TEXT,
                rol TEXT,
                fecha TEXT,
                hora TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS imagenes_dicom (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente TEXT,
                modalidad TEXT,
                filas INTEGER,
                columnas INTEGER,
                voxel_alto REAL,
                voxel_ancho REAL,
                voxel_largo REAL,
                dimensiones TEXT
            )
        """)
        # Usuarios iniciales de prueba
        cur.execute("""
            INSERT OR IGNORE INTO usuarios (usuario, password, nombre, rol)
            VALUES ('img', '123', 'Usuario Imagenes', 'imagenes')
        """)
        cur.execute("""
            INSERT OR IGNORE INTO usuarios (usuario, password, nombre, rol)
            VALUES ('sen', '123', 'Usuario Senales', 'senales')
        """)
        conn.commit()
        conn.close()

    def validar_usuario(self, usuario, password):
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nombre, rol FROM usuarios
            WHERE usuario = ? AND password = ?
        """, (usuario, password))
        fila = cur.fetchone()

        if fila is None:
            conn.close()
            return None

        uid, nombre, rol = fila
        ahora = datetime.now()
        fecha = ahora.strftime("%Y-%m-%d")
        hora = ahora.strftime("%H:%M:%S")

        cur.execute("""
            INSERT INTO ingresos (usuario_id, nombre, rol, fecha, hora)
            VALUES (?, ?, ?, ?, ?)
        """, (uid, nombre, rol, fecha, hora))
        conn.commit()
        conn.close()

        return {
            "id": uid,
            "nombre": nombre,
            "rol": rol,
            "fecha": fecha,
            "hora": hora,
        }

    def guardar_dicom(self, datos):
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO imagenes_dicom (
                paciente, modalidad, filas, columnas,
                voxel_alto, voxel_ancho, voxel_largo, dimensiones
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datos.get("paciente", ""),
            datos.get("modalidad", ""),
            datos.get("filas", 0),
            datos.get("columnas", 0),
            datos.get("voxel_alto", 0.0),
            datos.get("voxel_ancho", 0.0),
            datos.get("voxel_largo", 0.0),
            str(datos.get("dimensiones", "")),
        ))
        conn.commit()
        conn.close()