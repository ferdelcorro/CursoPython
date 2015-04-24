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
        