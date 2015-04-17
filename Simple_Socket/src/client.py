# -*- coding: utf-8 -*-
from socket import error
from server.setting import *
from socket import socket
from client.tools import Recive

HOST = 'localhost'
PORT = 6032

connected = []

def main():
    #Crea objeto socket
    s = socket()
    #Abre la conexion con el server
    s.connect((HOST, PORT))
    #Recibe informacion del server
    c = Recive(s, connected)
    c.start()
    c.join()
    """
    input_data = s.recv(1024)
    #Imprime la informacion recibida
    print input_data
    while True:
        #Solicita ingreso de caracter
        output_data = raw_input('> ')
        if output_data:
            try:
                #Envia la informacion
                s.send(output_data)
            except TypeError:
                #En caso de dar error por caracteres se hace una convercion
                s.send(bytes(output_data, 'utf-8'))
            #Recive mensaje del servidor
            input_data = s.recv(1024)
            #Imprime lo recibido
            print input_data
            #Si lo que enviamos es quit entonces cierra el programa
            if output_data == '\quit':
                return
    """


if __name__ == "__main__":
    main()
