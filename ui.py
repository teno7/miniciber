#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Eufracio Tenoch Sedano Rosales
tenochsr@gmail.com
"""
from coleccion.comandos import Interprete
from coleccion.maquinas import ListaComputadoras
from coleccion.rentas import ListaAlquiler, Tarifa
from tkinter import *
from tkinter.ttk import *

class BaseView(Treeview):
    
    def __init__(self, parent):
        Treeview.__init__(self, parent)
        self.__item_ids = []

    def refresh(self):
        pass
    
    def clear(self):
        for i in self.__item_ids:
            self.delete(i)
        self.__item_ids = []
        
    def inserRow(self, row):
        self.__item_ids.append(self.insert("", -1, values=row))
        
class ComputadorasView(BaseView):
    
    def __init__(self, parent):
        BaseView.__init__(self, parent)
        self.computadoras = ListaComputadoras()
        self["columns"]= ('nombre', 'mac', 'ip')
        self.column("#0", width=10)
        self.column("nombre", width=50)
        self.heading("nombre", text="PC")
        self.column("mac", width=100)
        self.heading("mac", text="MAC")
        self.column("ip", width=100)
        self.heading("ip", text="IP")
    
    def refresh(self):
        self.clear()
        for c in self.computadoras:
            self.inserRow((c.nombre, c.mac, c.ip))
        
class TarifasView(BaseView):
    
    def __init__(self, parent):
        BaseView.__init__(self, parent)
        self.tarifa = Tarifa()
        self["columns"]= ('tiempo', 'cobro')
        self.column("#0", width=10)
        self.column("tiempo", width=50)
        self.heading("tiempo", text="Tiempo")
        self.column("cobro", width=100)
        self.heading("cobro", text="Cobro")
    
    def refresh(self):
        self.clear()
        for cob in self.tarifa:
            self.inserRow((cob.minutos, cob.importe))
        
class AlquilerView(BaseView):
    
    def __init__(self, parent):
        BaseView.__init__(self, parent)
        
    def refresh(self):
        pass
    
class CiberView(BaseView):
    
    def __init__(self, parent):
        BaseView.__init__(self, parent)
        self.computadoras = ListaComputadoras()
        self["columns"]= ('nombre', 'inicio', 'limite', 'abono', 'tiempo')
        self.column("#0", width=10)
        self.column("nombre", width=50)
        self.heading("nombre", text="PC")
        self.column("inicio", width=100)
        self.heading("inicio", text="Llegada")
        self.column("limite", width=100)
        self.heading("limite", text="Limite")
        self.column("abono", width=100)
        self.heading("abono", text="Abono")
        self.column("tiempo", width=100)
        self.heading("tiempo", text="Tiempo")

    def refresh(self):
        self.clear()
        for c in self.computadoras:
            if c.alquiler:
                col = (c.nombre, c.alquiler.inicio, c.alquiler.limite,
                       c.alquiler.abono, c.alquiler.tiempo)
            else:
                col = (c.nombre, "LIBRE", "LIBRE", 0.0, "LIBRE")
            self.inserRow(col)
            
class TKUI(Frame):

    def __init__(self, w, h):
        root = Tk()
        root.title("MiniCiber")
        Frame.__init__(self, root, width=w, height=h)
        self.pack(fill=BOTH, expand=1)
        self.espacio_tabla = Frame(self)
        self.espacio_tabla.pack(side="top", fill=BOTH, expand=1)
        self.tabla = CiberView(self.espacio_tabla)
        self.tabla.pack(side="top", fill=BOTH, expand=1)
        self.linea_comandos = Frame(self)
        self.linea_comandos.pack(side="top", fill=X, expand=1)
        self.linea_instrucciones = Frame(self)
        self.linea_instrucciones.pack(side="bottom", fill=X, expand=1)
        self.f2 = Label(self.linea_instrucciones, text="<F2> Ciber")
        self.f7 = Label(self.linea_instrucciones, text="<F7> Computadoras")
        self.f8 = Label(self.linea_instrucciones, text="<F8> Tarifas")
        self.f9 = Label(self.linea_instrucciones, text="<F9> Alquileres")
        self.f2.pack(side="left")
        self.f7.pack(side="left")
        self.f8.pack(side="left")
        self.f9.pack(side="left")
        self.bind_all("<Escape>", self.ocultar_comandos)
        self.bind_all("<F2>", self.mostrar_ciber)
        self.bind_all("<F7>", self.mostrar_comp)
        self.bind_all("<F8>", self.mostrar_alq)
        self.bind_all("<F9>", self.mostrar_tar)
        self.bind_all(":", self.mostrar_comandos)
        self.tabla.refresh()
        self.after(1000, self.tabla.refresh)
        root.mainloop()
    
    def mostrar_ciber(self, i):
        for child in self.espacio_tabla.winfo_children():
            child.destroy()
        self.tabla = CiberView(self.espacio_tabla)
        self.tabla.pack(side="top", fill=BOTH, expand=1)
        
    def mostrar_comp(self, i):
        for child in self.espacio_tabla.winfo_children():
            child.destroy()
        self.tabla = ComputadorasView(self.espacio_tabla)
        self.tabla.pack(side="top", fill=BOTH, expand=1)
        
    def mostrar_alq(self, i):
        for child in self.espacio_tabla.winfo_children():
            child.destroy()
        self.tabla = AlquilerView(self.espacio_tabla)
        self.tabla.pack(side="top", fill=BOTH, expand=1)
    
    def mostrar_tar(self, i):
        for child in self.espacio_tabla.winfo_children():
            child.destroy()
        self.tabla = TarifasView(self.espacio_tabla)
        self.tabla.pack(side="top", fill=BOTH, expand=1)

    def mostrar_comandos(self, i):
        if len(self.linea_comandos.winfo_children())>0:
            self.comando.focus_set()
            return
        self.dospuntos = Label(self.linea_comandos, text=":")
        self.comando = Entry(self.linea_comandos)
        self.dospuntos.pack(side="left")
        self.comando.pack(side="left", fill=X, expand=1)
        self.comando.focus_set()
        self.comando.bind("<Return>", self.leer_comando)

    def ocultar_comandos(self, i):
        for child in self.linea_comandos.winfo_children():
            child.destroy()

    def leer_comando(self, c):
        cmd = self.comando.get()
        self.comando.delete(0, END)
        inter = Interprete()
        if inter.ejecutar(cmd):
            self.refresh()
        else:
            self.mostrar_msg(inter.error)

    def mostrar_msg(self, msg):
        label = Label(self, text=msg)
        label.pack(side="bottom", fill=X, expand=1)
        self.after(5000, label.destroy)