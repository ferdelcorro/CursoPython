# -*- coding: utf-8 -*-
from socket import error
from threading import Thread
from server.setting import *


class Client(Thread):
    """
    Servidor eco - reenvía todo lo recibido.
    """

    def __init__(self, conn, addr, client):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.conn = conn
        self.addr = addr
        self.client = client

    def run(self):
        self.conn.send(MSG_WELCOME_CLIENTE)
        while True:
            try:
                input_data = self.conn.recv(1024)
                print 'entro --->'+str(input_data)
            except error:
                print "[%s] Error de lectura." % self.name
                break
            else:
                if input_data:
                    if input_data == EXIT_OPTION:
                        self.conn.close()
                        print self.addr[0] + " se a desconectado."
                        self.client.remove(self)
                        print "--%s cliente conectados" % str(len(self.client))
                        break
                    else:
                        self.conn.send("Server: " + input_data)
        self.conn.close()

    def close(self):
        """Método para cerrar el socket."""
        self.conn.close()


"""
class Client(Thread):

    def __init__(self, conn, addr, client):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.conn = conn
        self.addr = addr
        self.client = client

    def run(self):
        self.conn.send(MSG_WELCOME_CLIENTE)
        e = Escribe(self.conn, self.addr, self.client, self)
        e.start()
        while self in self.client:
            try:
                input_data = self.conn.recv(1024)
                if input_data:
                    print input_data
            except error:
                self.client.remove(self)
            #else:
            #    if input_data:
            #        if input_data == EXIT_OPTION:
            #            self.conn.close()
            #            print self.addr[0] + " se a desconectado."
            #            self.client.remove(self)
            #            print "--%s cliente conectados" % str(len(self.client))
            #            break
            #        else:
            #            self.conn.send("Server: " + input_data)
        self.conn.close()

    def close(self):
        self.conn.close()


class Escribe(Thread):

    def __init__(self, conn, addr, client, parent):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.conn = conn
        self.addr = addr
        self.client = client
        self.parent = parent

    def run(self):
        while self.parent in self.client:
            output_data = raw_input('> ')
            if output_data:
                try:
                    #Envia la informacion
                    self.conn.send(output_data)
                except TypeError:
                    #En caso de dar error por caracteres se hace una convercion
                    self.conn.send(bytes(output_data, 'utf-8'))

                if output_data == EXIT_OPTION:
                    self.conn.close()
                    self.client.remove(self.parent)
                    print 'bye'

    def close(self):
        self.conn.close()
"""