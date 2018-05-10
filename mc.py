#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Eufracio Tenoch Sedano Rosales
tenochsr@gmail.com
"""
from definiciones import Sistema
import ui

def main():
    s = Sistema()
    try:
        tiempos_tkui = ui.TKUI(800, 500)
    except SystemExit as e:
        if e.code == 0:
            s.kill_daemon()
            print ("salio con 0")
        else:
            print ("salio con 1")
    #if tiempos_tkui.exit_mode == 0:
    return 0

if __name__ == '__main__':
    main()
