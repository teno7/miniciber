
CREATE TABLE Computadoras (
    nombre VARCHAR(15) UNIQUE PRIMARY KEY, 
    mac VARCHAR(17) UNIQUE, 
    ip VARCHAR(15) UNIQUE
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

CREATE TABLE Tarifa(
    Minutos INTEGER PRIMARY KEY,
    Cobro REAL
); /* !Fin */
