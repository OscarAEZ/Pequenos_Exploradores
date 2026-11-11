"""Pantalla de acceso para los actores del sistema."""

from pathlib import Path

import customtkinter as ctk
from PIL import Image

from app.services.autenticacion_service import autenticar_usuario


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COLORES = {
    "fondo": "#F3F5FC",
    "blanco": "#FFFFFF",
    "lavanda": "#D8CCF5",
    "lavanda_claro": "#ECE9FA",
    "menta": "#AFE8CF",
    "texto": "#17264A",
    "secundario": "#687895",
    "borde": "#D5DDED",
    "rojo": "#C84C5A"
}


class VentanaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.usuario = None
        self.title("Pequeños Exploradores - Inicio de sesión")
        self.geometry("780x560")
        self.resizable(False, False)
        self.configure(fg_color=COLORES["fondo"])

        recursos = Path(__file__).resolve().parent / "recursos_guarderia"
        logo = Image.open(
            recursos / "logo_pequenos_exploradores.png"
        ).convert("RGBA")
        self.logo = ctk.CTkImage(
            light_image=logo,
            dark_image=logo,
            size=(132, 132)
        )

        osito = Image.open(
            recursos / "osito_pastel_con_globos_y_estrellas.png"
        ).convert("RGBA")
        self.osito = ctk.CTkImage(
            light_image=osito,
            dark_image=osito,
            size=(112, 126)
        )

        contenedor = ctk.CTkFrame(
            self,
            fg_color=COLORES["blanco"],
            corner_radius=20,
            border_width=1,
            border_color=COLORES["borde"]
        )
        contenedor.pack(
            fill="both",
            expand=True,
            padx=34,
            pady=28
        )

        ctk.CTkLabel(
            contenedor,
            image=self.logo,
            text=""
        ).pack(pady=(16, 2))

        ctk.CTkLabel(
            contenedor,
            text="Pequeños Exploradores",
            font=("Arial", 25, "bold"),
            text_color=COLORES["texto"]
        ).pack(pady=(0, 3))

        ctk.CTkLabel(
            contenedor,
            text="Sistema de Gestión de Guardería",
            font=("Arial", 13),
            text_color=COLORES["secundario"]
        ).pack(pady=(0, 17))

        formulario = ctk.CTkFrame(
            contenedor,
            fg_color="transparent",
            width=390
        )
        formulario.pack()

        ctk.CTkLabel(
            formulario,
            text="Nombre de usuario",
            font=("Arial", 12, "bold"),
            text_color=COLORES["texto"]
        ).pack(anchor="w", pady=(0, 5))

        self.entrada_usuario = ctk.CTkEntry(
            formulario,
            width=360,
            height=40,
            corner_radius=9,
            border_color=COLORES["borde"],
            fg_color=COLORES["blanco"],
            text_color=COLORES["texto"],
            placeholder_text="Escribe tu usuario"
        )
        self.entrada_usuario.pack(pady=(0, 13))

        ctk.CTkLabel(
            formulario,
            text="Contraseña",
            font=("Arial", 12, "bold"),
            text_color=COLORES["texto"]
        ).pack(anchor="w", pady=(0, 5))

        self.entrada_contrasena = ctk.CTkEntry(
            formulario,
            width=360,
            height=40,
            corner_radius=9,
            border_color=COLORES["borde"],
            fg_color=COLORES["blanco"],
            text_color=COLORES["texto"],
            placeholder_text="Escribe tu contraseña",
            show="*"
        )
        self.entrada_contrasena.pack()

        self.lbl_estado = ctk.CTkLabel(
            formulario,
            text="",
            font=("Arial", 11),
            text_color=COLORES["rojo"],
            wraplength=350
        )
        self.lbl_estado.pack(pady=(7, 2))

        ctk.CTkButton(
            formulario,
            text="Iniciar sesión",
            width=210,
            height=42,
            corner_radius=10,
            font=("Arial", 13, "bold"),
            fg_color=COLORES["menta"],
            hover_color="#83D0AE",
            text_color=COLORES["texto"],
            command=self._iniciar_sesion
        ).pack(pady=(8, 5))

        ctk.CTkLabel(
            contenedor,
            image=self.osito,
            text=""
        ).place(relx=0.91, rely=0.88, anchor="center")

        ctk.CTkLabel(
            contenedor,
            text="Acceso exclusivo para personal de recepción y educadoras",
            font=("Arial", 10),
            text_color=COLORES["secundario"]
        ).pack(side="bottom", pady=(0, 12))

        self.entrada_usuario.focus_set()
        self.bind("<Return>", lambda _evento: self._iniciar_sesion())

    def _iniciar_sesion(self):
        nombre_usuario = self.entrada_usuario.get().strip()
        contrasena = self.entrada_contrasena.get()

        if not nombre_usuario or not contrasena:
            self.lbl_estado.configure(
                text="Escribe tu nombre de usuario y contraseña."
            )
            return

        try:
            usuario = autenticar_usuario(nombre_usuario, contrasena)

            if usuario is None:
                self.lbl_estado.configure(
                    text="Usuario o contraseña incorrectos, o cuenta desactivada."
                )
                self.entrada_contrasena.delete(0, "end")
                return

            self.usuario = usuario
            self.destroy()

        except Exception as error:
            self.lbl_estado.configure(
                text=(
                    "No fue posible iniciar sesión. Verifica la conexión "
                    "y que hayas ejecutado database/usuarios.sql.\n"
                    f"Detalle: {error}"
                )
            )


def iniciar_sesion():
    ventana = VentanaLogin()
    ventana.mainloop()
    return ventana.usuario
