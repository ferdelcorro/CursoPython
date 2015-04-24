# -*- coding: utf-8 -*-
from socket import error
from threading import Thread


class Recive(Thread):

    def __init__(self, socket, connected):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.my_socket = socket
        self.connected = connected

    def run(self):
        while len(self.connected) == 0:
            input_data = self.my_socket.recv(1024)
            if input_data:
                print input_data


class Envia(Thread):

    def __init__(self, socket, connected):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.my_socket = socket
        self.connected = connected

    def run(self):
        while len(self.connected) == 0:
            output_data = raw_input("> ")

            if output_data:
                try:
                    #Envia la informacion
                    self.my_socket.send(output_data)
                except TypeError:
                    #En caso de dar error por caracteres se hace una convercion
                    self.my_socket.send(bytes(output_data, "utf-8"))
                if output_data == '\quit':
                    self.connected.append('bye')
                    print 'bye'
