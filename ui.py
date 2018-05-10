#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Eufracio Tenoch Sedano Rosales
tenochsr@gmail.com
"""
from coleccion import ListaAlquiler, Interprete
from tkinter import *
from tkinter.ttk import *

class TKUI(Frame):

    def __init__(self, w, h):
        root = Tk()
        root.title("MiniCiber")
        Frame.__init__(self, root, width=w, height=h)
        self.pack(fill=BOTH, expand=1)
        self.alquileres = ListaAlquiler()
        self.tabla = Treeview(self)
        self.tabla["columns"]= ('nombre', 'inicio', 'limite', 'abono', 'tiempo')
        self.tabla.column("#0", width=10)
        self.tabla.column("nombre", width=50)
        self.tabla.heading("nombre", text="PC")
        self.tabla.column("inicio", width=100)
        self.tabla.heading("inicio", text="Llegada")
        self.tabla.column("limite", width=100)
        self.tabla.heading("limite", text="Limite")
        self.tabla.column("abono", width=100)
        self.tabla.heading("abono", text="Abono")
        self.tabla.column("tiempo", width=100)
        self.tabla.heading("tiempo", text="Tiempo")
        self.tabla.pack(side="top", fill=BOTH, expand=1)
        self.bind_all("<Escape>", self.ocultar_comandos)
        self.bind_all(":", self.mostrar_comandos)
        self.linea_comandos = None
        self.__item_ids = []
        self.refresh()
        root.mainloop()

    def refresh(self):
        for i in self.__item_ids:
            self.tabla.delete(i)
        self.__item_ids = []
        for a in self.alquileres.lista():
            self.__item_ids.append(self.tabla.insert(
                "", -1, values=(a.nombre, a.inicio,
                                a.limite, a.abono, a.tiempo)
                ))
        self.after(1000, self.refresh)

    def mostrar_comandos(self, i):
        if self.linea_comandos:
            self.comando.focus_set()
            return
        self.linea_comandos = Frame(self)
        self.dospuntos = Label(self.linea_comandos, text=":")
        self.comando = Entry(self.linea_comandos)
        self.dospuntos.pack(side="left")
        self.comando.pack(side="left", fill=X, expand=1)
        self.linea_comandos.pack(side="bottom", fill=X, expand=1)
        self.comando.focus_set()
        self.comando.bind("<Return>", self.leer_comando)

    def ocultar_comandos(self, i):
        if self.linea_comandos:
            self.linea_comandos.destroy()
            self.linea_comandos = None

    def leer_comando(self, c):
        cmd = self.comando.get()
        print (cmd)
        self.comando.delete(0, END)
        inter = Interprete(cmd)
        if inter.validar():
            if not inter.ejecutar():
                self.mostrar_msg(inter.error)
            self.refresh()
        else:
            self.mostrar_msg(inter.error)

    def mostrar_msg(self, msg):
        label = Label(self, text=msg)
        label.pack(side="bottom", fill=X, expand=1)
        self.after(5000, label.destroy)