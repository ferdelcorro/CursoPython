# -*- coding: utf-8 -*-
from socket import error
from server.setting import *
from socket import socket
from client.tools import Recive, Envia

HOST = 'tuxis-us-03.tuxis.com.ar'
PORT = 6030

connected = []


def main():

    try:
        #Crea objeto socket
        s = socket()
        #Abre la conexion con el server
        s.connect((HOST, PORT))
        #Recibe informacion del server
        r = Recive(s, connected)
        e = Envia(s, connected)
        r.start()
        e.start()

    except KeyboardInterrupt:
        r.my_socket.close()
        e.my_socket.close()

        r.__stop = True
        e.__stop = True


if __name__ == "__main__":
    main()
