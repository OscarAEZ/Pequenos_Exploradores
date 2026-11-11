"""Punto de entrada del sistema Pequeños Exploradores."""

from app.interfaces.login import iniciar_sesion
from app.interfaces.ventana_principal import VentanaPrincipal
from app.interfaces.ventana_educadora import VentanaEducadora


def main():
    # Al cerrar sesión se vuelve a mostrar el acceso.
    while True:
        usuario = iniciar_sesion()

        if usuario is None:
            break

        if usuario["rol"] == "recepcionista":
            aplicacion = VentanaPrincipal(usuario)
        elif usuario["rol"] == "educadora":
            aplicacion = VentanaEducadora(usuario)
        else:
            # El servicio de autenticación solo permite estos dos roles.
            break

        aplicacion.mainloop()


if __name__ == "__main__":
    main()
