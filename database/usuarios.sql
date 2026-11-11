-- =====================================================
-- PEQUENOS EXPLORADORES
-- Usuarios para separar el acceso de Recepcionista y Educadora
-- Ejecutar despues de database/schema.sql y datos_prueba.sql
-- =====================================================

USE pequenos_exploradores;

CREATE TABLE IF NOT EXISTS Usuario (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    nombreUsuario VARCHAR(60) NOT NULL,
    passwordHash VARCHAR(255) NOT NULL,
    rol ENUM('recepcionista', 'educadora') NOT NULL,
    idRecepcionista INT NULL,
    idEducadora INT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    fechaCreacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_usuario_nombre UNIQUE (nombreUsuario),
    CONSTRAINT uq_usuario_recepcionista UNIQUE (idRecepcionista),
    CONSTRAINT uq_usuario_educadora UNIQUE (idEducadora),

    CONSTRAINT fk_usuario_recepcionista
        FOREIGN KEY (idRecepcionista)
        REFERENCES Recepcionista(idRecepcionista),

    CONSTRAINT fk_usuario_educadora
        FOREIGN KEY (idEducadora)
        REFERENCES Educadora(idEducadora),

    CONSTRAINT chk_usuario_rol_actor CHECK (
        (rol = 'recepcionista'
            AND idRecepcionista IS NOT NULL
            AND idEducadora IS NULL)
        OR
        (rol = 'educadora'
            AND idEducadora IS NOT NULL
            AND idRecepcionista IS NULL)
    )
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;