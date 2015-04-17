# -*- coding: utf-8 -*-
from socket import error
from threading import Thread


class Recive(Thread):

    def __init__(self, socket, connected):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.socket = socket
        self.connected = connected

    def run(self):
        e = Envia(self.socket, self.connected)
        e.start()
        while len(self.connected) == 0:
            input_data = self.socket.recv(1024)
            if input_data:
                print input_data


class Envia(Thread):

    def __init__(self, socket, connected):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.socket = socket
        self.connected = connected

    def run(self):
        while len(self.connected) == 0:
            output_data = raw_input("> ")

            if output_data:
                try:
                    #Envia la informacion
                    self.socket.send(output_data)
                except TypeError:
                    #En caso de dar error por caracteres se hace una convercion
                    self.socket.send(bytes(output_data, "utf-8"))
                if output_data == '\quit':
                    self.connected.append('bye')
                    print 'bye'
