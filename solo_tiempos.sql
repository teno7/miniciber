
CREATE TABLE Computadoras (
    Nombre VARCHAR(15) UNIQUE PRIMARY KEY, 
    MacID VARCHAR(17) UNIQUE, 
    IP VARCHAR(15) UNIQUE
); /* !Fin */

CREATE TABLE Alquiler(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(15), 
    inicio REAL,
    fin REAL, 
    limite REAL,
    muerto REAL,
    abono REAL
); /* !Fin */
