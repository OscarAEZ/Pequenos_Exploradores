
"""Configuración y apertura de conexiones con MySQL."""

import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


# Ruta principal del proyecto
RUTA_PROYECTO = Path(__file__).resolve().parents[2]

# Cargar las credenciales desde .env
RUTA_ENV = RUTA_PROYECTO / ".env"
load_dotenv(RUTA_ENV)


def obtener_conexion():
    """Abre una conexión nueva con la base de datos."""

    host = os.getenv("DB_HOST", "127.0.0.1").strip()
    puerto = os.getenv("DB_PORT", "3306").strip()
    usuario = os.getenv("DB_USER", "root").strip()
    contrasena = os.getenv("DB_PASSWORD", "")
    base_datos = os.getenv(
        "DB_NAME", "pequenos_exploradores"
    ).strip()

    if not host or not usuario or not base_datos:
        raise ValueError(
            "Faltan datos de conexión. Revisa el archivo .env."
        )

    try:
        puerto = int(puerto)
    except (TypeError, ValueError) as error:
        raise ValueError(
            "DB_PORT debe contener un puerto válido."
        ) from error

    return mysql.connector.connect(
        host=host,
        port=puerto,
        user=usuario,
        password=contrasena,
        database=base_datos,
        connection_timeout=5,
        charset="utf8mb4",
        use_unicode=True
    )


def probar_conexion():
    """Comprueba si MySQL responde correctamente."""

    conexion = None

    try:
        conexion = obtener_conexion()
        return conexion.is_connected()

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()

