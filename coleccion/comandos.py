#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Eufracio Tenoch Sedano Rosales
tenochsr@gmail.com
"""
from definiciones import Sistema
from coleccion.maquinas import ListaComputadoras
from coleccion.rentas import Tarifa
from time import time, strftime, localtime
import math, re, sys


class Interprete:

    def __init__(self):
        self.computadoras = ListaComputadoras()
        self.tarifa = Tarifa()
        self.error = ""

    def ejecutar(self, cmd):
        if "q!" == cmd: # La instruccion de salida podria estar incluida
            sys.exit(0) # En alguna de las otras instrucciones 
        elif "q" == cmd:# Debe definirse en el codigo de abajo
            sys.exit(1)
        re_pc = "pcc$|pcd\s*(\w*)$|pc\s+(\w+),\s*((?:[a-fA-F0-9]{2,2}[:\-]){3,3}[a-fA-F0-9]),\s*((?:\d{1,3}\.){3,3}\d{1,3})$"
        re_tarifa = "(trc)$|trd\s*(\d+)$|tr\s*(\d+),\s*(\d+(?:\.\d+)?)$"
        re_control = "s(\d+(?:,\d+))(\S+)"
        pcm = re.match(re_pc, cmd)
        trm = re.match(re_tarifa, cmd)
        ccm = re.match(re_control, cmd)
        if pcm:
            return ejecutar_pc(pcm)
        elif trm:
            return ejecutar_tarifa(trm)
        elif ccm:
            selector = ccm.group(0)
            objetivos = selector.split(",")
            for o in objetivos:
                if o not in self.computadoras:
                    self.error = "Objetivo no encontrado"
                    return False
            lista_cmd = self.validar_cc(ccm.group(1))
            if lista_cmd:
                return self.ejecutar_cc(objetivos, lista_cmd)
            self.error = "Semantica no comprendida por el intérprete"
            return False
        ### SENTENCIA PARA DECLARAR NO VALIDAD UNA INSTRUCCION ###
        self.error = "Error de sintaxis: '{}' No reconocido".format(cmd)
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
        arg = arg.replace(" ", "")
        #### ---- EXPRESIONES REGULARES PARA ARGUMENTOS PRIMARIOS ---- ####
        prim = "i(\d*)|" #Hay acciones que son incompatibles
        prim += "c(\w+)|" #En la misma sentencia
        prim += "(t)"
        lista_prim = re.search(prim, arg)
        resto = re.sub(prim, "", arg, 1)
        #### ---- EXPRESIONES REGULARES PARA ARGUMENTOS SECUNDARIOS ---- ####
        reglas_sec = []
        reglas_sec.append("b(\+?\d+(?:.\d+)?)") #Entre ellas mismas
        reglas_sec.append("l(\+?\d+)") #No puedes iniciar y terminar
        reglas_sec.append("m(\+?\d+)") #No puedes iniciar y terminar
        lista_sec = []
        for r in reglas_sec:
            match = re.search(r, resto)
            resto = re.sub(r, "", resto, 1)
            if match:
                lista_sec.append(match.group(1))
        if len(resto) > 0:
            return None
        return (lista_prim.groups(), lista_sec)

    def ejecutar_cc(self, objetivos, lista_cmd):
        prim, sec = lista_cmd
        ##### ------ EJECUSION DE ARGUMENTOS SECUNDARIOS ------ ##### 
        if prim[0]: # --- Procesando iniciar (i)
            for pc in objetivos:
                if not self.computadoras[pc].iniciar(prim[0]):
                    self.error = "Computadora con alquiler asignado: {}"
                    self.error = self.error.format(pc)
                    return False
        elif prim[1]: # --- Procesando cambiar (c)
            self.computadoras.cambiar(objetivos[0], prim[1])
        elif prim[2]: # --- Procesando terminar (t)
            for pc in objetivos:
                self.computadoras[pc].detener()
        ##### ------ EJECUSION DE ARGUMENTOS SECUNDARIOS ------ ##### 
        if sec[0]: # Procesando abono (b)
            if "+" in sec[0]:
                arg = int(sec[0].replace("+", ""))
                for pc in objetivos:
                    self.computadoras[pc].alquiler.abono += arg 
            else:
                arg = int(sec[0])
                for pc in objetivos:
                    self.computadoras[pc].alquiler.abono = arg
        elif sec[1]: # Procesando limite (l)
            if "+" in sec[1]:
                arg = int(sec[1].replace("+", ""))
                for pc in objetivos:
                    self.computadoras[pc].alquiler.sumar_limite(arg)
            else:
                arg = int(sec[1])
                for pc in objetivos:
                    self.computadoras[pc].alquiler.limite = arg
        elif sec[2]: # Procesando tiempo muerto (m)
            if "+" in sec[2]:
                arg = int(sec[2].replace("+", ""))
                for pc in objetivos:
                    self.computadoras[pc].alquiler.muerto += arg
            else:
                arg = int(sec[2])
                for pc in objetivos:
                    self.computadoras[pc].alquiler.muerto = arg
        return True