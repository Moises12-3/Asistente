--create database DB_Asistente
--go

-- Crear una tabla llamada 'Ejemplo' con ID autoincrementable
--create schema asistent

use DB_Asistente
go
CREATE TABLE Accion (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Pronuncia VARCHAR(100),
    Accion VARCHAR(100),
    Palabra VARCHAR(100)
);




CREATE TABLE Chiste (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Pronuncia VARCHAR(max),
    Accion VARCHAR(max),
    Palabra VARCHAR(max)
);

