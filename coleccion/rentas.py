#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Eufracio Tenoch Sedano Rosales
tenochsr@gmail.com
"""
from definiciones import Sistema
from time import time, strftime, localtime
import math

s = Sistema()
db = s.db


class Alquiler:

    def __init__(self):
        self.id = None
        self.__nombre = ""
        self.__inicio = 0.0
        self.__fin = 0.0
        self.__limite = 0.0 #tambien va a ser una hora como inicio y fin
        self.__muerto = 0.0
        self.__abono = 0.0

    def set_nombre(self, n):
        self.__nombre = n
        self.__guardar()

    def get_nombre(self):
        return self.__nombre

    def set_inicio(self, minutos):
        self.__inicio = time()
        if minutos > 0:
            self.limite = minutos
        if self.__fin > 0:
            self.__muerto += time()-self.__fin
        self.__guardar()

    def get_inicio(self):
        return self.get_htime(self.__inicio)

    def set_fin(self, f):
        if f == 1:
            self.__fin = time()
        else:
            self.__fin = 0
        self.__guardar()

    def get_fin(self):
        return self.get_htime(self.__fin)

    def set_limite(self, minutos):
        self.__limite = minutos * 60
        self.__guardar()

    def sumar_limite(self, minutos):
        self.__limite += minutos*60
        self.__guardar()

    def get_limite(self):
        if self.__limite == 0:
            return "LIBRE"
        lim = self.__inicio + self.__limite
        if lim < time() or self.__fin > 0:
            return "TERMINADO"
        else:
            return self.get_htime(lim-time())

    def set_muerto(self, m):
        self.__muerto = m
        self.__guardar()

    def get_muerto(self):
        return self.__muerto

    def set_abono(self, a):
        self.__abono = a
        self.__guardar()

    def get_abono(self):
        return self.__abono

    def get_htime(self, t):
        if t < 60*60*24:
            minutos = math.floor(t/60)
            segundos = math.floor(t - minutos*60)
            horas = math.floor(minutos/60)
            minutos -= horas*60
            if segundos < 10:
                segundos = "0" + str(segundos)
            if minutos < 10:
                minutos = "0" + str(minutos)
            if horas < 10:
                horas = "0" + str(horas)
            return "{0}:{1}:{2}".format(horas, minutos, segundos)
        return strftime("%H:%M:%S", localtime(t))

    @property
    def tiempo(self):
        if self.__fin:
            f = self.__fin
        else:
            f = time()
        return self.get_htime(f-self.__inicio)


    def set_row(self, row):
        self.id = row[0]
        self.__nombre = row[1]
        self.__inicio = row[2]
        self.__fin = row[3]
        self.__limite = row[4]
        self.__muerto = row[5]
        self.__abono = row[6]

    def eliminar(self):
        if self.id:
            sql = "delete from Alquiler where id={};".format(self.id)
            cur = db.cursor()
            cur.execute(sql)
            db.commit()
            cur.close()

    def __guardar(self):
        if self.id:
            sql = "replace into Alquiler(id, nombre, inicio, fin, limite, "
            sql += "muerto, abono) values('{0}', '{1}', '{2}', '{3}', '{4}', "
            sql += "'{5}', '{6}');"
            sql = sql.format(self.id, self.__nombre, self.__inicio, self.__fin,
                             self.__limite, self.__muerto, self.__abono)
        else:
            sql = "insert into Alquiler(nombre, inicio, fin, limite, "
            sql += "muerto, abono) values('{0}', '{1}', '{2}', '{3}', '{4}', "
            sql += "'{5}');"
            sql = sql.format(self.__nombre, self.__inicio, self.__fin,
                             self.__limite, self.__muerto, self.__abono)
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        cur.close()

    nombre = property(get_nombre, set_nombre)
    inicio = property(get_inicio, set_inicio)
    fin = property(get_fin, set_fin)
    limite = property(get_limite, set_limite)
    muerto = property(get_muerto, set_muerto)
    abono = property(get_abono, set_abono)


class ListaAlquiler: #Regresar lista de computadoras con su respectivo alquiler

    def __init__(self):
        self.__ver_activos = True
        self.__lista = []
        self.__refresh()
        self.error = ""

    def __getitem__(self, x):
        for a in self.lista():
            if a.nombre == x:
                return a
        return None

    def lista(self):
        self.__refresh()
        return self.__lista

    def lista_pc(self):
        a = []
        for i in self.lista():
            a.append(i.nombre)
        return a

    def nuevo(self, pc, limite=0, abono=0):
        if pc in self.lista_pc():
            print("ya esta")
            self.error = "Maquina no disponible"
            return False
        a = Alquiler()
        a.nombre = pc
        self.__refresh()
        maq = self[pc]
        self[pc].inicio = limite
        if abono:
            self[pc].abono = abono
        return True

    def cambiar(self, pco, pcd):
        if pco in self.lista_pc() and pcd not in self.lista_pc():
            self[pco].nombre = pcd

    def __refresh(self):
        sql = "select * from Alquiler where fin{}0;"
        if self.__ver_activos:
            sql = sql.format("=")
        else:
            sql = sql.format(">")
        self.__lista = []
        cur = db.cursor()
        for row in cur.execute(sql):
            a = Alquiler()
            a.set_row(row)
            self.__lista.append(a)
        cur.close()