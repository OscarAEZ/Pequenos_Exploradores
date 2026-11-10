
-- =====================================================
-- GUARDERIA "PEQUENOS EXPLORADORES"
-- EQUIPO 14
-- U3-E1: DATOS FICTICIOS PARA PRUEBAS
-- =====================================================

USE pequenos_exploradores;

START TRANSACTION;

-- =====================================================
-- 1. MENORES
-- =====================================================

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


-- =====================================================
-- 2. TUTORES
-- =====================================================

INSERT INTO Tutor (nombreCompleto)
SELECT 'Tutor ficticio A'
WHERE NOT EXISTS (
    SELECT 1 FROM Tutor
    WHERE nombreCompleto = 'Tutor ficticio A'
);

INSERT INTO Tutor (nombreCompleto)
SELECT 'Tutor ficticio B'
WHERE NOT EXISTS (
    SELECT 1 FROM Tutor
    WHERE nombreCompleto = 'Tutor ficticio B'
);


-- =====================================================
-- 3. RECEPCIONISTAS
-- =====================================================

INSERT INTO Recepcionista (nombre)
SELECT 'Recepcionista ficticia A'
WHERE NOT EXISTS (
    SELECT 1 FROM Recepcionista
    WHERE nombre = 'Recepcionista ficticia A'
);


-- =====================================================
-- 4. EDUCADORAS
-- =====================================================

INSERT INTO Educadora (nombre)
SELECT 'Educadora ficticia A'
WHERE NOT EXISTS (
    SELECT 1 FROM Educadora
    WHERE nombre = 'Educadora ficticia A'
);

INSERT INTO Educadora (nombre)
SELECT 'Educadora ficticia B'
WHERE NOT EXISTS (
    SELECT 1 FROM Educadora
    WHERE nombre = 'Educadora ficticia B'
);


-- =====================================================
-- 5. PERSONAS AUTORIZADAS
-- =====================================================

INSERT INTO PersonaAutorizada (nombreCompleto)
SELECT 'Persona autorizada ficticia A'
WHERE NOT EXISTS (
    SELECT 1 FROM PersonaAutorizada
    WHERE nombreCompleto = 'Persona autorizada ficticia A'
);

INSERT INTO PersonaAutorizada (nombreCompleto)
SELECT 'Persona autorizada ficticia B'
WHERE NOT EXISTS (
    SELECT 1 FROM PersonaAutorizada
    WHERE nombreCompleto = 'Persona autorizada ficticia B'
);

INSERT INTO PersonaAutorizada (nombreCompleto)
SELECT 'Persona autorizada ficticia C'
WHERE NOT EXISTS (
    SELECT 1 FROM PersonaAutorizada
    WHERE nombreCompleto = 'Persona autorizada ficticia C'
);


-- =====================================================
-- 6. RELACION TUTOR - MENOR
-- =====================================================

-- Tutor A relacionado con Menor A

INSERT INTO TutorMenor (idTutor, idMenor)
SELECT t.idTutor, m.idMenor
FROM Tutor t
JOIN Menor m
WHERE t.nombreCompleto = 'Tutor ficticio A'
AND m.nombreCompleto = 'Menor ficticio A'
AND NOT EXISTS (
    SELECT 1
    FROM TutorMenor tm
    WHERE tm.idTutor = t.idTutor
    AND tm.idMenor = m.idMenor
);


-- Tutor A relacionado con Menor B

INSERT INTO TutorMenor (idTutor, idMenor)
SELECT t.idTutor, m.idMenor
FROM Tutor t
JOIN Menor m
WHERE t.nombreCompleto = 'Tutor ficticio A'
AND m.nombreCompleto = 'Menor ficticio B'
AND NOT EXISTS (
    SELECT 1
    FROM TutorMenor tm
    WHERE tm.idTutor = t.idTutor
    AND tm.idMenor = m.idMenor
);


-- Tutor B relacionado con Menor A

INSERT INTO TutorMenor (idTutor, idMenor)
SELECT t.idTutor, m.idMenor
FROM Tutor t
JOIN Menor m
WHERE t.nombreCompleto = 'Tutor ficticio B'
AND m.nombreCompleto = 'Menor ficticio A'
AND NOT EXISTS (
    SELECT 1
    FROM TutorMenor tm
    WHERE tm.idTutor = t.idTutor
    AND tm.idMenor = m.idMenor
);


-- =====================================================
-- 7. AVISOS E INDICACIONES
-- =====================================================

-- Aviso recibido por la Educadora A

INSERT INTO Aviso (
    descripcion,
    idTutor,
    idMenor,
    idRecepcionista,
    idEducadora
)
SELECT
    'Aviso de prueba: el menor A sera recogido a las 13:00.',
    t.idTutor,
    m.idMenor,
    r.idRecepcionista,
    e.idEducadora
