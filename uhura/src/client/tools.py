# -*- coding: utf-8 -*-
from socket import error
from threading import Thread
from client.core import getTerminalSize, print_there
import json


MSG_SENDED = {}


class Recive(Thread):

    def __init__(self, socket, connected, history, msg_id):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.socket = socket
        self.connected = connected
        self.history = history
        self.msg_id = msg_id
        for x in range(getTerminalSize()[1]-1):
            self.history.append(' ')
        print self.history

    def run(self):
        while len(self.connected) == 0:
            try:
                input_data = self.socket.recv(1024)
            except:
                break
            else:
                if input_data:
                    input_data = json.loads(input_data)

                    if input_data['type'] == 'MSG-P' or \
                            input_data['type'] == 'MSG':
                        input_data = msg(input_data)
                    elif input_data['type'] == 'R-CMD':
                        input_data = cmd_response(input_data)

                    if '\n' in input_data:
                        for x in input_data.split('\n'):
                            self.history.append(x)
                    else:
                        self.history.append(input_data)
                    pos_temp = len(self.history) - getTerminalSize()[1]
                    history_tmp = self.history[pos_temp:]
                    for x in range(getTerminalSize()[1]):
                        for y in range(getTerminalSize()[0]):
                            print_there(x, y, ' ')
                    acumulador = 0
                    for x in history_tmp:
                        print_there(acumulador, 0, x)
                        acumulador += 1

    #privado
    #s = {
    #    'type': 'MSG-P',
    #    'from': 'Juan_Perez',
    #    'time': '03:00',
    #    'msg': 'Hola como andan',
    #}
    #publico
    #s = {
    #    'type': 'MSG',
    #    'from': 'Juan_Perez',
    #    'time': '03:00',
    #    'msg': 'Hola como andan',
    #}
    def msg(self, msg):
        msg_result = str(msg['time']) + ' - '
        msg_result += '<' + str(msg['from']) + '> '
        msg_result += str(msg['msg'])
        return msg_result

    #s = {
    #    'type': 'R-CMD',
    #    'id': '23d23d',
    #    'status': 'OK',
    #    'response': ''
    #}
    def cmd_response(self, msg):
        if MSG_SENDED[msg['id']] == 'user_list':
            msg = reciv_user_list(msg)
        elif MSG_SENDED[msg['id']] == 'help':
            msg = reciv_help(msg)
        else:
            msg = reciv_nick(msg)
        return msg

    #comando: user_list
    #s = {
    #    'type': 'R-CMD',
    #    'id': '23d23d',
    #    'status': 'OK',
    #    'Description': 'Usuarios conectados',
    #    'response': ['Juan_Perez', 'Tuxis']
    #}
    def reciv_user_list(self, msg):
        if msg['status'] == 'OK':
            msg_result = str(msg['Description']) + ' '
            for x in msg['response']:
                msg_result += str(x) + ' '
        else:
            msg_result = 'Ha ocurrido un error'
        return msg_result

    #comando: help
    #s = {
    #    'type': 'R-CMD',
    #    'id': '23d23d',
    #    'status': 'OK',
    #    'response-str': 'Ayuda del Server',
    #    'response-vec': ['---------\nHelp del Server UHURA\n\help:\n\t
    #Permite consultar la ayuda.']
    #}
    def reciv_help(self, msg):
        if msg['status'] == 'OK':
            msg_result = str(msg['response-str']) + ' '
            for x in msg['response-vec']:
                msg_result += str(x) + ' '
        else:
            msg_result = 'Ha ocurrido un error'
        return msg_result

    #comando: nick
    #    s = {
    #    'type': 'R-CMD',
    #    'id': '23d23d',
    #    'status': 'OK',
    #    'response': ''
    #}
    def reciv_nick(self, msg):
        if msg['status'] == 'OK':
            msg_result = 'Su nick ha sido cambiado a ' + str(
                MSG_SENDED[msg['id']]['parameter'][0]
            )
        else:
            msg_result = 'Ha ocurrido un error'
        return msg_result


