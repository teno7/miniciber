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
        re_pc = "pc\s(\w+),\s(\w*),\s(\w*)"
        re_tarifa = "(trc)$|trd\s*(\d+)$|tr\s*(\d+),\s*(\d+(?:\.\d+)?)$"
        re_selector = "s\d+(,\d+)*"
        pcm = re.match(re_pc, self.cmd)
        m = re.match(re_selector, self.cmd)
        trm = re.match(re_tarifa, self.cmd)
        if pcm:
            return validar_pc(pcm)
        elif trm:
            return ejecutar_tarifa(trm)
        elif m:
            return self.validar_accion(m)
        ### SENTENCIA PARA DECLARAR NO VALIDAD UNA INSTRUCCION ###
        self.error = "Error de sintaxis: '{}' No reconocido".format(self.cmd)
        return False
    
    def ejecutar_pc(self, pcm):
		grps = pcm.groups()
		if grps[0]:
		    if not self.computadoras[grps[0]].eliminar(): ## Funcion no implementada
			    self.error = "No se pudo eliminar {}".format(grps[0])
		        return False
			return True
		elif grps[1]:
		    self.computadoras.nuevo(grps[1], grps[2], grps[3])
	    else:
		    self.computadoras.clear() ## Funcion no implementada
    
    def ejecutar_tarifa(self, trm):
        grps = trm.groups()
        if grps[0]:
            self.tarifa.limpiar()
        elif grps[1]:
            self.eliminar(int(grps[1]))
        elif grps[2]:
            self.tarifa.insertar(int(grps[2]), int(grps[3]))
        return True
        
    def validar_accion(self, m):
        regla = {}
        regla["inicio"] = "i\d*"
        regla["abono"] = "b\+{,1}\d+(.\d+){,1}"
        regla["limite"] = "l\+{,1}\d+"
        regla["muerto"] = "m\+{,1}\d+"
        regla["cambiar"] = "c\d+"
        regla["terminar"] = "t"
        regla["eliminar"] = "d"
        selector = m.group(0)
        selector = selector.replace("s", "")
        self.__objetivos = selector.split(",")
        ccmd = self.cmd.replace(m.group(0), "")
        for r in regla:
            match = re.search(regla[r], ccmd)
            if match:
                self.__instrucciones.append(match.group(0))
                ccmd = ccmd.replace(match.group(0), "")
        return True if ccmd == "" else False

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
