
-- Guardería Pequeños Exploradores
-- Equipo 14
-- U3-E1: Datos ficticios para pruebas

USE pequenos_exploradores;

-- Registrar dos menores ficticios
-- Evitar duplicarlos si se ejecuta otra vez

INSERT INTO Menor (nombreCompleto)
SELECT 'Menor ficticio A'
WHERE NOT EXISTS (
    SELECT 1 FROM Menor
    WHERE nombreCompleto = 'Menor ficticio A'
);

INSERT INTO Menor (nombreCompleto)
SELECT 'Menor ficticio B'
WHERE NOT EXISTS (
    SELECT 1 FROM Menor
    WHERE nombreCompleto = 'Menor ficticio B'
);
