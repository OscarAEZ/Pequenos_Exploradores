# Sistema de Gestión de la Guardería «Pequeños Exploradores»

**Ingeniería de Software — Unidad 3, Evidencias 1 y 2**

**Equipo 14**

### Integrantes

- Ayala Esquivel Oscar Zabdiel

- Salazar Paredes Alejandro

---

## 1. Descripción del proyecto

«Pequeños Exploradores» es un sistema de gestión para una guardería, desarrollado para apoyar las actividades del personal de recepción y las educadoras.

El sistema permite registrar y comunicar avisos e indicaciones sobre los menores, consultar información relacionada con ellos y verificar las personas autorizadas para recogerlos.

La aplicación se desarrolla como un programa de escritorio, con una interfaz gráfica sencilla y organizada, utilizando una estructura que separa las interfaces, los servicios y las operaciones de conexión con la base de datos.

El acceso al sistema se realiza mediante cuentas de usuario, diferenciando las funciones disponibles para recepción y educadoras.

## 2. Tecnologías utilizadas

| Tecnología | Versión | Uso en el proyecto |
|---|---|---|
| Python | 3.13.7 | Lenguaje de programación principal. |
| CustomTkinter | 6.0.0 | Desarrollo de interfaces gráficas. |
| Visual Studio Code | 1.146.0 (x64) | Entorno de desarrollo y edición del código. |
| MySQL Server | 9.5.0 | Sistema gestor de base de datos. |
| MySQL Workbench | No especificada | Administración y consulta de la base de datos. |
| mysql-connector-python | 26.10.0 | Conexión entre Python y MySQL. |
| python-dotenv | 1.2.4 | Administración de variables de entorno. |
| Git | 2.56.0.windows.4 | Control de versiones del proyecto. |
| GitHub | Servicio web | Alojamiento y colaboración en el repositorio. |
| GitHub Desktop | Versión no confirmada | Administración de commits y sincronización del repositorio. |

Las dependencias necesarias para ejecutar el sistema están registradas en `requirements.txt`. Las versiones indicadas corresponden al entorno utilizado durante el desarrollo del proyecto.

## 3. Estructura del proyecto

El proyecto se organiza en carpetas para mantener separado el código de la aplicación, las interfaces gráficas, los servicios y los archivos de la base de datos.

```text
Pequenos_Exploradores/
│
├── app/
│   ├── database/
│   │   └── conexion.py
│   │
│   ├── interfaces/
│   │   ├── recursos_guarderia/
│   │   ├── __init__.py
│   │   ├── login.py
│   │   ├── ventana_principal.py
│   │   └── ventana_educadora.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── autenticacion_service.py
│   │   └── guarderia_service.py
│   │
│   ├── crear_usuario.py
│   └── main.py
│
├── database/
│   ├── schema.sql
│   ├── datos_prueba.sql
│   └── usuarios.sql
│
├── docs/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

**Descripción de las carpetas principales:**

- `app/database/`: contiene la conexión de Python con MySQL.

- `app/interfaces/`: contiene las ventanas y componentes gráficos del sistema.

- `app/interfaces/recursos_guarderia/`: almacena imágenes, iconos y recursos visuales.

- `app/services/`: contiene las operaciones del sistema y las consultas SQL.

- `database/`: contiene los scripts para crear las tablas y preparar los datos de demostración.

- `docs/`: almacena documentación relacionada con el proyecto.

## 4. Requisitos para ejecutar el proyecto

Para utilizar el sistema en otra computadora se necesita:

- Python 3.13.

- MySQL Server.

- MySQL Workbench.

- Visual Studio Code (recomendado).

- Las dependencias registradas en `requirements.txt`.

También se requiere contar con acceso a la base de datos local y configurar correctamente sus credenciales.

## 5. Preparación del entorno de desarrollo

### Paso 1. Descargar el proyecto

Clonar el repositorio de GitHub o descargarlo como archivo ZIP.

Abrir la carpeta principal `Pequenos_Exploradores` desde Visual Studio Code.

### Paso 2. Crear el entorno virtual

Abrir una terminal de PowerShell y ejecutar:

```powershell

py -m venv .venv

```

### Paso 3. Activar el entorno virtual

```powershell

.\\.venv\Scripts\Activate.ps1

```

Si PowerShell bloquea la activación, ejecutar:

```powershell

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

