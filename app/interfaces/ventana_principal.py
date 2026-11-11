
import customtkinter as ctk
import tkinter as tk
from pathlib import Path
from PIL import Image

from app.services.guarderia_service import (
    listar_menores,
    listar_tutores_por_menor,
    listar_educadoras,
    registrar_aviso,
    listar_avisos_pendientes_comunicacion,
    comunicar_aviso,
    listar_avisos_por_menor,
    listar_personas_autorizadas,
    obtener_contexto_aclaracion
)


# =====================================================
# CONFIGURACION VISUAL
# =====================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COLORES = {
    # Fondo general y superficies
    "fondo": "#F3F5FC",
    "blanco": "#FFFFFF",

    # Lavanda y morados de la interfaz propuesta
    "lavanda": "#D8CCF5",
    "lavanda_claro": "#ECE9FA",
    "morado": "#B9A8E8",
    "morado_oscuro": "#9682D1",

    # Verde menta para acciones positivas
    "menta": "#AFE8CF",
    "menta_oscuro": "#83D0AE",

    # Azul claro para tarjetas y paneles informativos
    "azul": "#E3ECFC",
    "azul_oscuro": "#344A9A",

    # Texto y bordes
    "texto": "#17264A",
    "secundario": "#687895",
    "borde": "#D5DDED",

    # Estados de mensajes
    "rojo": "#E56B70",
    "amarillo": "#F2B451"
}


# =====================================================
# VENTANA PRINCIPAL
# =====================================================

