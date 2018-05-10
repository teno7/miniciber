#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Eufracio Tenoch Sedano Rosales
tenochsr@gmail.com
"""
from os.path import *
from multiprocessing import Process
import sys, os, signal, sqlite3

class Sistema:

    def __init__(self):
        if sys.platform in ["linux", "darwin"]:
            mcdir = "/.config/miniciber/"
        else:
            mcdir = "\miniciber-conf"
        self.config_dir = expanduser("~") + mcdir
        if not isdir(self.config_dir):
            os.mkdir(self.config_dir)
        self.__daemon_pid = None
        self.__db = None

    def __get_daemon_pid(self):
        pid_path = self.config_dir + "mcp.pid"
        if isfile(pid_path):
            fpid = open(pid_path)
            pid = int(fpid.read())
            fpid.close()
            return pid
        return None

    def kill_daemon(self):
        try:
            pid = self.__get_daemon_pid()
            if pid:
                os.kill(pid, signal.SIGTERM)
        except Exception:
            pass
        pid_path = self.config_dir + "mcp.pid"
        if isfile(pid_path):
            os.remove(pid_path)

    @property
    def db(self):
        db_path = self.config_dir + "tiempos.dat"
        sql = "SELECT name FROM sqlite_master WHERE type='table';"
        self.__db = sqlite3.connect(db_path)
        cur = self.__db.cursor()
        tablas = cur.execute(sql)
        if len(tablas.fetchall()) == 0:
            f = open("solo_tiempos.sql")
            sql = f.read()
            cur.executescript(sql)
            f.close()
            self.__db.commit()
        cur.close()
        return self.__db