```

Después repetir el comando de activación.

### Paso 4. Instalar las dependencias

Con el entorno virtual activado, ejecutar:

```powershell

python -m pip install --upgrade pip

```

Posteriormente:

```powershell

python -m pip install -r requirements.txt

```

Este procedimiento instala las bibliotecas necesarias para ejecutar la aplicación.

## 6. Creación de la base de datos

La base de datos del proyecto se llama `pequenos_exploradores`.

Su estructura se desarrolló tomando como referencia el modelo relacional corregido de la Unidad 2, Evidencia 2.

El modelo relacional contempla las siguientes ocho tablas:

1. `Tutor`

2. `Menor`

3. `TutorMenor`

4. `Recepcionista`

5. `Educadora`

6. `Aviso`

7. `PersonaAutorizada`

8. `AutorizacionRetiro`

Adicionalmente, se utiliza la tabla `Usuario` para administrar las cuentas de acceso al sistema.

### Procedimiento de creación

1. Abrir MySQL Workbench.

2. Conectarse al servidor MySQL local.

3. Abrir el archivo `database/schema.sql`.

4. Ejecutar las instrucciones para crear la base de datos y sus tablas.

5. Ejecutar `database/usuarios.sql` para preparar la tabla de usuarios, si todavía no está incluida en el esquema principal.

6. Ejecutar `database/datos_prueba.sql` para insertar los registros ficticios.

7. Actualizar la lista de esquemas y comprobar que la base de datos esté disponible.

Para verificar la creación se puede ejecutar:

```sql

USE pequenos_exploradores;

SHOW TABLES;

```

El diseño utiliza claves primarias y foráneas para mantener la integridad de los datos.

En particular, la tabla `Aviso` utiliza una relación compuesta con `TutorMenor`, permitiendo validar que el tutor esté relacionado con el menor al que corresponde el aviso.

## 7. Datos ficticios para las pruebas

El archivo `database/datos_prueba.sql` contiene registros de demostración utilizados durante el desarrollo y las pruebas del sistema.

Entre ellos se encuentran:

- Menor ficticio A.

- Menor ficticio B.

- Tutores ficticios.

- Recepcionistas y educadoras.

- Avisos e indicaciones.

- Personas autorizadas y sus estados de autorización.

Estos registros permiten probar las operaciones sin utilizar información personal real.

Para comprobar los menores registrados se puede ejecutar:

```sql

USE pequenos_exploradores;

SELECT idMenor, nombreCompleto

FROM Menor

ORDER BY idMenor;

```

## 8. Configuración de la conexión con MySQL

El sistema utiliza variables de entorno para establecer la conexión con MySQL.

En la carpeta principal se encuentra el archivo `.env.example`.

Se debe copiar este archivo, crear una copia llamada `.env` y completar los datos correspondientes al servidor local.

Ejemplo:

```dotenv

DB_HOST=127.0.0.1

DB_PORT=3305

DB_USER=root

DB_PASSWORD=TU_CONTRASEÑA

DB_NAME=pequenos_exploradores

```

**Importante:**

- El puerto `3305` corresponde al entorno local utilizado durante el desarrollo.

- En otra computadora debe configurarse el puerto real del servidor MySQL.

- El usuario y la contraseña deben corresponder a una cuenta válida.

- El archivo `.env` contiene información privada y no debe publicarse en GitHub.

- El repositorio solamente debe incluir `.env.example`, sin credenciales reales.

## 9. Creación de cuentas de usuario

El sistema cuenta con un módulo para crear cuentas de acceso para los dos roles disponibles:

- Recepcionista.

- Educadora.

Para crear una cuenta se debe ejecutar desde la carpeta principal del proyecto, con el entorno virtual activado:

```powershell

python -m app.crear_usuario

```

El programa solicitará:

1. Seleccionar el tipo de usuario.

2. Elegir el registro de la recepcionista o educadora correspondiente.

3. Escribir un nombre de usuario de al menos cuatro caracteres.

4. Introducir una contraseña de al menos ocho caracteres.

5. Confirmar la contraseña.

Una vez completado el procedimiento, el sistema registra la cuenta y permite utilizarla para iniciar sesión.

Las cuentas se relacionan con los registros existentes de recepción y educadoras en la base de datos.

## 10. Ejecución de la aplicación

Antes de iniciar el sistema se debe comprobar que:

- El entorno virtual esté activado.

- Las dependencias estén instaladas.

- MySQL Server se encuentre en ejecución.

- La base de datos esté creada.

- El archivo `.env` esté configurado correctamente.

- Exista una cuenta de usuario registrada.

Para iniciar la aplicación se ejecuta:

```powershell

