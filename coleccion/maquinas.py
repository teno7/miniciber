#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Eufracio Tenoch Sedano Rosales
tenochsr@gmail.com
"""
from definiciones import Sistema
from time import time, strftime, localtime
import math, re, sys, json

s = Sistema()
db = s.db


class Computadora:
    ENC = 0
    APG = 1
    
    def __init__(self, nombre=None, mac=None, ip=None):
        self.__nombre = nombre
        self.__mac = mac
        self.__ip = ip
        self.__alquiler = None
        self.estado = self.APG
        if nombre and mac and ip:
            self.__guardar()
    
    def set_nombre(self, n):
        sqla = "update Alquiler set nombre={} where nombre={}"
        sqlc = "update Computadoras set nombre={} where nombre={}"
        sqla = sqla.format(n, self.__nombre)
        sqlc = sqlc.format(n, self.__nombre)
        cur = db.cursor()
        cur.execute(sqla)
        cur.execute(sqlc)
        db.commit()
        cur.close()
        self.__nombre = n
    
    def get_nombre(self):
        return self.__nombre
    
    def set_mac(self, mac):
        self.__mac = mac
        self.__guardar()
        
    def get_mac(self):
        return self.__mac
    
    def set_ip(self, ip):
        self.__ip = ip
        self.__guardar()
    
    def get_ip(self):
        return self.__ip
    
    @property
    def alquiler(self):
        sql = "select * from Alquiler where fin<>0 and nombre='{}' limit 1"
        sql = sql.format(self.nombre)
        cur = db.cursor()
        self.__alquiler = None
        for row in cur.execute(sql):
            self.__alquiler = Alquiler()
            self.__alquiler.set_row(row)
        return self.__alquiler
    
    @property
    def estado_alquiler(self):
        return "LIBRE" if self.alquiler is None else "OCUPADA"
    
    @property
    def tupla(self):
        if self.alquiler:
            return (self.nombre, self.estado, self.__alquiler.inicio, 
                    self.__alquiler.limite, "$ "+ str(self.__alquiler.abono),
                    self.__alquiler.tiempo)
        else:
            return (self.nombre, self.estado, "00:00", "00:00", "$ 0.0", "00:00")
        
    def serialize(self):
        c = {}
        c["NOMBRE"] = self.nombre
        c["MAC"] = self.mac
        c["IP"] = self.ip
        alq = None
        if self.alquiler:
            alq = {"ID": self.__alquiler.id, 
                   "NOMBRE": self.__alquiler.nombre,
                   "INICIO": self.__alquiler.inicio,
                   "FIN": self.__alquiler.fin,
                   "LIMITE": self.__alquiler.limite,
                   "MUERTO": self.__alquiler.muerto,
                   "ABONO": self.__alquiler.abono}
        c["ALQUILER"] = alq
        return json.dumps(c)
    
    def load(self, pack):
        c = json.loads(pack)
        self.nombre = c["NOMBRE"]
        self.mac = c["MAC"]
        self.ip = c[]
        
    def iniciar(self, limite=0):
        if self.alquiler:
            self.error = "Maquina en uso"
            return False
        else:
            a = Alquiler()
            a.nombre = self.nombre
            a.limite = limite
            return True
    
    def detener(self):
        if self.alquiler:
            self.alquiler.fin = 1
    
    def historial(self):
        sql = "select * from Alquiler where fin=0 and nombre='{}' limit 10"
        sql = sql.format(self.nombre)
        cur = db.cursor()
        lista = []
        for row in cur.execute(sql):
            a = Alquiler()
            a.set_row(row)
            lista.append(a)
        return lista
    
    def set_row(self, row):
        self.nombre = row[0]
        self.mac = row[1]
        self.ip = row[2]
        
    def encender(self):
        pass
    
    def apagar(self):
        pass
    
    def __guardar(self):
        sql = "REPLACE INTO Computadoras (nombre, mac, ip) "
        sql += "values('{}', '{}', '{}')"
        sql = sql.format(self.nombre, self.mac, self.ip)
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        cur.close()
    
    nombre = property(self.get_nombre, self.set_nombre)
    mac = property(self.get_mac, self.set_mac)
    ip = property(self.get_ip, self.set_ip)


class ListaComputadoras:
    
    def __init__(self):
        self.__lista = []
        self.alquileres = ListaAlquiler()
        
    def __getitem__(self, n):
        for c in self.__lista:
            if c.nombre == n
            return c
        return None
    
    def nuevo(self, nombre, mac, ip):
        c = Computadora(nombre, mac, ip)
        self.__refresh()
        
    def __refresh(self):
        sql = "select * from Computadoras;"
        self.__lista = []
        cur = db.cursor()
        for row in cur.execute(sql):
            a = Computadora()
            a.set_row(row)
            self.__lista.append(a)
        cur.close()
        