
import os
from pathlib import Path

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Cargar la configuración privada del proyecto
RUTA_ENV = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(RUTA_ENV)


def obtener_menores():
    conexion = None
    cursor = None

    try:
        # Datos de conexión obtenidos del archivo .env
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        cursor = conexion.cursor()

        # Consulta real a la tabla Menor
        cursor.execute(
            "SELECT idMenor, nombreCompleto "
            "FROM Menor ORDER BY idMenor"
        )

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()


def probar_conexion():
    print("Prueba de conexión - Pequeños Exploradores")

    try:
        menores = obtener_menores()

        print("\nConsulta ejecutada correctamente.")
        print(f"Menores registrados: {len(menores)}")

        for id_menor, nombre in menores:
            print(f"{id_menor} - {nombre}")

    except (Error, ValueError, TypeError) as error:
        print(f"Error al consultar MySQL: {error}")


if __name__ == "__main__":
    probar_conexion()