class VentanaPrincipal(ctk.CTk):

    def __init__(self, usuario):
        super().__init__()

        if usuario.get("rol") != "recepcionista":
            raise PermissionError("Esta interfaz es exclusiva de recepción.")

        self.usuario = usuario

        self.title("Pequeños Exploradores - Sistema de Gestión")
        self.geometry("1180x760")
        self.minsize(1000, 650)
        self.configure(fg_color=COLORES["fondo"])

        # Cargar el logotipo desde app/interfaces/recursos_guarderia/
        ruta_logo = Path(__file__).resolve().parent / "recursos_guarderia" / "logo_pequenos_exploradores.png"
        self.logo_original = tk.PhotoImage(file=str(ruta_logo))
        self.logo_lateral = self.logo_original.subsample(10, 10)
        self.logo_encabezado = self.logo_original.subsample(25, 25)

        # Cargar los iconos del menu lateral desde recursos_guarderia.
        ruta_icono_avisos = (
            Path(__file__).resolve().parent
            / "recursos_guarderia"
            / "icono_avisos.png"
        )
        imagen_icono_avisos = Image.open(ruta_icono_avisos).convert("RGBA")
        self.icono_avisos = ctk.CTkImage(
            light_image=imagen_icono_avisos,
            dark_image=imagen_icono_avisos,
            size=(18, 22)
        )

        ruta_icono_personas = (
            Path(__file__).resolve().parent
            / "recursos_guarderia"
            / "icono_personas.png"
        )
        imagen_icono_personas = Image.open(ruta_icono_personas).convert("RGBA")
        self.icono_personas = ctk.CTkImage(
            light_image=imagen_icono_personas,
            dark_image=imagen_icono_personas,
            size=(23, 16)
        )

        # Cargar la ilustracion decorativa inferior (PNG con fondo transparente).
        ruta_ilustracion = (
            Path(__file__).resolve().parent
            / "recursos_guarderia"
            / "osito_pastel_con_globos_y_estrellas.png"
        )
        imagen_ilustracion = Image.open(ruta_ilustracion).convert("RGBA")
        self.ilustracion_inferior = ctk.CTkImage(
            light_image=imagen_ilustracion,
            dark_image=imagen_ilustracion,
            size=(145, 162)
        )

        # Cargar el avatar del menor para las tarjetas informativas.
        ruta_avatar = (
            Path(__file__).resolve().parent
            / "recursos_guarderia"
            / "avatar_menor.png"
        )
        imagen_avatar = Image.open(ruta_avatar).convert("RGBA")
        self.imagen_menor = ctk.CTkImage(
            light_image=imagen_avatar,
            dark_image=imagen_avatar,
            size=(48, 48)
        )

        # Cargar los iconos para los mensajes emergentes.
        # Los tres archivos deben estar dentro de recursos_guarderia.
        ruta_recursos = Path(__file__).resolve().parent / "recursos_guarderia"

        imagen_exito = Image.open(
            ruta_recursos / "icono_exito.png"
        ).convert("RGBA")
        self.icono_mensaje_exito = ctk.CTkImage(
            light_image=imagen_exito,
            dark_image=imagen_exito,
            size=(64, 64)
        )

        imagen_advertencia = Image.open(
            ruta_recursos / "icono_advertencia.png"
        ).convert("RGBA")
        self.icono_mensaje_advertencia = ctk.CTkImage(
            light_image=imagen_advertencia,
            dark_image=imagen_advertencia,
            size=(64, 64)
        )

        imagen_error = Image.open(
            ruta_recursos / "icono_error.png"
        ).convert("RGBA")
        self.icono_mensaje_error = ctk.CTkImage(
            light_image=imagen_error,
            dark_image=imagen_error,
            size=(64, 64)
        )

        self._crear_estructura()

        self.mostrar_avisos("registrar")

    # =================================================
    # ESTRUCTURA GENERAL
    # =================================================

    def _crear_estructura(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # MENU LATERAL

        self.menu_lateral = ctk.CTkFrame(
            self,
            width=215,
            corner_radius=0,
            fg_color=COLORES["lavanda_claro"]
        )

        self.menu_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.menu_lateral.grid_propagate(False)

        logo = tk.Label(
            self.menu_lateral,
            image=self.logo_lateral,
            bg=COLORES["lavanda_claro"],
            bd=0,
            highlightthickness=0
        )
        logo.image = self.logo_lateral
        logo.pack(pady=(15, 22))

        self.btn_avisos = ctk.CTkButton(
            self.menu_lateral,
            text="Avisos",
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
            command=lambda: self.mostrar_avisos("registrar")
        )
        self.btn_avisos.pack(
            fill="x",
            padx=12,
            pady=6
        )

        self.btn_personas = ctk.CTkButton(
            self.menu_lateral,
            text="Personas autorizadas",
            image=self.icono_personas,
            compound="left",
            anchor="w",
            width=190,
            height=48,
            corner_radius=10,
            font=("Arial", 13),
            fg_color="transparent",
            hover_color=COLORES["lavanda"],
            text_color=COLORES["texto"],
            command=self.mostrar_personas
        )
        self.btn_personas.pack(
            fill="x",
            padx=12,
            pady=6
        )

        # ILUSTRACION INFERIOR

        inferior = ctk.CTkFrame(
            self.menu_lateral,
            fg_color="transparent"
        )
        inferior.pack(
            side="bottom",
            pady=12
        )

        # Ilustracion del osito en la parte inferior izquierda.
        # Se conserva la referencia en self para que la imagen no desaparezca.
        ctk.CTkLabel(
            inferior,
            image=self.ilustracion_inferior,
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

        # AREA PRINCIPAL

        self.panel_principal = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=COLORES["fondo"]
        )

        self.panel_principal.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.panel_principal.grid_rowconfigure(1, weight=1)
        self.panel_principal.grid_columnconfigure(0, weight=1)

        # ENCABEZADO

        encabezado = ctk.CTkFrame(
            self.panel_principal,
            height=75,
            corner_radius=0,
            fg_color=COLORES["blanco"]
        )

        encabezado.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        encabezado.grid_propagate(False)

        logo_header = tk.Label(
            encabezado,
            image=self.logo_encabezado,
            bg=COLORES["blanco"],
            bd=0,
            highlightthickness=0
        )
        logo_header.image = self.logo_encabezado
        logo_header.pack(
            side="left",
            padx=(22, 12),
            pady=5
        )

        textos = ctk.CTkFrame(
            encabezado,
            fg_color="transparent"
        )
        textos.pack(side="left", pady=12)

        ctk.CTkLabel(
            encabezado,
            text=f"Sesión: {self.usuario.get('nombre_actor', 'Recepcionista')}  |  Recepcionista",
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

        ctk.CTkLabel(
            textos,
            text="Pequeños Exploradores",
            font=("Arial", 19, "bold"),
            text_color=COLORES["texto"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            textos,
            text="Sistema de Gestión - Guardería",
            font=("Arial", 11),
            text_color=COLORES["secundario"]
        ).pack(anchor="w")

        # CONTENIDO DINAMICO

        self.area_contenido = ctk.CTkFrame(
            self.panel_principal,
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
        self.area_contenido.grid_rowconfigure(0, weight=1)

    # =================================================
    # FUNCIONES GENERALES DE INTERFAZ
    # =================================================

    def _limpiar_area(self):

        for elemento in self.area_contenido.winfo_children():
            elemento.destroy()

    def _seleccionar_menu(self, opcion):

        if opcion == "avisos":
            self.btn_avisos.configure(
                fg_color=COLORES["lavanda"],
                font=("Arial", 14, "bold")
            )

            self.btn_personas.configure(
                fg_color="transparent",
                font=("Arial", 13)
            )

        else:
            self.btn_personas.configure(
                fg_color=COLORES["lavanda"],
                font=("Arial", 13, "bold")
            )

            self.btn_avisos.configure(
                fg_color="transparent",
                font=("Arial", 14)
            )

    def _titulo_pagina(self, titulo, descripcion):

        ctk.CTkLabel(
            self.area_contenido,
            text=titulo,
            font=("Arial", 25, "bold"),
            text_color=COLORES["texto"]
        ).pack(anchor="w", pady=(5, 2))

        ctk.CTkLabel(
            self.area_contenido,
            text=descripcion,
            font=("Arial", 13),
            text_color=COLORES["secundario"]
        ).pack(anchor="w", pady=(0, 15))

    def _panel(self, padre):

        return ctk.CTkFrame(
            padre,
            fg_color=COLORES["blanco"],
            corner_radius=13,
            border_width=1,
            border_color=COLORES["borde"]
        )

    def _etiqueta(self, padre, texto):

        return ctk.CTkLabel(
            padre,
            text=texto,
            font=("Arial", 13, "bold"),
            text_color=COLORES["texto"]
        )

    def _combo(self, padre, valores, comando=None):

        return ctk.CTkComboBox(
            padre,
            values=valores,
            command=comando,
            height=38,
            corner_radius=8,
            border_color=COLORES["borde"],
            fg_color=COLORES["blanco"],
            button_color=COLORES["lavanda"],
            button_hover_color="#C9B9EF",
            dropdown_fg_color=COLORES["blanco"],
            text_color=COLORES["texto"],
            font=("Arial", 12),
            state="readonly"
        )

    def _boton(
        self,
        padre,
        texto,
        comando,
        color=None,
        ancho=180
    ):

        return ctk.CTkButton(
            padre,
            text=texto,
            command=comando,
            width=ancho,
            height=42,
            corner_radius=9,
            font=("Arial", 13, "bold"),
            fg_color=color or COLORES["menta"],
            hover_color=(
                COLORES["menta_oscuro"]
                if color is None
                else COLORES["morado_oscuro"]
            ),
            text_color=COLORES["texto"]
        )

    # =================================================
    # MENSAJES EMERGENTES
    # =================================================

    def _mensaje(self, titulo, mensaje, tipo="exito"):

        # Seleccionar la imagen correspondiente al estado del mensaje.
        configuracion = {
            "exito": self.icono_mensaje_exito,
            "advertencia": self.icono_mensaje_advertencia,
            "error": self.icono_mensaje_error
        }

        icono = configuracion.get(
            tipo,
            configuracion["exito"]
        )

        ventana = ctk.CTkToplevel(self)
        ventana.title("Pequeños Exploradores")
        ventana.geometry("410x255")
        ventana.resizable(False, False)
        ventana.configure(fg_color=COLORES["blanco"])
        ventana.transient(self)
        ventana.grab_set()

        ventana.update_idletasks()

        x = self.winfo_rootx() + (
            self.winfo_width() - 410
        ) // 2

        y = self.winfo_rooty() + (
            self.winfo_height() - 255
        ) // 2

        ventana.geometry(f"410x255+{x}+{y}")

        # Mostrar el icono PNG en lugar del símbolo de texto.
        ctk.CTkLabel(
            ventana,
            image=icono,
            text="",
            fg_color="transparent"
        ).pack(pady=(16, 5))

        ctk.CTkLabel(
            ventana,
            text=mensaje,
            font=("Arial", 14),
            text_color=COLORES["texto"],
            wraplength=340,
            justify="center"
        ).pack(padx=20, pady=10)

        self._boton(
            ventana,
            "Aceptar",
            ventana.destroy,
            COLORES["lavanda"],
            130
        ).pack(pady=12)


    # =================================================
    # PESTAÑAS DE AVISOS
    # =================================================

    def _crear_pestanas(self, seleccion):

        marco = ctk.CTkFrame(
            self.area_contenido,
            fg_color="transparent"
        )
        marco.pack(fill="x", pady=(0, 12))

        opciones = [
            ("Registrar aviso", "registrar"),
            ("Comunicar avisos", "comunicar")
        ]

        for texto, valor in opciones:

            activo = valor == seleccion

            boton = ctk.CTkButton(
                marco,
                text=texto,
                width=175,
                height=38,
                corner_radius=8,
                fg_color=(
                    COLORES["lavanda"]
                    if activo
                    else COLORES["blanco"]
                ),
                hover_color="#C9B9EF",
                text_color=COLORES["texto"],
                border_width=1,
                border_color=COLORES["borde"],
                command=lambda v=valor: self.mostrar_avisos(v)
            )

            boton.pack(side="left", padx=(0, 8))

    # =================================================
    # CU-01 Y CU-02
    # =================================================

    def mostrar_avisos(self, seccion="registrar"):

        self._seleccionar_menu("avisos")
        self._limpiar_area()

        self._titulo_pagina(
            "Avisos e indicaciones",
            "Registre avisos y comuníquelos a la educadora correspondiente."
        )

        self._crear_pestanas(seccion)

        if seccion == "registrar":
            self._pantalla_registrar_aviso()

        elif seccion == "comunicar":
            self._pantalla_comunicar_aviso()


    # =================================================
    # CU-01: REGISTRAR AVISOS
    # =================================================

    def _pantalla_registrar_aviso(self):

        formulario = ctk.CTkScrollableFrame(
            self.area_contenido,
            fg_color=COLORES["blanco"],
            corner_radius=13,
            border_width=1,
            border_color=COLORES["borde"]
        )

        formulario.pack(
            fill="both",
            expand=True
        )

        self._etiqueta(
            formulario,
            "Menor:"
        ).pack(anchor="w", padx=20, pady=(18, 7))

        try:
            self.menores = listar_menores()

            self.mapa_menores = {
                f"{m['nombreCompleto']} (ID {m['idMenor']})": m
                for m in self.menores
            }

            valores = list(self.mapa_menores.keys())

        except Exception as error:

            valores = []
            self._mensaje(
                "Error de conexión",
                f"No fue posible consultar los menores.\n{error}",
                "error"
            )

        self.combo_menor = self._combo(
            formulario,
            valores,
            self._seleccionar_menor_registro
        )

        self.combo_menor.set("Seleccione un menor...")
        self.combo_menor.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )

        # TARJETA DEL MENOR

        tarjeta = ctk.CTkFrame(
            formulario,
            fg_color=COLORES["azul"],
            corner_radius=10
        )
        tarjeta.pack(
            fill="x",
            padx=20,
            pady=5
        )

        ctk.CTkLabel(
            tarjeta,
            image=self.imagen_menor,
            text="",
            fg_color="transparent"
        ).pack(side="left", padx=15, pady=8)

        texto_menor = ctk.CTkFrame(
            tarjeta,
            fg_color="transparent"
        )
        texto_menor.pack(side="left", pady=8)

        self._etiqueta(
            texto_menor,
            "Nombre del menor:"
        ).pack(anchor="w")

        self.lbl_nombre_menor = ctk.CTkLabel(
            texto_menor,
            text="---",
            font=("Arial", 13),
            text_color=COLORES["texto"]
        )
        self.lbl_nombre_menor.pack(anchor="w")

        # TUTOR Y RECEPCIONISTA AUTENTICADO

        fila = ctk.CTkFrame(
            formulario,
            fg_color="transparent"
        )
        fila.pack(fill="x", padx=20, pady=12)

        fila.grid_columnconfigure(0, weight=1)
        fila.grid_columnconfigure(1, weight=1)

        columna_tutor = ctk.CTkFrame(
            fila,
            fg_color="transparent"
        )
        columna_tutor.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        self._etiqueta(
            columna_tutor,
            "Tutor:"
        ).pack(anchor="w", pady=(0, 6))

        self.combo_tutor = self._combo(
            columna_tutor,
            ["Seleccione un tutor..."]
        )
        self.combo_tutor.pack(fill="x")
        self.combo_tutor.set("Seleccione un tutor...")

        columna_recepcionista = ctk.CTkFrame(
            fila,
            fg_color=COLORES["azul"],
            corner_radius=8
        )
        columna_recepcionista.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(10, 0)
        )

        self._etiqueta(
            columna_recepcionista,
            "Recepcionista responsable:"
        ).pack(anchor="w", padx=12, pady=(8, 2))

        ctk.CTkLabel(
            columna_recepcionista,
            text=self.usuario.get("nombre_actor", "Usuario de recepción"),
            font=("Arial", 12),
            text_color=COLORES["texto"]
        ).pack(anchor="w", padx=12, pady=(0, 8))

        # DESCRIPCION DEL AVISO

        self._etiqueta(
            formulario,
            "Descripción del aviso:"
        ).pack(anchor="w", padx=20, pady=(12, 7))

        self.txt_descripcion = ctk.CTkTextbox(
            formulario,
            height=135,
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"],
            fg_color=COLORES["blanco"],
            text_color=COLORES["texto"],
            font=("Arial", 13)
        )

        self.txt_descripcion.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        # BOTONES

        botones = ctk.CTkFrame(
            formulario,
            fg_color="transparent"
        )
        botones.pack(pady=(5, 20))

        self._boton(
            botones,
            "▣  Guardar aviso",
            self._guardar_aviso,
            COLORES["menta"],
            200
        ).pack(side="left", padx=8)

        self._boton(
            botones,
            "←  Limpiar",
            self._limpiar_formulario,
            COLORES["lavanda"],
            150
        ).pack(side="left", padx=8)

    def _seleccionar_menor_registro(self, valor):

        menor = self.mapa_menores.get(valor)

        if not menor:
            return

        self.lbl_nombre_menor.configure(
            text=menor["nombreCompleto"]
        )

        try:

            tutores = listar_tutores_por_menor(
                menor["idMenor"]
            )

            self.mapa_tutores = {
                f"{t['nombreCompleto']} (ID {t['idTutor']})": t
                for t in tutores
            }

            valores = list(self.mapa_tutores.keys())

            if not valores:
                valores = ["Sin tutores relacionados"]

            self.combo_tutor.configure(values=valores)
            self.combo_tutor.set("Seleccione un tutor...")

        except Exception as error:

            self._mensaje(
                "Error",
                f"No fue posible consultar los tutores.\n{error}",
                "error"
            )

    def _guardar_aviso(self):

        menor = self.mapa_menores.get(
            self.combo_menor.get()
        )

        tutor = getattr(self, "mapa_tutores", {}).get(
            self.combo_tutor.get()
        )

        id_recepcionista = self.usuario.get("idRecepcionista")

        descripcion = self.txt_descripcion.get(
            "1.0",
            "end"
        ).strip()

        if not menor or not tutor or not id_recepcionista or not descripcion:

            self._mensaje(
                "Información incompleta",
                "Complete la información necesaria para guardar el aviso.",
                "advertencia"
            )
            return

        try:

            id_aviso = registrar_aviso(
                tutor["idTutor"],
                menor["idMenor"],
                id_recepcionista,
                descripcion
            )

            self._mensaje(
                "Aviso registrado",
                f"El aviso se registró correctamente.\nFolio: {id_aviso}",
                "exito"
            )

            self.txt_descripcion.delete("1.0", "end")

        except Exception as error:

            self._mensaje(
                "Error al guardar",
                f"No fue posible guardar el aviso.\n{error}",
                "error"
            )

    def _limpiar_formulario(self):

        self.combo_menor.set("Seleccione un menor...")
        self.lbl_nombre_menor.configure(text="---")
        self.combo_tutor.set("Seleccione un tutor...")
        self.txt_descripcion.delete("1.0", "end")

    # =================================================
    # CU-02: COMUNICAR AVISOS
    # =================================================

    def _pantalla_comunicar_aviso(self):

        panel = self._panel(self.area_contenido)
        panel.pack(fill="both", expand=True, padx=2, pady=2)

        self._etiqueta(
            panel,
            "Avisos pendientes de comunicación:"
        ).pack(anchor="w", padx=20, pady=(20, 8))

        try:

            avisos = listar_avisos_pendientes_comunicacion()

            self.mapa_avisos_pendientes = {
                f"Aviso #{a['idAviso']} - {a['menor']}": a
                for a in avisos
            }

            valores = list(
                self.mapa_avisos_pendientes.keys()
            )

        except Exception as error:

            valores = []
            self._mensaje(
                "Error",
                f"No fue posible consultar los avisos.\n{error}",
                "error"
            )

        self.combo_aviso_pendiente = self._combo(
            panel,
            valores,
            self._mostrar_detalle_pendiente
        )

        self.combo_aviso_pendiente.set(
            "Seleccione un aviso..."
        )

        self.combo_aviso_pendiente.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        self.lbl_detalle_pendiente = ctk.CTkLabel(
            panel,
            text="Seleccione un aviso para visualizar su información.",
            fg_color=COLORES["azul"],
            corner_radius=10,
            height=115,
            wraplength=700,
            justify="left",
            font=("Arial", 13),
            text_color=COLORES["texto"]
        )

        self.lbl_detalle_pendiente.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self._etiqueta(
            panel,
            "Educadora que recibirá el aviso:"
        ).pack(anchor="w", padx=20, pady=(15, 7))

        try:

            educadoras = listar_educadoras()

            self.mapa_educadoras = {
                f"{e['nombre']} (ID {e['idEducadora']})": e
                for e in educadoras
            }

            valores_educadoras = list(
                self.mapa_educadoras.keys()
            )

        except Exception as error:

            valores_educadoras = []
            self._mensaje(
                "Error",
                f"No fue posible consultar las educadoras.\n{error}",
                "error"
            )

        self.combo_educadora = self._combo(
            panel,
            valores_educadoras
        )

        self.combo_educadora.set(
            "Seleccione una educadora..."
        )

        self.combo_educadora.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        if not avisos:

            self._mensaje(
                "Sin avisos pendientes",
                "Actualmente no hay avisos pendientes de comunicar.",
                "advertencia"
            )

        self._boton(
            panel,
            "Comunicar aviso",
            self._comunicar_aviso,
            COLORES["menta"],
            220
        ).pack(pady=15)

    def _mostrar_detalle_pendiente(self, valor):

        aviso = self.mapa_avisos_pendientes.get(valor)

        if not aviso:
            return

        texto = (
            f"Menor: {aviso['menor']}\n"
            f"Tutor: {aviso['tutor']}\n"
            f"Recepcionista: {aviso['recepcionista']}\n\n"
            f"Descripción:\n{aviso['descripcion']}"
        )

        self.lbl_detalle_pendiente.configure(text=texto)

    def _comunicar_aviso(self):

        aviso = self.mapa_avisos_pendientes.get(
            self.combo_aviso_pendiente.get()
        )

        educadora = self.mapa_educadoras.get(
            self.combo_educadora.get()
        )

        if not aviso or not educadora:

            self._mensaje(
                "Información incompleta",
                "Seleccione un aviso y una educadora.",
                "advertencia"
            )
            return

        try:

            comunicar_aviso(
                aviso["idAviso"],
                educadora["idEducadora"]
            )

            self._mensaje(
                "Aviso comunicado",
                "El aviso fue comunicado correctamente a la educadora.",
                "exito"
            )

            self.mostrar_avisos("comunicar")

        except Exception as error:

            self._mensaje(
                "Error",
                f"No fue posible comunicar el aviso.\n{error}",
                "error"
            )

    # =================================================
    # CU-04, CU-05, CU-06 Y CU-07
    # =================================================

    def mostrar_personas(self):

        self._seleccionar_menu("personas")
        self._limpiar_area()

        self._titulo_pagina(
            "Consultar personas autorizadas",
            "Visualice las personas autorizadas para recoger al menor."
        )

        panel = self._panel(self.area_contenido)
        panel.pack(fill="both", expand=True)

        self._etiqueta(
            panel,
            "Menor:"
        ).pack(anchor="w", padx=20, pady=(18, 7))

        try:

            menores = listar_menores()

            self.mapa_menores_personas = {
                f"{m['nombreCompleto']} (ID {m['idMenor']})": m
                for m in menores
            }

            valores = list(
                self.mapa_menores_personas.keys()
            )

        except Exception as error:

            valores = []
            self._mensaje(
                "Error",
                f"No fue posible consultar los menores.\n{error}",
                "error"
            )

        self.combo_menor_personas = self._combo(
            panel,
            valores,
            self._seleccionar_menor_personas
        )

        self.combo_menor_personas.set(
            "Seleccione un menor..."
        )

        self.combo_menor_personas.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )

        # TARJETA DEL MENOR

        tarjeta = ctk.CTkFrame(
            panel,
            fg_color=COLORES["azul"],
            corner_radius=10
        )
        tarjeta.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            tarjeta,
            image=self.imagen_menor,
            text="",
            fg_color="transparent"
        ).pack(side="left", padx=15, pady=8)

        datos = ctk.CTkFrame(
            tarjeta,
            fg_color="transparent"
        )
        datos.pack(side="left", pady=8)

        self._etiqueta(
            datos,
            "Nombre del menor:"
        ).pack(anchor="w")

        self.lbl_menor_personas = ctk.CTkLabel(
            datos,
            text="---",
            font=("Arial", 13),
            text_color=COLORES["texto"]
        )
        self.lbl_menor_personas.pack(anchor="w")

        # TITULO DE TABLA

        self._etiqueta(
            panel,
            "Personas autorizadas:"
        ).pack(anchor="w", padx=20, pady=(15, 7))

        tabla = ctk.CTkFrame(
            panel,
            fg_color=COLORES["blanco"],
            border_width=1,
            border_color=COLORES["borde"],
            corner_radius=8
        )
        tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 10)
        )

        encabezado = ctk.CTkFrame(
            tabla,
            fg_color=COLORES["lavanda"],
            corner_radius=5
        )
        encabezado.pack(fill="x", padx=2, pady=2)

        encabezado.grid_columnconfigure(0, weight=1)
        encabezado.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="Nombre de la persona autorizada",
            font=("Arial", 12, "bold"),
            text_color=COLORES["texto"]
        ).grid(row=0, column=0, sticky="ew", padx=5, pady=10)

        ctk.CTkLabel(
            encabezado,
            text="Estado de autorización",
            font=("Arial", 12, "bold"),
            text_color=COLORES["texto"]
        ).grid(row=0, column=1, sticky="ew", padx=5, pady=10)

        self.filas_personas = ctk.CTkScrollableFrame(
            tabla,
            fg_color=COLORES["blanco"]
        )
        self.filas_personas.pack(
            fill="both",
            expand=True,
            padx=2,
            pady=2
        )

        # BOTONES CU-04 Y CU-07

        botones = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )
        botones.pack(pady=(5, 15))

        self._boton(
            botones,
            "Consultar información",
            self._mostrar_informacion_menor,
            COLORES["lavanda"],
            205
        ).pack(side="left", padx=7)

        self._boton(
            botones,
            "Aclarar diferencias",
            self._abrir_aclaracion,
            COLORES["menta"],
            190
        ).pack(side="left", padx=7)

    def _seleccionar_menor_personas(self, valor):

        menor = self.mapa_menores_personas.get(valor)

        if not menor:
            return

        self.lbl_menor_personas.configure(
            text=menor["nombreCompleto"]
        )

        self._cargar_personas_autorizadas(
            menor["idMenor"]
        )

    def _cargar_personas_autorizadas(self, id_menor):

        for widget in self.filas_personas.winfo_children():
            widget.destroy()

        try:

            personas = listar_personas_autorizadas(id_menor)

            if not personas:

                ctk.CTkLabel(
                    self.filas_personas,
                    text="No hay personas autorizadas registradas.",
                    font=("Arial", 12),
                    text_color=COLORES["secundario"]
                ).pack(pady=20)

                return

            for persona in personas:

                fila = ctk.CTkFrame(
                    self.filas_personas,
                    fg_color=COLORES["blanco"],
                    corner_radius=5
                )
                fila.pack(fill="x", pady=2)

                fila.grid_columnconfigure(0, weight=1)
                fila.grid_columnconfigure(1, weight=1)

                ctk.CTkLabel(
                    fila,
                    text=persona["persona"],
                    font=("Arial", 12),
                    text_color=COLORES["texto"]
                ).grid(
                    row=0,
                    column=0,
                    sticky="ew",
                    padx=10,
                    pady=12
                )

                ctk.CTkLabel(
                    fila,
                    text=persona["estado"],
                    font=("Arial", 12),
                    text_color=COLORES["texto"]
                ).grid(
                    row=0,
                    column=1,
                    sticky="ew",
                    padx=10,
                    pady=12
                )

                ctk.CTkFrame(
                    fila,
                    height=1,
                    fg_color=COLORES["borde"]
                ).grid(
                    row=1,
                    column=0,
                    columnspan=2,
                    sticky="ew"
                )

        except Exception as error:

            self._mensaje(
                "Error",
                f"No fue posible consultar las autorizaciones.\n{error}",
                "error"
            )

    # =================================================
    # CU-04: CONSULTAR INFORMACION DE LOS MENORES
    # =================================================

    def _obtener_contexto_menor_seleccionado(self):

        menor = self.mapa_menores_personas.get(
            self.combo_menor_personas.get()
        )

        if not menor:
            self._mensaje(
                "Seleccione un menor",
                "Primero debe seleccionar un menor.",
                "advertencia"
            )
            return None

        try:
            contexto = obtener_contexto_aclaracion(
                menor["idMenor"]
            )

            if not contexto:
                self._mensaje(
                    "Sin información",
                    "No fue posible localizar la información del menor.",
                    "advertencia"
                )
                return None

            return contexto

        except Exception as error:
            self._mensaje(
                "Error de consulta",
                f"No fue posible obtener la información.\n{error}",
                "error"
            )
            return None

    def _formatear_contexto_menor(self, contexto):

        datos_menor = contexto["menor"]
        tutores = contexto["tutores"]
        avisos = contexto["avisos"]

        lineas = [
            f"Menor: {datos_menor['nombreCompleto']}",
            f"Identificador: {datos_menor['idMenor']}",
            "",
            "Tutores relacionados:"
        ]

        if tutores:
            for tutor in tutores:
                lineas.append(
                    f"• {tutor['nombreCompleto']} (ID {tutor['idTutor']})"
                )
        else:
            lineas.append("No hay tutores registrados.")

        lineas.extend([
            "",
            "Avisos e indicaciones registrados:"
        ])

        if avisos:
            for aviso in avisos:
                fecha = aviso.get("fechaComunicacion")

                if fecha is None:
                    fecha_texto = "Pendiente de comunicación"
                elif hasattr(fecha, "strftime"):
                    fecha_texto = fecha.strftime("%d/%m/%Y %H:%M")
                else:
                    fecha_texto = str(fecha)

                lineas.extend([
                    f"Folio: {aviso['idAviso']}",
                    f"Descripción: {aviso['descripcion']}",
                    f"Tutor: {aviso['tutor']}",
                    f"Recepcionista: {aviso['recepcionista']}",
                    f"Educadora: {aviso['educadora'] or 'Pendiente de comunicación'}",
                    f"Fecha de comunicación: {fecha_texto}",
                    ""
                ])
        else:
            lineas.append("No hay avisos registrados para este menor.")

        lineas.extend([
            "",
            "Nota: esta consulta muestra la información disponible.",
            "No modifica los registros originales."
        ])

        return "\n".join(lineas)

    def _mostrar_informacion_menor(self):

        contexto = self._obtener_contexto_menor_seleccionado()

        if contexto is None:
            return

        self._ventana_informacion(
            "Consultar información del menor · CU-04",
            self._formatear_contexto_menor(contexto)
        )

    # =================================================
    # CU-07: ACLARAR DIFERENCIAS DE INFORMACION
    # =================================================

    def _abrir_aclaracion(self):

        contexto = self._obtener_contexto_menor_seleccionado()

        if contexto is None:
            return

        menor = contexto["menor"]

        ventana = ctk.CTkToplevel(self)
        ventana.title("Aclarar diferencias · Pequeños Exploradores")
        ventana.geometry("760x700")
        ventana.minsize(680, 620)
        ventana.configure(fg_color=COLORES["fondo"])
        ventana.transient(self)
        ventana.grab_set()

        contenido = ctk.CTkScrollableFrame(
            ventana,
            fg_color=COLORES["fondo"],
            corner_radius=0
        )
        contenido.pack(fill="both", expand=True, padx=18, pady=15)

        ctk.CTkLabel(
            contenido,
            text="Aclarar diferencias de información",
            font=("Arial", 22, "bold"),
            text_color=COLORES["texto"]
        ).pack(anchor="w", pady=(5, 3))

        ctk.CTkLabel(
            contenido,
            text=(
                "Revise los datos relacionados con el menor para determinar "
                "si la diferencia detectada puede aclararse."
            ),
            font=("Arial", 13),
            text_color=COLORES["secundario"],
            wraplength=680,
            justify="left"
        ).pack(anchor="w", pady=(0, 14))

        tarjeta_menor = ctk.CTkFrame(
            contenido,
            fg_color=COLORES["azul"],
            corner_radius=10
        )
        tarjeta_menor.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            tarjeta_menor,
            image=self.imagen_menor,
            text="",
            fg_color="transparent"
        ).pack(side="left", padx=14, pady=10)

        datos_menor = ctk.CTkFrame(
            tarjeta_menor,
            fg_color="transparent"
        )
        datos_menor.pack(side="left", fill="x", expand=True, pady=10)

        ctk.CTkLabel(
            datos_menor,
            text="Menor seleccionado",
            font=("Arial", 12, "bold"),
            text_color=COLORES["secundario"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            datos_menor,
            text=menor["nombreCompleto"],
            font=("Arial", 15, "bold"),
            text_color=COLORES["texto"]
        ).pack(anchor="w")

        self._boton(
            contenido,
            "Consultar información relacionada · CU-04",
            lambda: self._consultar_datos_desde_aclaracion(ventana),
            COLORES["lavanda"],
            300
        ).pack(anchor="w", pady=(0, 14))

        self._etiqueta(
            contenido,
            "1. Describa la diferencia detectada:"
        ).pack(anchor="w", pady=(3, 6))

        txt_diferencia = ctk.CTkTextbox(
            contenido,
            height=95,
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"],
            fg_color=COLORES["blanco"],
            text_color=COLORES["texto"],
            font=("Arial", 13)
        )
        txt_diferencia.pack(fill="x", pady=(0, 13))

        self._etiqueta(
            contenido,
            "2. Fundamento u observaciones de la revisión:"
        ).pack(anchor="w", pady=(2, 6))

        txt_observaciones = ctk.CTkTextbox(
            contenido,
            height=105,
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"],
            fg_color=COLORES["blanco"],
            text_color=COLORES["texto"],
            font=("Arial", 13)
        )
        txt_observaciones.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            contenido,
            text=(
                "Importante: esta operación no modifica automáticamente "
                "los registros originales del menor. El resultado se muestra "
                "en esta ventana; la base de datos actual no contempla guardar "
                "un historial de aclaraciones."
            ),
            font=("Arial", 11),
            text_color=COLORES["secundario"],
            wraplength=680,
            justify="left"
        ).pack(anchor="w", pady=(0, 12))

        resultado = ctk.CTkLabel(
            contenido,
            text=(
                "Después de revisar la información, seleccione si la "
                "diferencia pudo aclararse o si debe quedar pendiente."
            ),
            font=("Arial", 12),
            text_color=COLORES["secundario"],
            fg_color=COLORES["blanco"],
            corner_radius=8,
            wraplength=660,
            justify="left"
        )
        resultado.pack(fill="x", pady=(0, 12), padx=2, ipady=10)

        def finalizar_aclaracion(estado):

            diferencia = txt_diferencia.get("1.0", "end").strip()
            observaciones = txt_observaciones.get("1.0", "end").strip()

            if not diferencia:
                resultado.configure(
                    text="Escriba primero cuál es la diferencia detectada.",
                    fg_color=COLORES["azul"],
                    text_color=COLORES["texto"]
                )
                return

            if not observaciones:
                resultado.configure(
                    text=(
                        "Agregue el fundamento o las observaciones de la "
                        "revisión antes de indicar el resultado."
                    ),
                    fg_color=COLORES["azul"],
                    text_color=COLORES["texto"]
                )
                return

            if estado == "aclarada":
                texto_resultado = (
                    "RESULTADO: DIFERENCIA ACLARADA\n\n"
                    "La recepcionista determinó que la información pudo "
                    "aclararse con los datos revisados."
                )
                color_resultado = COLORES["menta"]
            else:
                texto_resultado = (
                    "RESULTADO: PENDIENTE DE CONFIRMACIÓN\n\n"
                    "La información disponible no fue suficiente para "
                    "aclarar la diferencia."
                )
                color_resultado = "#FFF0CC"

            resultado.configure(
                text=(
                    f"{texto_resultado}\n\n"
                    f"Diferencia detectada: {diferencia}\n\n"
                    f"Fundamento u observaciones: {observaciones}\n\n"
                    "Los registros originales permanecen sin cambios."
                ),
                fg_color=color_resultado,
                text_color=COLORES["texto"],
                justify="left"
            )

        botones_resultado = ctk.CTkFrame(
            contenido,
            fg_color="transparent"
        )
        botones_resultado.pack(pady=(2, 12))

        self._boton(
            botones_resultado,
            "Diferencia aclarada",
            lambda: finalizar_aclaracion("aclarada"),
            COLORES["menta"],
            190
        ).pack(side="left", padx=6)

        self._boton(
            botones_resultado,
            "Dejar pendiente",
            lambda: finalizar_aclaracion("pendiente"),
            COLORES["lavanda"],
            170
        ).pack(side="left", padx=6)

        self._boton(
            contenido,
            "Cerrar",
            ventana.destroy,
            COLORES["blanco"],
            130
        ).pack(pady=(0, 8))

    def _consultar_datos_desde_aclaracion(self, ventana_aclaracion):

        contexto = self._obtener_contexto_menor_seleccionado()

        if contexto is None:
            return

        self._ventana_informacion(
            "Información relacionada · CU-04",
            self._formatear_contexto_menor(contexto),
            padre=ventana_aclaracion
        )

    def _ventana_informacion(self, titulo, contenido, padre=None):

        padre = padre or self

        ventana = ctk.CTkToplevel(padre)
        ventana.title("Pequeños Exploradores")
        ventana.geometry("560x520")
        ventana.minsize(480, 400)
        ventana.configure(fg_color=COLORES["fondo"])
        ventana.transient(padre)
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text=titulo,
            font=("Arial", 20, "bold"),
            text_color=COLORES["texto"]
        ).pack(anchor="w", padx=20, pady=(20, 10))

        texto = ctk.CTkTextbox(
            ventana,
            corner_radius=10,
            fg_color=COLORES["blanco"],
            border_width=1,
            border_color=COLORES["borde"],
            text_color=COLORES["texto"],
            font=("Arial", 12)
        )

        texto.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        texto.insert("1.0", contenido)
        texto.configure(state="disabled")

        self._boton(
            ventana,
            "Cerrar",
            ventana.destroy,
            COLORES["lavanda"],
            140
        ).pack(pady=15)


# =====================================================
# INICIAR APLICACION
# =====================================================

def iniciar_aplicacion(usuario):

    aplicacion = VentanaPrincipal(usuario)
    aplicacion.mainloop()