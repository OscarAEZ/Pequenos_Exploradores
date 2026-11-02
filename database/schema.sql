
-- Guardería "Pequeños Exploradores"
-- Equipo 14 - Ingeniería de Software
-- U3-E1: Creación de la base de datos
-- Basado en el modelo corregido de U2-E2

CREATE DATABASE IF NOT EXISTS pequenos_exploradores
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

USE pequenos_exploradores;

-- 1. Tutores
CREATE TABLE IF NOT EXISTS Tutor (
    idTutor INT AUTO_INCREMENT PRIMARY KEY,
    nombreCompleto VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- 2. Menores
CREATE TABLE IF NOT EXISTS Menor (
    idMenor INT AUTO_INCREMENT PRIMARY KEY,
    nombreCompleto VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- 3. Recepcionistas
CREATE TABLE IF NOT EXISTS Recepcionista (
    idRecepcionista INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- 4. Educadoras
CREATE TABLE IF NOT EXISTS Educadora (
    idEducadora INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- 5. Personas autorizadas
CREATE TABLE IF NOT EXISTS PersonaAutorizada (
    idPersonaAutorizada INT AUTO_INCREMENT PRIMARY KEY,
    nombreCompleto VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- 6. Relación Tutor-Menor (N:M)
CREATE TABLE IF NOT EXISTS TutorMenor (
    idTutor INT NOT NULL,
    idMenor INT NOT NULL,

    PRIMARY KEY (idTutor, idMenor),

    CONSTRAINT fk_tutormenor_tutor
        FOREIGN KEY (idTutor)
        REFERENCES Tutor(idTutor),

    CONSTRAINT fk_tutormenor_menor
        FOREIGN KEY (idMenor)
        REFERENCES Menor(idMenor)
) ENGINE=InnoDB;

-- 7. Avisos e indicaciones
CREATE TABLE IF NOT EXISTS Aviso (
    idAviso INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(1000) NOT NULL,
    idTutor INT NOT NULL,
    idMenor INT NOT NULL,
    idRecepcionista INT NOT NULL,
    idEducadora INT NULL,

    CONSTRAINT fk_aviso_tutor_menor
        FOREIGN KEY (idTutor, idMenor)
        REFERENCES TutorMenor(idTutor, idMenor),

    CONSTRAINT fk_aviso_recepcionista
        FOREIGN KEY (idRecepcionista)
        REFERENCES Recepcionista(idRecepcionista),

    CONSTRAINT fk_aviso_educadora
        FOREIGN KEY (idEducadora)
        REFERENCES Educadora(idEducadora)
) ENGINE=InnoDB;

-- 8. Autorizaciones de retiro
CREATE TABLE IF NOT EXISTS AutorizacionRetiro (
    idAutorizacion INT AUTO_INCREMENT PRIMARY KEY,
    estadoAutorizacion VARCHAR(50) NOT NULL,
    idMenor INT NOT NULL,
    idPersonaAutorizada INT NOT NULL,

    CONSTRAINT fk_autorizacion_menor
        FOREIGN KEY (idMenor)
        REFERENCES Menor(idMenor),

    CONSTRAINT fk_autorizacion_persona
        FOREIGN KEY (idPersonaAutorizada)
        REFERENCES PersonaAutorizada(idPersonaAutorizada)
) ENGINE=InnoDB;
