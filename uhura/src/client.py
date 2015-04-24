# -*- coding: utf-8 -*-
from socket import error
from server.setting import *
from socket import socket
from client.tools import Recive, Envia

HOST = '201.235.199.203'
#HOST = 'localhost'
PORT = 6031

msg_id = 0
connected = []
history = []


def main():
    #Crea objeto socket
    s = socket()
    s.connect((HOST, PORT))
    print "\n"*80
    r = Recive(s, connected, history, msg_id)
    e = Envia(s, connected, history, msg_id)
    r.start()
    e.start()


if __name__ == "__main__":
    main()
