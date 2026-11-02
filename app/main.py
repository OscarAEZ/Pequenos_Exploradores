
import customtkinter as ctk
from mysql.connector import Error
from database.conexion import obtener_menores

# Configuración visual
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def consultar_menores():
    try:
        # Consulta real a MySQL
        menores = obtener_menores()

        texto = (
            "Consulta realizada correctamente.\n"
            f"Menores registrados: {len(menores)}\n\n"
        )

        for id_menor, nombre in menores:
            texto += f"{id_menor} - {nombre}\n"

        resultado.configure(
            text=texto,
            text_color="#246B48"
        )

    except (Error, ValueError, TypeError, OSError) as error:
        resultado.configure(
            text=f"Error al consultar MySQL:\n{error}",
            text_color="#B42335"
        )


# Ventana principal
ventana = ctk.CTk()
ventana.title("Pequeños Exploradores - Prueba técnica")
ventana.geometry("700x500")
ventana.resizable(False, False)

# Contenedor
marco = ctk.CTkFrame(
    ventana,
    fg_color="#F6F3FF",
    corner_radius=15
)
marco.pack(fill="both", expand=True, padx=20, pady=20)

# Título
titulo = ctk.CTkLabel(
    marco,
    text="Pequeños Exploradores",
    font=("Arial", 28, "bold"),
    text_color="#243447"
)
titulo.pack(pady=(35, 10))

# Subtítulo
subtitulo = ctk.CTkLabel(
    marco,
    text="Demostración de conexión Python - MySQL\nUnidad 3 - Evidencia 1",
    font=("Arial", 17),
    text_color="#243447",
    justify="center"
)
subtitulo.pack(pady=10)

# Botón de consulta
boton_consultar = ctk.CTkButton(
    marco,
    text="Consultar menores de prueba",
    width=250,
    height=42,
    command=consultar_menores
)
boton_consultar.pack(pady=15)

# Área para mostrar resultados
resultado = ctk.CTkLabel(
    marco,
    text="Presiona el botón para consultar MySQL.",
    font=("Arial", 15),
    text_color="#243447",
    justify="left",
    wraplength=580
)
resultado.pack(pady=15)

# Botón para cerrar
boton_cerrar = ctk.CTkButton(
    marco,
    text="Cerrar",
    width=140,
    height=38,
    fg_color="#8C81C6",
    hover_color="#7065A9",
    command=ventana.destroy
)
boton_cerrar.pack(pady=10)

# Iniciar aplicación
ventana.mainloop()

