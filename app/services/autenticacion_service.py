"""Autenticación de usuarios y control básico de roles."""

import hashlib
import hmac
import secrets

from app.database.conexion import obtener_conexion


ITERACIONES = 310_000


def _crear_hash(contrasena):
    """Genera un hash PBKDF2 con sal aleatoria."""
    sal = secrets.token_hex(16)
    derivado = hashlib.pbkdf2_hmac(
        "sha256",
        contrasena.encode("utf-8"),
        bytes.fromhex(sal),
        ITERACIONES
    ).hex()

    return f"pbkdf2_sha256${ITERACIONES}${sal}${derivado}"


def _verificar_hash(contrasena, hash_guardado):
    """Comprueba una contraseña sin almacenar texto plano."""
    try:
        algoritmo, iteraciones, sal, esperado = hash_guardado.split("$")
        if algoritmo != "pbkdf2_sha256":
            return False

        calculado = hashlib.pbkdf2_hmac(
            "sha256",
            contrasena.encode("utf-8"),
            bytes.fromhex(sal),
            int(iteraciones)
        ).hex()

        return hmac.compare_digest(calculado, esperado)

    except (ValueError, TypeError):
        return False


def autenticar_usuario(nombre_usuario, contrasena):
    """Devuelve los datos del usuario autenticado o None si no coincide."""
    nombre_usuario = (nombre_usuario or "").strip()

    if not nombre_usuario or not contrasena:
        return None

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                u.idUsuario,
                u.nombreUsuario,
                u.passwordHash,
                u.rol,
                u.idRecepcionista,
                u.idEducadora,
                COALESCE(r.nombre, e.nombre) AS nombre_actor
            FROM Usuario u
            LEFT JOIN Recepcionista r
                ON r.idRecepcionista = u.idRecepcionista
            LEFT JOIN Educadora e
                ON e.idEducadora = u.idEducadora
            WHERE u.nombreUsuario = %s
              AND u.activo = 1
            LIMIT 1
            """,
            (nombre_usuario,)
        )

        usuario = cursor.fetchone()

        if not usuario or not _verificar_hash(
            contrasena,
            usuario["passwordHash"]
        ):
            return None

        usuario.pop("passwordHash", None)
        return usuario

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


def crear_usuario(
    nombre_usuario,
    contrasena,
    rol,
    id_recepcionista=None,
    id_educadora=None
):
    """Crea una cuenta vinculada a un registro de Recepcionista o Educadora."""
    nombre_usuario = (nombre_usuario or "").strip()
    rol = (rol or "").strip().lower()

    if len(nombre_usuario) < 4:
        raise ValueError("El nombre de usuario debe tener al menos 4 caracteres.")

    if len(nombre_usuario) > 60:
        raise ValueError("El nombre de usuario no puede superar 60 caracteres.")

    if len(contrasena or "") < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")

    if rol == "recepcionista":
        if not id_recepcionista or id_educadora is not None:
            raise ValueError("Seleccione una recepcionista válida.")
    elif rol == "educadora":
        if not id_educadora or id_recepcionista is not None:
            raise ValueError("Seleccione una educadora válida.")
    else:
        raise ValueError("El rol debe ser recepcionista o educadora.")

    hash_contrasena = _crear_hash(contrasena)

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO Usuario (
                nombreUsuario,
                passwordHash,
                rol,
                idRecepcionista,
                idEducadora
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                nombre_usuario,
                hash_contrasena,
                rol,
                id_recepcionista,
                id_educadora
            )
        )

        id_usuario = cursor.lastrowid
        conexion.commit()
        return id_usuario

    except Exception:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()
