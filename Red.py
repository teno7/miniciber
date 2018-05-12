#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Eufracio Tenoch Sedano Rosales
tenochsr@gmail.com
"""

from PyQt5.QtCore import QObject, QByteArray, QSettings, pyqtSignal as Signal, QCryptographicHash
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
import struct
from sockectserver import BaseRequestHandler

class Oreja(BaseRequestHandler):
    
    def handler(self):
        data = self.request[0].strip().split(":")
        conn = self.request[1]
        

class Conexion:
    
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(socket.gethostname(), 35555)
        self.socket.listen(10)
    
    def atender():
        while True:
            conn, addr = self.accpet()
            datos = conn.recv(1024)
            datos = datos.split(":")
            conn.send(self.alquileres.send_state())
            
    
    refresh = Signal()
    
    def __init__(self, parent):
        QObject.__init__(self, parent)
        self.Oreja = QUdpSocket(self)
        self.Boca = QUdpSocket(self)
        self.Oreja.readyRead.connect(self.readCommand)
        self.Oreja.bind(35555, QUdpSocket.ShareAddress)
        
    def sendIP(self):
        settings = QSettings()
        ip = settings.value("mysql/ip")
        self.sendMessage("clients", "config", ip)
        
    def sendRefresh(self):
        self.sendMessage("all", "refresh")
    
    def sendRefreshClient(self):
        self.sendMessage("clients", "refresh")
    
    def sendRefreshServer(self):
        self.sendMessage("server", "refresh")
        
    def sendTimeout(self, host, res):
        self.sendMessage(host, "timeout", str(res))
    
    def sendTurnoff(self, mac):
        hashmac = QCryptographicHash(QCryptographicHash.Md5)
        hashmac.addData(mac)
        macmd5 = str(hashmac.result().toHex())
        macmd5 = macmd5.split("'")[1]
        self.sendMessage(macmd5, "turnoff")
    
    def sendWake(self, mac):
# Thank you to remco https://github.com/remcohaszing/pywakeonlan
        data = b'FFFFFFFFFFFF' + (mac.replace(":","") * 20).encode()
        send_data = b''
        for i in range(0, len(data), 2):
            send_data += struct.pack(b'B', int(data[i: i + 2], 16))
        self.Boca.writeDatagram(send_data, QHostAddress.Broadcast, 9)
    
    def sendMessage(self, destiny, command, args=""):
        msg = "zise:" + destiny + ":" + command
        if len(args) > 0:
            msg += ":" +  args
        self.Boca.writeDatagram(msg, QHostAddress.Broadcast, 35555)
        
    def readCommand(self):
        msgTot = ""
        while self.Oreja.hasPendingDatagrams():
            msg, rem, port = self.Oreja.readDatagram(self.Oreja.pendingDatagramSize())
            msgTot += msg.decode("utf-8")
        print (msgTot)
        dMen = msgTot.split(":")
        if dMen[0] == "zise":
            if dMen[1] == "all" or dMen[1] == "server":
                if dMen[2] == "refresh":
                    self.refresh.emit()
                if dMen[2] == "requestip":
                    self.sendIP()
