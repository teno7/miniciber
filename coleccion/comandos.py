#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Eufracio Tenoch Sedano Rosales
tenochsr@gmail.com
"""
from definiciones import Sistema
from coleccion.maquinas import ListaComputadoras
from coleccion.renta import Tarifa
from time import time, strftime, localtime
import math, re, sys


class Interprete:

    def __init__(self, cmd):
        self.cmd = cmd
        self.computadoras = ListaComputadoras()
        self.tarifa = Tarifa()
        self.__instrucciones = []
        self.__objetivos = []
        self.error = ""

    def ejecutar(self):
        if self.cmd == "q" or self.cmd == "q!":
            self.__instrucciones.append(self.cmd)
            return True
        re_pc = "pcc$|pcd\s*(\w*)$|pc\s+(\w+),\s*([a-fA-F0-9]{2,2}[:\-]{3,3}[a-fA-F0-9]),\s*(\d{1,3}\.{3,3}\d{1,3})$"
        re_tarifa = "(trc)$|trd\s*(\d+)$|tr\s*(\d+),\s*(\d+(?:\.\d+)?)$"
        re_control = "s(\d+(?:,\d+))(\S+)"
        pcm = re.match(re_pc, self.cmd)
        ccm = re.match(re_control, self.cmd)
        trm = re.match(re_tarifa, self.cmd)
        if pcm:
            return validar_pc(pcm)
        elif trm:
            return ejecutar_tarifa(trm)
        elif ccm:
            selector = ccm.group(0)
            objetivos = selector.split(",")
            lista_cmd = self.validar_cc(ccm.group(1))
            if lista_cmd:
                return self.ejecutar_cc(lista_cmd)
            self.error = "Argumentos son requeridos para control"
            return False
        ### SENTENCIA PARA DECLARAR NO VALIDAD UNA INSTRUCCION ###
        self.error = "Error de sintaxis: '{}' No reconocido".format(self.cmd)
        return False

    def ejecutar_pc(self, pcm):
        grps = pcm.groups()
        if grps[0]:
            if not self.computadoras[grps[0]].eliminar():
                self.error = "No se pudo eliminar {}".format(grps[0])
                return False
        elif grps[1]:
            self.computadoras.nuevo(grps[1], grps[2], grps[3])
        else:
            self.computadoras.clear()
        return True

    def ejecutar_tarifa(self, trm):
        grps = trm.groups()
        if grps[0]:
            self.tarifa.limpiar()
        elif grps[1]:
            self.eliminar(int(grps[1]))
        elif grps[2]:
            self.tarifa.insertar(int(grps[2]), int(grps[3]))
        return True

    def validar_cc(self, arg):
        iniciar = "(i)(\d*)" #Hay acciones que son incompatibles
        abono = "(a)(\+?\d+(?:.\d+)?)" #Entre ellas mismas
        limmuer = "([lm])(\+?\d+)" #No puedes iniciar y terminar
        cambiar = "(c)(\d+)" #En la misma sentencia
        terminar = "(t)()"
        eliminar = "(d)()"
        reglas = []
        reglas.append((0, iniciar, 1))
        reglas.append((1, "$", 4))
        reglas.append((2, "$", 4))
        reglas.append((1, abono, 4))
        reglas.append((0, cambiar, 4))
        reglas.append((0, terminar, 4))
        reglas.append((0, eliminar, 4))
        reglas.append((0, abono, 2))
        reglas.append((0, limmuer, 2))
        reglas.append((2, limmuer, 4))
        reglas.append((3, abono, 4))
        est = 0
        lista_cmd = []
        while est < 4 and len(arg) > 0:
            for r in reglas:
                if est == r[0]:
                    match = re.match(r[1], arg)
                    if match:
                        est = r[2]
                        lista_cmd.append(match.group(1), match.group(2))
                        arg = arg.replace(match.group(0), "")
                        break
                    else:
                        est = 5
        if est == 4:
            return lista_cmd
        return None

    def ejecutar_cc(self, lista_cmd):# lista es tupla CAMBIAR FUNCION
        for ins, arg in lista_cmd:
            if "i" in ins:
                arg = ins.replace("i", "")
                if len(arg) > 0:
                    arg = int(arg)
                else:
                    arg = 0
                for pc in self.__objetivos:
                    if not self.computadoras[pc].iniciar(arg):
                        self.error = "Computadora con alquiler asignado: {}"
                        self.error = self.error.format(pc)
                        return False
            elif "b" in ins:
                arg = ins.replace("b", "")
                if "+" in arg:
                    arg = int(arg.replace("+", ""))
                    for pc in self.__objetivos:
                        self.computadoras[pc].alquiler.abono += arg
                else:
                    arg = int(arg)
                    for pc in self.__objetivos:
                        self.computadoras[pc].alquiler.abono = arg
            elif "c" in ins:#######################
                arg = int(ins.replace("c", ""))
                for pc in self.__objetivos:
                    self.alquileres.cambiar(pc, arg)
            elif "l" in ins:
                arg = ins.replace("l", "")
                if "+" in arg:
                    arg = int(arg.replace("+", ""))
                    for pc in self.__objetivos:
                        self.computadoras[pc].alquiler.sumar_limite(arg)
                else:
                    arg = int(arg)
                    for pc in self.__objetivos:
                        self.computadoras[pc].alquiler.limite = arg
            elif "m" in ins:
                arg = ins.replace("m", "")
                if "+" in arg:
                    arg = int(arg.replace("+", ""))
                    for pc in self.__objetivos:
                        self.computadoras[pc].alquiler.muerto += arg
                else:
                    arg = int(arg)
                    for pc in self.__objetivos:
                        self.computadoras[pc].alquiler.muerto = arg
            elif "t" in ins:
                for pc in self.__objetivos:
                    self.computadoras[pc].detener()
            elif "d" in ins:
                for pc in self.__objetivos:
                    self.computadoras[pc].eliminar()
            elif "q!" in ins:
                sys.exit(0)
            elif "q" in ins:
                sys.exit(1)
        return True