class Envia(Thread):

    def __init__(self, socket, connected, history, msg_id):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.socket = socket
        self.connected = connected
        self.history = history
        self.promt = '> '
        self.msg_id = msg_id

    def run(self):
        print "\n"*80
        while len(self.connected) == 0:
            output_data = raw_input(self.promt)
            if output_data:

                if '\say' in output_data:
                    private_msg(output_data)
                elif '\\nick' in output_data:
                    cmd_msg(output_data)
                elif '\user_list' in output_data:
                    list_msg(output_data)
                elif '\help' in output_data:
                    help_msg(output_data)
                else:
                    send_msg(output_data)

                if output_data[:6] == '\\nick ':
                    self.promt = '[' + output_data[6:] + ']: '
                if output_data == '\quit':
                    print 'Te has desconectado'
                    self.socket.close()
                    break

    def send_msg(self, msg):
        try:
            #Envia la informacion
            self.socket.send(msg)
        except TypeError:
            #En caso de dar error por caracteres se hace una convercion
            self.socket.send(bytes(msg, "utf-8"))

    #privado
    #s = {
    #    'type': 'MSG-P',
    #    'id': '23d23d',
    #    'msg': 'Hola como andas',
    #    'to': 'Juan_Perez'
    #}
    def private_msg(self, msg):
        while '\say' in msg:
            msg = msg.split('\say')[1]
        msg_id = self.msg_id
        self.msg_id += 1
        to = msg.split('>')[0]
        to = to.splot('<')[1]
        msg = msg.split('>')[1]
        s = {
            'type': 'MSG-P',
            'id': msg_id,
            'msg': msg,
            'to': to
        }
        json_resultante = json.dumos(s)
        MSG_SENDED[msg_id] = json_resultante
        send_msg(json_resultante)

    #publico
    #s = {
    #    'type': 'MSG',
    #    'id': '23d23d',
    #    'msg': 'Hola como andan',
    #}
    def public_msg(self, msg):
        msg_id = self.msg_id
        self.msg_id += 1
        s = {
            'type': 'MSG',
            'id': msg_id,
            'msg': msg,
        }
        json_resultante = json.dumos(s)
        MSG_SENDED[msg_id] = json_resultante
        send_msg(json_resultante)

    #comando: nick
    #s = {
    #    'type': 'CMD',
    #    'id': '23d23d',
    #    'cmd': 'nick',
    #    'parameter': ['Tuxis', ]
    #}
    def nick_msg(self, msg):
        while '\\nick' in msg:
            msg = msg.split('\\nick ')[1]
        msg_id = self.msg_id
        self.msg_id += 1
        s = {
            'type': 'CMD',
            'id': msg_id,
            'cmd': 'nick',
            'parameter': [msg,]
        }
        json_resultante = json.dumos(s)
        MSG_SENDED[msg_id] = json_resultante
        send_msg(json_resultante)

    #comando: user_list
    #s = {
    #    'type': 'CMD',
    #    'id': '23d23d',
    #    'cmd': 'user_list',
    #}
    def list_msg(self, msg):
        while '\user_list' in msg:
            msg = msg.split('\user_list')[1]
        msg_id = self.msg_id
        self.msg_id += 1
        s = {
            'type': 'CMD',
            'id': msg_id,
            'cmd': 'user_list'
        }
        json_resultante = json.dumos(s)
        MSG_SENDED[msg_id] = json_resultante
        send_msg(json_resultante)

    #comando: help
    #s = {
    #    'type': 'CMD',
    #    'id': '23d23d',
    #    'cmd': 'help',
    #}
    def help_msg(self, msg):
        msg_id = self.msg_id
        self.msg_id += 1
        s = {
            'type': 'CMD',
            'id': msg_id,
            'cmd': 'help',
        }
        json_resultante = json.dumos(s)
        MSG_SENDED[msg_id] = json_resultante
        send_msg(json_resultante)