python -m app.main

```

Se abrirá la ventana de inicio de sesión de «Pequeños Exploradores».

Después de introducir las credenciales, el sistema identifica el rol del usuario y muestra la interfaz correspondiente.

### Acceso de recepción

La recepcionista cuenta con funciones para:

- Registrar avisos e indicaciones.

- Comunicar avisos a las educadoras.

- Consultar personas autorizadas para recoger a los menores.

- Consultar información relacionada con los menores.

- Aclarar diferencias de información.

### Acceso de educadoras

La educadora cuenta con funciones para:

- Consultar los avisos que le fueron comunicados.

- Visualizar la información del menor relacionada con cada aviso.

- Actualizar la información mostrada mediante la consulta de avisos recibidos.

## 11. Casos de uso y funcionalidades

La aplicación incorpora las funciones correspondientes a los casos de uso definidos en la documentación del proyecto.

| Caso de uso | Funcionalidad |

|---|---|

| CU-01 | Registrar avisos e indicaciones. |

| CU-02 | Comunicar avisos de los menores. |

| CU-03 | Consultar avisos recibidos por la educadora. |

| CU-04 | Consultar información de los menores. |

| CU-06 | Consultar personas autorizadas. |

| CU-07 | Aclarar diferencias de información. |

**Funcionamiento de CU-07:**

Este caso de uso permite que la recepcionista revise diferencias entre la información proporcionada y los datos registrados en el sistema.

Para realizar la revisión puede consultar los antecedentes del menor mediante CU-04, comparar la información disponible y determinar si la diferencia pudo aclararse o si necesita una verificación adicional.

Los resultados posibles son:

- ****Diferencia aclarada:**** cuando se logra determinar cuál información es correcta.

- ****Pendiente de confirmación:**** cuando no existe información suficiente para resolver la diferencia.

De acuerdo con la trazabilidad del proyecto, CU-07 utiliza información previamente almacenada, pero no contempla guardar un historial independiente de aclaraciones. Por ello, el resultado de la revisión se presenta en la interfaz y los registros originales permanecen sin modificaciones.

## 12. Estado actual del proyecto

La versión actual cuenta con una aplicación de escritorio que integra la conexión con MySQL, el acceso mediante cuentas de usuario y las interfaces correspondientes a recepción y educadoras.

### Funcionalidades desarrolladas

- Organización del proyecto mediante módulos.

- Conexión entre Python y MySQL.

- Inicio de sesión.

- Creación de cuentas para recepcionistas y educadoras.

- Identificación de roles.

- Interfaz principal de recepción.

- Interfaz de educadoras.

- Registro y comunicación de avisos.

- Consulta de avisos recibidos.

- Consulta de personas autorizadas.

- Consulta de información relacionada con los menores.

- Interfaz para aclarar diferencias de información.

### Trabajo pendiente y mejoras

- Completar las pruebas de funcionamiento de todos los casos de uso.

- Verificar la persistencia de las operaciones que modifican datos.

- Revisar el manejo de errores y validaciones.

- Continuar ajustando las interfaces conforme a los prototipos de U2-E3.

- Completar las evidencias y documentación de las siguientes etapas.

## 13. Control de versiones y colaboración

El proyecto utiliza Git y GitHub para mantener un control de los cambios realizados durante el desarrollo.

GitHub Desktop facilita la administración del repositorio y permite:

- Consultar archivos modificados.

- Identificar archivos nuevos.

- Crear commits.

- Consultar el historial de versiones.

- Sincronizar los cambios con GitHub.

Cada integrante debe registrar sus modificaciones mediante commits con mensajes descriptivos.

Antes de compartir los cambios se recomienda comprobar que el proyecto continúe ejecutándose correctamente.

El archivo `.gitignore` evita incorporar al repositorio archivos temporales, entornos virtuales y credenciales privadas.

Entre los archivos que no deben publicarse se encuentran:

- `.env`

- `.venv/`

- `__pycache__/`

- Archivos `.pyc`

---

**Proyecto académico: Sistema de Gestión de la Guardería «Pequeños Exploradores».**

**Ingeniería de Software — Unidad 3, Evidencias 1 y 2.**

**Equipo 14.**
