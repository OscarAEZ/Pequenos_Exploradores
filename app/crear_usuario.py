"""Asistente de terminal para crear cuentas de Recepcionista y Educadora.

Ejecutar desde la carpeta principal:
    python -m app.crear_usuario
"""

from getpass import getpass

from app.services.autenticacion_service import crear_usuario
from app.services.guarderia_service import (
    listar_recepcionistas,
    listar_educadoras
)


def seleccionar_actor(rol):
    if rol == "recepcionista":
        actores = listar_recepcionistas()
        campo_id = "idRecepcionista"
        campo_nombre = "nombre"
        etiqueta = "recepcionista"
    else:
        actores = listar_educadoras()
        campo_id = "idEducadora"
        campo_nombre = "nombre"
        etiqueta = "educadora"

    if not actores:
        raise ValueError(
            f"No hay registros de {etiqueta}. "
            "Primero agrega el registro correspondiente en MySQL."
        )

    print(f"\\nRegistros de {etiqueta} disponibles:")
    for actor in actores:
        print(f"  {actor[campo_id]} - {actor[campo_nombre]}")

    while True:
        valor = input(f"Escribe el ID de la {etiqueta}: ").strip()
        try:
            id_actor = int(valor)
        except ValueError:
            print("El ID debe ser un número.")
            continue

        if any(actor[campo_id] == id_actor for actor in actores):
            return id_actor

        print("Ese ID no aparece en la lista. Intenta nuevamente.")


def main():
    print("=" * 55)
    print("CREAR USUARIO - PEQUENOS EXPLORADORES")
    print("=" * 55)
    print("1. Recepcionista")
    print("2. Educadora")

    opcion = input("Selecciona el rol (1 o 2): ").strip()
    if opcion == "1":
        rol = "recepcionista"
    elif opcion == "2":
        rol = "educadora"
    else:
        print("Opción no válida.")
        return

    id_actor = seleccionar_actor(rol)
    nombre_usuario = input("Nombre de usuario (mínimo 4 caracteres): ").strip()
    contrasena = getpass("Contraseña (mínimo 8 caracteres): ")
    confirmacion = getpass("Confirma la contraseña: ")

    if contrasena != confirmacion:
        print("Las contraseñas no coinciden. No se creó la cuenta.")
        return

    if rol == "recepcionista":
        id_usuario = crear_usuario(
            nombre_usuario,
            contrasena,
            rol,
            id_recepcionista=id_actor
        )
    else:
        id_usuario = crear_usuario(
            nombre_usuario,
            contrasena,
            rol,
            id_educadora=id_actor
        )

    print(f"\\nCuenta creada correctamente. ID de usuario: {id_usuario}")
    print("Ya puedes iniciar sesión desde la aplicación.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"\\nNo fue posible crear la cuenta: {error}")