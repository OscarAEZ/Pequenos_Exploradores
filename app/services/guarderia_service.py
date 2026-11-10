
"""Servicios y operaciones de la guardería Pequeños Exploradores.

Separa las consultas SQL de las interfaces gráficas.
"""

from contextlib import contextmanager

from app.database.conexion import obtener_conexion


@contextmanager
def sesion_bd():
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        yield conexion, cursor

    except Exception:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()


def consultar(sql, parametros=()):
    with sesion_bd() as (_, cursor):
        cursor.execute(sql, parametros)
        return cursor.fetchall()


# --------------------------------------------------
# INFORMACIÓN GENERAL
# --------------------------------------------------

def obtener_resumen():
    consultas = {
        "menores": "SELECT COUNT(*) AS total FROM Menor",
        "avisos": "SELECT COUNT(*) AS total FROM Aviso",
        "pendientes": """
            SELECT COUNT(*) AS total
            FROM Aviso
            WHERE idEducadora IS NULL
        """,
        "autorizaciones": """
            SELECT COUNT(*) AS total
            FROM AutorizacionRetiro
        """
    }

    resultado = {}

    with sesion_bd() as (_, cursor):
        for clave, sql in consultas.items():
            cursor.execute(sql)
            fila = cursor.fetchone()
            resultado[clave] = fila["total"] if fila else 0

    return resultado


# --------------------------------------------------
# CONSULTAS GENERALES
# --------------------------------------------------

def listar_menores():
    return consultar("""
        SELECT idMenor, nombreCompleto
        FROM Menor
        ORDER BY nombreCompleto, idMenor
    """)


def obtener_menor(id_menor):
    filas = consultar("""
        SELECT idMenor, nombreCompleto
        FROM Menor
        WHERE idMenor = %s
    """, (id_menor,))

    return filas[0] if filas else None


def listar_tutores_por_menor(id_menor):
    return consultar("""
        SELECT t.idTutor, t.nombreCompleto
        FROM Tutor t
        INNER JOIN TutorMenor tm
            ON tm.idTutor = t.idTutor
        WHERE tm.idMenor = %s
        ORDER BY t.nombreCompleto
    """, (id_menor,))


def listar_recepcionistas():
    return consultar("""
        SELECT idRecepcionista, nombre
        FROM Recepcionista
        ORDER BY nombre
    """)


def listar_educadoras():
    return consultar("""
        SELECT idEducadora, nombre
        FROM Educadora
        ORDER BY nombre
    """)


# --------------------------------------------------
# CU-01: REGISTRAR AVISOS E INDICACIONES
# --------------------------------------------------

def registrar_aviso(
    id_tutor,
    id_menor,
    id_recepcionista,
    descripcion
):
    descripcion = (descripcion or "").strip()

    if not descripcion:
        raise ValueError(
            "Escribe la descripción del aviso."
        )

    if len(descripcion) > 1000:
        raise ValueError(
            "El aviso no puede superar los 1000 caracteres."
        )

    with sesion_bd() as (conexion, cursor):

        cursor.execute("""
            INSERT INTO Aviso (
                descripcion,
                idTutor,
                idMenor,
                idRecepcionista,
                idEducadora
            )
            VALUES (%s, %s, %s, %s, NULL)
        """, (
            descripcion,
            id_tutor,
            id_menor,
            id_recepcionista
        ))

        id_aviso = cursor.lastrowid
        conexion.commit()

        return id_aviso


# --------------------------------------------------
# CU-02: COMUNICAR AVISOS DE LOS MENORES
# --------------------------------------------------

def listar_avisos_pendientes_comunicacion():
    return consultar("""
        SELECT
            a.idAviso,
            a.descripcion,
            a.idMenor,
            m.nombreCompleto AS menor,
            t.nombreCompleto AS tutor,
            r.nombre AS recepcionista
        FROM Aviso a
        INNER JOIN Menor m
            ON m.idMenor = a.idMenor
        INNER JOIN Tutor t
            ON t.idTutor = a.idTutor
        INNER JOIN Recepcionista r
            ON r.idRecepcionista = a.idRecepcionista
        WHERE a.idEducadora IS NULL
        ORDER BY a.idAviso DESC
    """)


def comunicar_aviso(id_aviso, id_educadora):

    with sesion_bd() as (conexion, cursor):

        cursor.execute("""
            UPDATE Aviso
            SET idEducadora = %s
            WHERE idAviso = %s
            AND idEducadora IS NULL
        """, (id_educadora, id_aviso))

        if cursor.rowcount != 1:
            raise ValueError(
                "El aviso ya fue comunicado o no está disponible."
            )

        conexion.commit()


# --------------------------------------------------
# CU-03: CONSULTAR AVISOS RECIBIDOS
# --------------------------------------------------

def listar_avisos_por_educadora(id_educadora):
    return consultar("""
        SELECT
            a.idAviso,
            a.descripcion,
            a.idMenor,
            m.nombreCompleto AS menor,
            t.nombreCompleto AS tutor,
            r.nombre AS recepcionista
        FROM Aviso a
        INNER JOIN Menor m
            ON m.idMenor = a.idMenor
        INNER JOIN Tutor t
            ON t.idTutor = a.idTutor
        INNER JOIN Recepcionista r
            ON r.idRecepcionista = a.idRecepcionista
        WHERE a.idEducadora = %s
        ORDER BY a.idAviso DESC
    """, (id_educadora,))


# --------------------------------------------------
# CU-04: CONSULTAR INFORMACIÓN DE LOS MENORES
# --------------------------------------------------

def listar_avisos_por_menor(id_menor):
    return consultar("""
        SELECT
            a.idAviso,
            a.descripcion,
            t.nombreCompleto AS tutor,
            r.nombre AS recepcionista,
            e.nombre AS educadora
        FROM Aviso a
        INNER JOIN Tutor t
            ON t.idTutor = a.idTutor
        INNER JOIN Recepcionista r
            ON r.idRecepcionista = a.idRecepcionista
        LEFT JOIN Educadora e
            ON e.idEducadora = a.idEducadora
        WHERE a.idMenor = %s
        ORDER BY a.idAviso DESC
    """, (id_menor,))


# --------------------------------------------------
# CU-05 Y CU-06: PERSONAS AUTORIZADAS
# --------------------------------------------------

def listar_personas_autorizadas(id_menor):
    return consultar("""
        SELECT
            pa.idPersonaAutorizada,
            pa.nombreCompleto AS persona,
            ar.estadoAutorizacion AS estado
        FROM AutorizacionRetiro ar
        INNER JOIN PersonaAutorizada pa
            ON pa.idPersonaAutorizada =
               ar.idPersonaAutorizada
        WHERE ar.idMenor = %s
        ORDER BY pa.nombreCompleto
    """, (id_menor,))


# --------------------------------------------------
# CU-07: ACLARAR DIFERENCIAS DE INFORMACIÓN
# --------------------------------------------------

def obtener_contexto_aclaracion(id_menor):

    menor = obtener_menor(id_menor)

    if menor is None:
        return None

    tutores = listar_tutores_por_menor(id_menor)
    avisos = listar_avisos_por_menor(id_menor)

    return {
        "menor": menor,
        "tutores": tutores,
        "avisos": avisos
    }
