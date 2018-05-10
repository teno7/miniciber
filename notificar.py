#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Eufracio Tenoch Sedano Rosales
tenochsr@gmail.com
"""
from os.path import *
from definiciones import Sistema
from coleccion import ListaAlquiler
import notify2, time, os, signal 


s = Sistema()
config_dir = s.config_dir

def get_old_pid():
    pid_path = config_dir + "mcp.pid"
    if isfile(pid_path):
        fpid = open(pid_path)
        pid = int(fpid.read())
        fpid.close()
        return pid
    return None

def save():
    pid_path = config_dir + "mcp.pid"
    fpid = open(pid_path, "w")
    fpid.write(str(os.getpid()))
    fpid.close()

#def kill(self):
#    pid_path = self.config_dir + "mcp.pid"
#    if isfile(pid_path):
#        os.remove(pid_path)

def verificar_tiempos():
    notify2.init("miniciber")
    alquileres = ListaAlquiler()
    while True:
        t = False
        for a in alquileres.lista():
            if a.limite == "TERMINADO":
                t = True
        if t:
            msg = "El tiempo se ha terminado para uno o mas clientes!!!"
            n = notify2.Notification("¡Tiempo agotado!", msg)
            n.show()
        time.sleep(30)


def main():
    old_pid = get_old_pid()
    if old_pid:
        try:
            os.kill(old_pid, signal.SIGTERM)
        except Exception:
            pass
    save()
    verificar_tiempos()
    return 0

if __name__ == '__main__':
    main()
