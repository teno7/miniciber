#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Eufracio Tenoch Sedano Rosales
tenochsr@gmail.com
"""
from definiciones import Sistema
from coleccion.maquinas import ListaComputadoras
from time import time, strftime, localtime
import math, re, sys


class Interprete:

    def __init__(self, cmd):
        self.cmd = cmd
        self.computadoras = ListaComputadoras()
        self.__instrucciones = []
        self.__objetivos = []
        self.error = ""

    def validar(self):
        if self.cmd == "q" or self.cmd == "q!":
            self.__instrucciones.append(self.cmd)
            return True
        regla = {}
        re_pc = "pc\s(\w+),\s(\w*),\s(\w*)"
        re_selector = "s\d+(,\d+)*"
        regla["inicio"] = "i\d*"
        regla["abono"] = "b\+{,1}\d+(.\d+){,1}"
        regla["limite"] = "l\+{,1}\d+"
        regla["muerto"] = "m\+{,1}\d+"
        regla["cambiar"] = "c\d+"
        regla["terminar"] = "t"
        regla["eliminar"] = "d"
        pcm = re.match(re_pc, self.cmd)
        if pcm:
            nombre = pcm[0]
            MAC = pcm[1]
            ip = pcm[2] ##### Meter esto en las instrucciones #######
        m = re.match(re_selector, self.cmd)
        if m:
            selector = m.group(0)
            selector = selector.replace("s", "")
            self.__objetivos = selector.split(",")
            self.cmd = self.cmd.replace(m.group(0), "")
            for r in regla:
                match = re.search(regla[r], self.cmd)
                if match:
                    self.__instrucciones.append(match.group(0))
                    self.cmd = self.cmd.replace(match.group(0), "")
        else:
            self.error = "Selector no valido"
            return False
        if len(self.cmd) > 0:
            self.error = "Error de sintaxis: '{}' No reconocido".format(self.cmd)
            return False
        else:
            return True

    def ejecutar(self):
        for ins in self.__instrucciones:
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