FROM Tutor t
JOIN Menor m
JOIN Recepcionista r
JOIN Educadora e
WHERE t.nombreCompleto = 'Tutor ficticio A'
AND m.nombreCompleto = 'Menor ficticio A'
AND r.nombre = 'Recepcionista ficticia A'
AND e.nombre = 'Educadora ficticia A'
AND NOT EXISTS (
    SELECT 1
    FROM Aviso a
    WHERE a.descripcion =
    'Aviso de prueba: el menor A sera recogido a las 13:00.'
    AND a.idMenor = m.idMenor
);


-- Aviso pendiente de comunicar

INSERT INTO Aviso (
    descripcion,
    idTutor,
    idMenor,
    idRecepcionista,
    idEducadora
)
SELECT
    'Aviso de prueba: indicacion alimentaria del menor B.',
    t.idTutor,
    m.idMenor,
    r.idRecepcionista,
    NULL
FROM Tutor t
JOIN Menor m
JOIN Recepcionista r
WHERE t.nombreCompleto = 'Tutor ficticio A'
AND m.nombreCompleto = 'Menor ficticio B'
AND r.nombre = 'Recepcionista ficticia A'
AND NOT EXISTS (
    SELECT 1
    FROM Aviso a
    WHERE a.descripcion =
    'Aviso de prueba: indicacion alimentaria del menor B.'
    AND a.idMenor = m.idMenor
);


-- Aviso recibido por la Educadora B

INSERT INTO Aviso (
    descripcion,
    idTutor,
    idMenor,
    idRecepcionista,
    idEducadora
)
SELECT
    'Aviso de prueba: observacion sobre el menor A.',
    t.idTutor,
    m.idMenor,
    r.idRecepcionista,
    e.idEducadora
FROM Tutor t
JOIN Menor m
JOIN Recepcionista r
JOIN Educadora e
WHERE t.nombreCompleto = 'Tutor ficticio B'
AND m.nombreCompleto = 'Menor ficticio A'
AND r.nombre = 'Recepcionista ficticia A'
AND e.nombre = 'Educadora ficticia B'
AND NOT EXISTS (
    SELECT 1
    FROM Aviso a
    WHERE a.descripcion =
    'Aviso de prueba: observacion sobre el menor A.'
    AND a.idMenor = m.idMenor
);


-- =====================================================
-- 8. AUTORIZACIONES DE RETIRO
-- =====================================================

-- Persona A autorizada para retirar al menor A

INSERT INTO AutorizacionRetiro (
    estadoAutorizacion,
    idMenor,
    idPersonaAutorizada
)
SELECT
    'Autorizada',
    m.idMenor,
    p.idPersonaAutorizada
FROM Menor m
JOIN PersonaAutorizada p
WHERE m.nombreCompleto = 'Menor ficticio A'
AND p.nombreCompleto = 'Persona autorizada ficticia A'
AND NOT EXISTS (
    SELECT 1
    FROM AutorizacionRetiro ar
    WHERE ar.idMenor = m.idMenor
    AND ar.idPersonaAutorizada = p.idPersonaAutorizada
);


-- Persona B pendiente de verificacion para el menor A

INSERT INTO AutorizacionRetiro (
    estadoAutorizacion,
    idMenor,
    idPersonaAutorizada
)
SELECT
    'Pendiente de verificacion',
    m.idMenor,
    p.idPersonaAutorizada
FROM Menor m
JOIN PersonaAutorizada p
WHERE m.nombreCompleto = 'Menor ficticio A'
AND p.nombreCompleto = 'Persona autorizada ficticia B'
AND NOT EXISTS (
    SELECT 1
    FROM AutorizacionRetiro ar
    WHERE ar.idMenor = m.idMenor
    AND ar.idPersonaAutorizada = p.idPersonaAutorizada
);


-- Persona C autorizada para retirar al menor B

INSERT INTO AutorizacionRetiro (
    estadoAutorizacion,
    idMenor,
    idPersonaAutorizada
)
SELECT
    'Autorizada',
    m.idMenor,
    p.idPersonaAutorizada
FROM Menor m
JOIN PersonaAutorizada p
WHERE m.nombreCompleto = 'Menor ficticio B'
AND p.nombreCompleto = 'Persona autorizada ficticia C'
AND NOT EXISTS (
    SELECT 1
    FROM AutorizacionRetiro ar
    WHERE ar.idMenor = m.idMenor
    AND ar.idPersonaAutorizada = p.idPersonaAutorizada
);


COMMIT;

-- =====================================================
-- FIN DE LOS DATOS DE PRUEBA
-- =====================================================

