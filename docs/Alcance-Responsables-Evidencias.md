# Sistema de Gestión de la Guardería "Pequeños Exploradores"

## Documento de alcance, responsables y referencias de evidencias

**Equipo:** 14\
**Repositorio:**
[Pequenos_Exploradores](https://github.com/OscarAEZ/Pequenos_Exploradores)\
**Rama de trabajo:** `main`\
**Versión de referencia:** [Commit 66471fb -- Preparar base técnica y
documentación
U3-E1](https://github.com/OscarAEZ/Pequenos_Exploradores/commit/66471fb7f33a99b798126088154cde123644bd78)

------------------------------------------------------------------------

## 1. Propósito del documento

Este archivo concentra el alcance funcional considerado para la
integración del sistema, la distribución de responsabilidades entre los
integrantes del Equipo 14 y las referencias de los archivos y evidencias
disponibles en el repositorio.

La prioridad indicada para cada caso de uso organiza el desarrollo; no
significa que las funcionalidades de prioridad media puedan eliminarse
del alcance.


## 2. Alcance funcional

El sistema de gestión de la guardería "Pequeños Exploradores" contempla los siguientes casos de uso.

### Distribución de casos de uso

| Caso de uso | Nombre | Prioridad | Responsable |
|---|---|---|---|
| CU-01 | Registrar avisos e indicaciones | Alta | Oscar Zabdiel |
| CU-02 | Comunicar avisos de los menores | Alta | Oscar Zabdiel |
| CU-03 | Consultar avisos recibidos | Media (propuesta) | Alejandro |
| CU-04 | Consultar información de los menores | Media | Alejandro |
| CU-05 | Mostrar reportes de personas autorizadas | Alta | Alejandro |
| CU-06 | Consultar personas autorizadas | Alta | Alejandro |
| CU-07 | Aclarar diferencias de información | Media | Oscar Zabdiel |

### Dependencias e integración

**CU-01. Registrar avisos e indicaciones**

Requiere las tablas Menor, Tutor, TutorMenor y Aviso. Debe seleccionarse un tutor asociado al menor y utilizar el identificador de la recepcionista obtenido de la sesión.

**CU-02. Comunicar avisos de los menores**

Depende de los avisos registrados mediante CU-01. La educadora participa como actor secundario en la comunicación.

**CU-03. Consultar avisos recibidos**

Depende de CU-01 y CU-02. Permite consultar avisos vinculados a la educadora. Se mantiene para conservar la continuidad CU-01 → CU-02 → CU-03 indicada por la docente. RF-09 es su requisito asociado y debe corroborarse específicamente su validación.

**CU-04. Consultar información de los menores**

Permite consultar información registrada de los menores sin modificarla. Puede apoyar a CU-07 cuando sea necesario revisar diferencias.

**CU-05. Mostrar reportes de personas autorizadas**

Es una función incluida obligatoriamente dentro de CU-06 mediante la relación `<<include>>`. Consulta nombres y estados de autorización, sin requerir una pantalla independiente.

**CU-06. Consultar personas autorizadas**

Permite seleccionar a un menor y visualizar las personas autorizadas para recogerlo y sus estados de autorización. Integra CU-05.

**CU-07. Aclarar diferencias de información**

Permite revisar diferencias en la información registrada. Cuando se requiere consultar datos del menor, se relaciona con CU-04 mediante `<<extend>>`. No modifica información automáticamente.

  -----------------------------------------------------------------------------------

### 2.1 Consideraciones del alcance

-   Se conserva CU-03 para respetar la continuidad funcional CU-01 →
    CU-02 → CU-03 señalada previamente por la docente.
-   RF-09 está asociado a CU-03, pero su incorporación formal debe
    corroborarse con la docente. Por ello, se registra como función
    propuesta pendiente de validación, sin presentarla como autorización
    ya concedida.
-   CU-05 se mantiene como comportamiento incluido en CU-06 mediante
    `<<include>>`; no se desarrolla como una pantalla o caso de uso
    independiente.
-   CU-04 puede apoyar a CU-07 mediante `<<extend>>` cuando sea
    necesario consultar información para aclarar una diferencia.
-   La prioridad media establece un orden de construcción y no
    representa la eliminación de esos casos de uso.


## 3. Responsables del equipo

El desarrollo del sistema de gestión de la guardería "Pequeños Exploradores" se distribuye entre los integrantes del Equipo 14. Cada integrante tiene asignados determinados casos de uso y es responsable de su elaboración, documentación, revisión e integración con el resto del sistema.

### 3.1 Oscar Zabdiel

**Casos de uso asignados:**

| ID | Caso de uso |
|---|---|
| CU-01 | Registrar avisos e indicaciones |
| CU-02 | Comunicar avisos de los menores |
| CU-07 | Aclarar diferencias de información |

**Responsabilidades:**

- Desarrollar y documentar los casos de uso asignados.
- Revisar el funcionamiento de las funcionalidades correspondientes.
- Verificar que los datos y procesos utilizados sean compatibles con la estructura general del sistema.
- Registrar sus modificaciones y avances en el repositorio del proyecto.

### 3.2 Alejandro

**Casos de uso asignados:**

| ID | Caso de uso |
|---|---|
| CU-03 | Consultar avisos recibidos |
| CU-04 | Consultar información de los menores |
| CU-05 | Mostrar reportes de personas autorizadas |
| CU-06 | Consultar personas autorizadas |

**Responsabilidades:**

- Desarrollar y documentar los casos de uso asignados.
- Revisar las relaciones y dependencias entre CU-03, CU-04, CU-05 y CU-06.
- Verificar que la consulta de información y los reportes correspondan al comportamiento establecido.
- Registrar sus modificaciones y avances en el repositorio del proyecto.

### 3.3 Responsabilidades compartidas

Ambos integrantes participan en la integración y revisión general del sistema mediante las siguientes actividades:

- Mantener la comunicación sobre los cambios realizados en sus respectivos módulos.
- Verificar la compatibilidad entre los casos de uso y sus dependencias.
- Mantener actualizada la documentación técnica y funcional.
- Registrar las aportaciones individuales mediante commits en GitHub.
- Revisar que las modificaciones no afecten el funcionamiento de otros componentes del proyecto.

La distribución de responsabilidades permite identificar las aportaciones de cada integrante y facilita el seguimiento del desarrollo e integración del sistema.



## 4. Referencias de evidencias del repositorio

El repositorio de GitHub contiene los archivos correspondientes a la estructura técnica y documental del sistema de gestión de la guardería "Pequeños Exploradores". A continuación, se presentan los enlaces que permiten consultar los componentes publicados y verificar los avances registrados.

### 4.1 Repositorio e historial de modificaciones

- **Repositorio principal:** permite consultar la estructura general del proyecto y sus archivos.
  [Abrir repositorio en GitHub](https://github.com/OscarAEZ/Pequenos_Exploradores)

- **Historial de commits:** permite revisar las modificaciones registradas por los integrantes del equipo.
  [Consultar historial de commits](https://github.com/OscarAEZ/Pequenos_Exploradores/commits/main/)

- **Commit de referencia U3-E1:** identifica la versión en la que se incorporaron los archivos de la base técnica y la documentación inicial.
  [Consultar commit 66471fb](https://github.com/OscarAEZ/Pequenos_Exploradores/commit/66471fb7f33a99b798126088154cde123644bd78)

### 4.2 Archivos principales del sistema

- **README.md:** contiene la descripción general del sistema, las tecnologías utilizadas, la estructura del proyecto y las instrucciones de preparación.
  [Consultar README.md](https://github.com/OscarAEZ/Pequenos_Exploradores/blob/main/README.md)

- **app/main.py:** archivo principal y punto de entrada de la aplicación.
  [Consultar main.py](https://github.com/OscarAEZ/Pequenos_Exploradores/blob/main/app/main.py)

- **app/database/conexion.py:** contiene la configuración y los procedimientos de conexión con MySQL.
  [Consultar conexion.py](https://github.com/OscarAEZ/Pequenos_Exploradores/blob/main/app/database/conexion.py)

### 4.3 Archivos de base de datos y configuración

- **database/schema.sql:** contiene las instrucciones SQL para crear la estructura de la base de datos y sus tablas.
  [Consultar schema.sql](https://github.com/OscarAEZ/Pequenos_Exploradores/blob/main/database/schema.sql)

- **database/datos_prueba.sql:** contiene los registros de prueba utilizados para preparar los datos de demostración.
  [Consultar datos_prueba.sql](https://github.com/OscarAEZ/Pequenos_Exploradores/blob/main/database/datos_prueba.sql)

- **requirements.txt:** especifica las dependencias necesarias para preparar el entorno de Python.
  [Consultar requirements.txt](https://github.com/OscarAEZ/Pequenos_Exploradores/blob/main/requirements.txt)

- **.env.example:** presenta las variables de entorno necesarias como referencia para configurar la conexión, sin publicar las credenciales privadas.
  [Consultar .env.example](https://github.com/OscarAEZ/Pequenos_Exploradores/blob/main/.env.example)

Las referencias anteriores permiten consultar directamente los archivos publicados y dar seguimiento a las modificaciones realizadas en el repositorio. Las capturas de ejecución y funcionamiento del sistema se documentarán por separado en el apartado 5.


## 5. Evidencias visuales previstas para la entrega

Para complementar la documentación del proyecto y respaldar su desarrollo, se contempla integrar las siguientes evidencias visuales:

### 5.1 Evidencias de funcionamiento

1. Captura de la aplicación ejecutándose desde `app/main.py`.
2. Captura de la consulta de registros de prueba desde la aplicación.
3. Captura de la estructura de la base de datos y las tablas creadas mediante `database/schema.sql`.
4. Captura de los registros de prueba cargados mediante `database/datos_prueba.sql`.

### 5.2 Evidencias del repositorio

5. Captura del repositorio de GitHub mostrando los archivos publicados y su estructura.
6. Captura del historial de commits para identificar las aportaciones realizadas por los integrantes.

### 5.3 Consideraciones

Las evidencias de funcionamiento y conexión con la base de datos quedan pendientes de integración hasta contar con el entorno de desarrollo configurado y disponible para realizar las pruebas correspondientes.

Las capturas del repositorio y del historial de modificaciones podrán incorporarse conforme se registren los avances de cada integrante.

Este apartado establece las evidencias previstas para respaldar la entrega y no implica que todas las pruebas o capturas hayan sido realizadas.

## 6. Referencia del alcance académico

La organización funcional se relaciona con los entregables previos del
Equipo 14:

-   **U2-E1:** arquitectura 4+1 y casos de uso.
-   **U2-E2:** modelo relacional corregido de ocho tablas.
-   **U2-E3:** matriz de trazabilidad, wireframes y prototipos de CU-01
    y CU-06.

## 7. Registro de cambios y aportación del colaborador

**Integrante:** Alejandro  
**Equipo:** 14  
**Proyecto:** Sistema de Gestión de la Guardería "Pequeños Exploradores"

### 7.1 Actividades realizadas

Como parte de la colaboración en la elaboración del documento U3-E1, se realizaron las siguientes modificaciones:

1. **Revisión del alcance funcional:** se reorganizó la presentación de los casos de uso CU-01 a CU-07, mejorando la identificación de sus nombres, prioridades, responsables y dependencias.

2. **Actualización de responsabilidades:** se mejoró la distribución de actividades entre los integrantes del equipo, identificando los casos de uso correspondientes a cada uno y las responsabilidades compartidas.

3. **Organización de referencias del repositorio:** se estructuraron los enlaces de GitHub para facilitar la consulta de los archivos principales, scripts de base de datos, configuración del proyecto e historial de modificaciones.

4. **Revisión de evidencias visuales:** se reorganizó la relación de capturas previstas para la entrega, diferenciando las evidencias disponibles de aquellas que todavía están pendientes de generar.

5. **Revisión de la documentación general:** se mejoró la organización y presentación del contenido para facilitar su lectura, consulta y seguimiento por parte de los integrantes y de la docente.

### 7.2 Resultado de la colaboración

Las modificaciones contribuyen a mejorar la claridad y organización de la documentación del proyecto, permiten identificar las responsabilidades individuales y facilitan el seguimiento de los avances registrados en el repositorio.

La aportación corresponde a actividades de revisión, organización y actualización documental. No implica que se hayan realizado pruebas de ejecución o modificaciones al código fuente desde el equipo del colaborador.

### 7.3 Registro de la aportación
Los cambios realizados en este documento se incorporan al repositorio mediante un commit desde la cuenta de GitHub del colaborador, permitiendo identificar su participación y consultar las modificaciones en el historial del proyecto.

------------------------------------------------------------------------

**Equipo 14 -- Sistema de Gestión de la Guardería "Pequeños
Exploradores"**\
**Documento de apoyo para la organización e integración del proyecto
U3-E1.**
