"""Interfaz exclusiva de la Educadora: recibe y consulta sus avisos."""

from pathlib import Path

import customtkinter as ctk
from PIL import Image

from app.services.guarderia_service import listar_avisos_por_educadora


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COLORES = {
    "fondo": "#F3F5FC",
    "blanco": "#FFFFFF",
    "lavanda": "#D8CCF5",
    "lavanda_claro": "#ECE9FA",
    "menta": "#AFE8CF",
    "menta_oscuro": "#83D0AE",
    "azul": "#E3ECFC",
    "texto": "#17264A",
    "secundario": "#687895",
    "borde": "#D5DDED",
    "rojo": "#E56B70"
}


class VentanaEducadora(ctk.CTk):
    """Muestra únicamente los avisos asignados a la educadora autenticada."""

    def __init__(self, usuario):
        super().__init__()

        if usuario.get("rol") != "educadora" or not usuario.get("idEducadora"):
            raise PermissionError("Esta interfaz es exclusiva de educadoras.")

        self.usuario = usuario
        self.title("Pequeños Exploradores - Educadora")
        self.geometry("1180x760")
        self.minsize(1000, 650)
        self.configure(fg_color=COLORES["fondo"])

        recursos = Path(__file__).resolve().parent / "recursos_guarderia"

        logo = Image.open(
            recursos / "logo_pequenos_exploradores.png"
        ).convert("RGBA")
        self.logo_lateral = ctk.CTkImage(
            light_image=logo,
            dark_image=logo,
            size=(105, 105)
        )
        self.logo_encabezado = ctk.CTkImage(
            light_image=logo,
            dark_image=logo,
            size=(48, 48)
        )

        imagen_avisos = Image.open(
            recursos / "icono_avisos.png"
        ).convert("RGBA")
        self.icono_avisos = ctk.CTkImage(
            light_image=imagen_avisos,
            dark_image=imagen_avisos,
            size=(22, 25)
        )

        osito = Image.open(
            recursos / "osito_pastel_con_globos_y_estrellas.png"
        ).convert("RGBA")
        self.osito = ctk.CTkImage(
            light_image=osito,
            dark_image=osito,
            size=(135, 150)
        )

        imagen_exito = Image.open(
            recursos / "icono_exito.png"
        ).convert("RGBA")
        self.icono_exito = ctk.CTkImage(
            light_image=imagen_exito,
            dark_image=imagen_exito,
            size=(58, 58)
        )

        imagen_error = Image.open(
            recursos / "icono_error.png"
        ).convert("RGBA")
        self.icono_error = ctk.CTkImage(
            light_image=imagen_error,
            dark_image=imagen_error,
            size=(58, 58)
        )

        self._crear_interfaz()
        self._mostrar_instruccion_consulta()

    def _crear_interfaz(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        menu = ctk.CTkFrame(
            self,
            width=215,
            corner_radius=0,
            fg_color=COLORES["lavanda_claro"]
        )
        menu.grid(row=0, column=0, sticky="nsew")
        menu.grid_propagate(False)

        ctk.CTkLabel(
            menu,
            image=self.logo_lateral,
            text=""
        ).pack(pady=(18, 22))

        ctk.CTkButton(
            menu,
            text="Avisos recibidos",
            image=self.icono_avisos,
            compound="left",
            anchor="w",
            width=190,
            height=48,
            corner_radius=10,
            font=("Arial", 14, "bold"),
            fg_color=COLORES["lavanda"],
            hover_color="#C9B9EF",
            text_color=COLORES["texto"],
            command=self.consultar_avisos
        ).pack(fill="x", padx=12, pady=6)

        inferior = ctk.CTkFrame(menu, fg_color="transparent")
        inferior.pack(side="bottom", pady=12)

        ctk.CTkLabel(
            inferior,
            image=self.osito,
            text="",
            fg_color="transparent"
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            inferior,
            text="Sistema de Gestión\n- Guardería -",
            font=("Arial", 11),
            text_color=COLORES["secundario"],
            justify="center"
        ).pack()

        principal = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=COLORES["fondo"]
        )
        principal.grid(row=0, column=1, sticky="nsew")
        principal.grid_columnconfigure(0, weight=1)
        principal.grid_rowconfigure(1, weight=1)

        encabezado = ctk.CTkFrame(
            principal,
            height=75,
            corner_radius=0,
            fg_color=COLORES["blanco"]
        )
        encabezado.grid(row=0, column=0, sticky="ew")
        encabezado.grid_propagate(False)

        ctk.CTkLabel(
            encabezado,
            image=self.logo_encabezado,
            text=""
        ).pack(side="left", padx=(22, 12), pady=5)

        textos = ctk.CTkFrame(encabezado, fg_color="transparent")
        textos.pack(side="left", pady=12)

        ctk.CTkLabel(
            textos,
            text="Pequeños Exploradores",
            font=("Arial", 19, "bold"),
            text_color=COLORES["texto"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            textos,
            text="Panel de educadora - Avisos recibidos",
            font=("Arial", 11),
            text_color=COLORES["secundario"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text=f"Sesión: {self.usuario.get('nombre_actor', 'Educadora')}  |  Educadora",
            font=("Arial", 11, "bold"),
            text_color=COLORES["secundario"]
        ).pack(side="right", padx=12)

        ctk.CTkButton(
            encabezado,
            text="Cerrar sesión",
            width=112,
            height=34,
            corner_radius=8,
            fg_color=COLORES["lavanda"],
            hover_color="#C9B9EF",
            text_color=COLORES["texto"],
            command=self.destroy
        ).pack(side="right", padx=(0, 18))

        self.area_contenido = ctk.CTkFrame(
            principal,
            fg_color=COLORES["fondo"],
            corner_radius=0
        )
        self.area_contenido.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=18,
            pady=15
        )
        self.area_contenido.grid_columnconfigure(0, weight=1)
        self.area_contenido.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.area_contenido,
            text="Avisos recibidos",
            font=("Arial", 25, "bold"),
            text_color=COLORES["texto"]
        ).grid(row=0, column=0, sticky="w", pady=(5, 2))

        contenedor = ctk.CTkFrame(
            self.area_contenido,
            fg_color=COLORES["blanco"],
            corner_radius=13,
            border_width=1,
            border_color=COLORES["borde"]
        )
        contenedor.grid(row=1, column=0, sticky="nsew")
        contenedor.grid_columnconfigure(0, weight=1)
        contenedor.grid_rowconfigure(1, weight=1)

        barra = ctk.CTkFrame(contenedor, fg_color="transparent")
        barra.grid(row=0, column=0, sticky="ew", padx=18, pady=(15, 8))

        ctk.CTkLabel(
            barra,
            text=f"Educadora: {self.usuario.get('nombre_actor', '')}",
            font=("Arial", 13, "bold"),
            text_color=COLORES["texto"]
        ).pack(side="left")

        ctk.CTkButton(
            barra,
            text="Consultar avisos",
            width=125,
            height=36,
            corner_radius=8,
            fg_color=COLORES["menta"],
            hover_color=COLORES["menta_oscuro"],
            text_color=COLORES["texto"],
            command=self.consultar_avisos
        ).pack(side="right")

        self.lista_avisos = ctk.CTkScrollableFrame(
            contenedor,
            fg_color=COLORES["fondo"],
            corner_radius=10
        )
        self.lista_avisos.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=18,
            pady=(5, 18)
        )

    def _limpiar_avisos(self):
        for widget in self.lista_avisos.winfo_children():
            widget.destroy()

    def _mostrar_instruccion_consulta(self):
        self._limpiar_avisos()

        ctk.CTkLabel(
            self.lista_avisos,
            text="Presiona «Consultar avisos» para ver los avisos que te fueron comunicados.",
            font=("Arial", 14),
            text_color=COLORES["secundario"]
        ).pack(pady=35)

    def consultar_avisos(self):
        self._limpiar_avisos()

        try:
            avisos = listar_avisos_por_educadora(
                self.usuario["idEducadora"]
            )

            if not avisos:
                ctk.CTkLabel(
                    self.lista_avisos,
                    text="Todavía no tienes avisos comunicados.",
                    font=("Arial", 14),
                    text_color=COLORES["secundario"]
                ).pack(pady=35)
                return

            for aviso in avisos:
                tarjeta = ctk.CTkFrame(
                    self.lista_avisos,
                    fg_color=COLORES["blanco"],
                    corner_radius=11,
                    border_width=1,
                    border_color=COLORES["borde"]
                )
                tarjeta.pack(fill="x", padx=7, pady=7)

                ctk.CTkLabel(
                    tarjeta,
                    text=f"Aviso #{aviso['idAviso']}  ·  {aviso['menor']}",
                    font=("Arial", 14, "bold"),
                    text_color=COLORES["texto"]
                ).pack(anchor="w", padx=16, pady=(13, 6))

                ctk.CTkLabel(
                    tarjeta,
                    text=(
                        f"Tutor: {aviso['tutor']}\n"
                        f"Comunicado por: {aviso['recepcionista']}"
                    ),
                    font=("Arial", 11),
                    text_color=COLORES["secundario"],
                    justify="left"
                ).pack(anchor="w", padx=16, pady=(0, 7))

                ctk.CTkLabel(
                    tarjeta,
                    text=aviso["descripcion"],
                    font=("Arial", 13),
                    text_color=COLORES["texto"],
                    fg_color=COLORES["azul"],
                    corner_radius=8,
                    justify="left",
                    anchor="w",
                    wraplength=760
                ).pack(fill="x", padx=16, pady=(0, 13), ipady=9)

        except Exception as error:
            self._mostrar_error(str(error))

    def _mostrar_error(self, detalle):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Error de consulta")
        ventana.geometry("410x235")
        ventana.resizable(False, False)
        ventana.configure(fg_color=COLORES["blanco"])
        ventana.transient(self)
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            image=self.icono_error,
            text=""
        ).pack(pady=(14, 4))

        ctk.CTkLabel(
            ventana,
            text=f"No fue posible consultar los avisos.\n{detalle}",
            font=("Arial", 12),
            text_color=COLORES["texto"],
            wraplength=350,
            justify="center"
        ).pack(padx=18, pady=7)

        ctk.CTkButton(
            ventana,
            text="Aceptar",
            width=120,
            height=36,
            fg_color=COLORES["lavanda"],
            hover_color="#C9B9EF",
            text_color=COLORES["texto"],
            command=ventana.destroy
        ).pack(pady=10)
