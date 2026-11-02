# Sistema de Gestión de la Guardería “Pequeños Exploradores”

**Ingeniería de Software — Unidad 3, Evidencia 1**  
**Equipo 14**

**Integrantes:**
- Ayala Esquivel Oscar Zabdiel
- Salazar Paredes Alejandro

## 1. Descripción del proyecto

“Pequeños Exploradores” es un sistema de gestión para una guardería, diseñado para apoyar al personal en el registro y comunicación de avisos e indicaciones, la consulta de información de los menores y la verificación de las personas autorizadas para recogerlos.

Se desarrollará como una aplicación de escritorio, procurando que su interfaz sea sencilla, organizada y fácil de utilizar.

## 2. Tecnologías utilizadas

- **Lenguaje:** Python 3.13.7.
- **Interfaz gráfica:** CustomTkinter 6.0.0.
- **Entorno de desarrollo:** Visual Studio Code.
- **Base de datos:** MySQL Server 9.5.0.
- **Administración de la BD:** MySQL Workbench.
- **Conexión Python–MySQL:** mysql-connector-python 26.10.0.
- **Configuración local:** python-dotenv 1.2.4.
- **Control de versiones:** Git, GitHub y GitHub Desktop.

## 3. Estructura del proyecto

```text
Pequenos_Exploradores/
├── app/
│   ├── main.py
│   ├── database/
│   │   └── conexion.py
│   ├── interfaces/
│   └── services/
├── database/
│   ├── schema.sql
│   └── datos_prueba.sql
├── docs/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

La carpeta `app` contiene el código de la aplicación. La carpeta `database` contiene los scripts para preparar MySQL. El archivo `requirements.txt` registra las dependencias necesarias para ejecutar el proyecto.

## 4. Preparación del entorno

Para ejecutar el proyecto en otra computadora se necesita Python 3.13, MySQL Server y las dependencias indicadas.

**Paso 1.** Descargar el repositorio y abrir su carpeta en Visual Studio Code.

**Paso 2.** Crear un entorno virtual desde la terminal:

```powershell
py -m venv .venv
```

**Paso 3.** Activar el entorno virtual en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

**Paso 4.** Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

Si PowerShell bloquea la activación del entorno, se puede habilitar temporalmente para la terminal actual mediante:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Después se repite el comando de activación.

## 5. Creación de la base de datos

La base de datos se llama `pequenos_exploradores` y se implementó a partir del modelo relacional corregido de U2-E2.

El mecanismo utilizado para crearla es el script `database/schema.sql`. No se emplean migraciones adicionales.

**Procedimiento:**

1. Abrir MySQL Workbench.
2. Conectarse a MySQL Server con un usuario que tenga permisos para crear bases de datos y tablas.
3. Abrir `database/schema.sql`.
4. Ejecutar todas sus instrucciones en la conexión activa.
5. Actualizar la lista de esquemas para comprobar que se creó `pequenos_exploradores`.
6. Verificar que aparezcan las ocho tablas del modelo.

Las tablas son:

- `Tutor`
- `Menor`
- `TutorMenor`
- `Recepcionista`
- `Educadora`
- `Aviso`
- `PersonaAutorizada`
- `AutorizacionRetiro`

Para comprobar su creación se puede ejecutar:

```sql
USE pequenos_exploradores;
SHOW TABLES;
```

El diseño utiliza claves primarias y foráneas para mantener las relaciones entre los registros. En particular, `Aviso` incluye una clave foránea compuesta hacia `TutorMenor`, que permite validar la asociación entre tutor y menor.

## 6. Datos ficticios para la demostración

El archivo `database/datos_prueba.sql` contiene instrucciones para insertar datos ficticios.

Para utilizarlos:

1. Abrir el script en MySQL Workbench.
2. Ejecutarlo en el servidor donde se creó la base de datos.
3. Consultar la tabla `Menor` mediante:

```sql
SELECT idMenor, nombreCompleto
FROM Menor
ORDER BY idMenor;
```

En una base de datos recién preparada con estos scripts deben aparecer dos menores de demostración:

- Menor ficticio A.
- Menor ficticio B.

Estos registros se utilizan únicamente con fines académicos; no contienen información personal real.

## 7. Configuración de la conexión

El proyecto utiliza variables de entorno para configurar la conexión entre Python y MySQL.

Se debe copiar el archivo `.env.example`, guardarlo como `.env` en la carpeta principal del proyecto y completar los valores correspondientes al servidor local.

Ejemplo de configuración:

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3305
DB_USER=root
DB_PASSWORD=
DB_NAME=pequenos_exploradores
```

El puerto `3305` corresponde al entorno local utilizado durante el desarrollo. En otra computadora debe indicarse el puerto real del servidor MySQL.

El usuario y la contraseña deben sustituirse por credenciales válidas del entorno donde se ejecute el proyecto.

**Importante:** `.env` contiene información privada y no debe publicarse en GitHub. El repositorio solamente incluye `.env.example`, sin contraseñas reales.

## 8. Ejecución de la aplicación

Con el entorno virtual activado, las dependencias instaladas, la base de datos preparada y el archivo `.env` configurado, ejecutar:

```powershell
python app/main.py
```

Se abrirá una ventana de escritorio creada con CustomTkinter.

En la versión técnica de U3-E1, la ventana incluye el botón **“Consultar menores de prueba”**.

Al presionarlo, la aplicación ejecuta una consulta a MySQL y muestra los registros ficticios almacenados en la tabla `Menor`.

También es posible ejecutar la prueba desde la terminal:

```powershell
python app/database/conexion.py
```

## 9. Demostración técnica realizada

Durante U3-E1 se comprobó que:

- El proyecto se ejecuta correctamente en Python.
- CustomTkinter permite abrir una ventana gráfica.
- MySQL contiene las ocho tablas implementadas.
- Los datos ficticios se almacenan en la base de datos.
- Python establece una conexión con MySQL mediante `mysql-connector-python`.
- La aplicación ejecuta una consulta real y recupera dos registros ficticios.

La operación utilizada es:

```sql
SELECT idMenor, nombreCompleto
FROM Menor
ORDER BY idMenor;
```

El archivo `app/database/conexion.py` realiza la consulta y `app/main.py` presenta los resultados en la interfaz gráfica.

## 10. Estado actual y trabajo pendiente

**Completado en U3-E1:**

- Preparación del entorno de desarrollo.
- Organización inicial del proyecto.
- Instalación de dependencias.
- Implementación de la base de datos.
- Creación de scripts SQL.
- Inserción de datos ficticios.
- Demostración de conexión entre Python y MySQL.
- Preparación del repositorio y su documentación.

**Pendiente para las siguientes etapas:**

- Implementar los casos de uso aprobados.
- Desarrollar las interfaces definitivas conforme a los prototipos de U2-E3.
- Integrar las funciones del sistema.
- Completar las comprobaciones y la documentación de las siguientes evidencias.

Los prototipos de U2-E3 contemplan colores pastel, elementos decorativos de ositos y controles adecuados para el personal de la guardería.

La ventana presentada en U3-E1 es únicamente una demostración técnica y no representa la interfaz definitiva del sistema.

## 11. Control de versiones y colaboración

El proyecto utiliza Git para registrar los cambios y GitHub para compartir el repositorio entre los integrantes del equipo.

GitHub Desktop facilita la creación de commits, la consulta del historial y la sincronización de los archivos.

El archivo `.gitignore` evita incorporar al repositorio contraseñas, entornos virtuales y archivos temporales.

Cada integrante deberá registrar sus aportaciones mediante commits identificables y comprobar que el proyecto siga ejecutándose después de integrar los cambios.