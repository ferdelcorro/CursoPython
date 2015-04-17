# -*- coding: utf-8 -*-
import ast


class Agenda(object):
    registros = []
    
    def __init__(self, arg):
        super(Agenda, self).__init__()
        print arg

    def Leer_archivo(self):
        f = open('agenda.txt', 'r')
        for l in f:
            x = l.replace('\n', '')
            if x != '':
                x = ast.literal_eval(x)
                self.registros.append(x)

    def Escribir_archivo(self):
        f = open('agenda.txt', 'w')
        for l in self.registros:
            f.write(str(l)+'\n')

    def Guardar(self, Name, Last_Name, **kwars):
        s = {
            'name': Name,
            'last_name': Last_Name,
        }
        if 'addres' in kwars:
            s['addres'] = kwars['addres']
        if 'email' in kwars:
            s['email'] = kwars['email']
        if 'phone' in kwars:
            s['phone'] = kwars['phone']
        self.registros.append(s)
        return True

    def Borrar(self, name, last_name):
        result = False
        for x in self.registros:
            if name == x['name'] and last_name == x['last_name']:
                self.registros.remove(x)
                result = True
        return result

    def Buscar(self, p_busqueda):
        resultado = []
        for x in self.registros:
            in_name = x['name'] in p_busqueda or p_busqueda in x['name']
            in_last_n = x['last_name'] in p_busqueda or p_busqueda in x['last_name']
            if in_name or in_last_n:
                resultado.append(x)
        return resultado

    def Listar(self):
        return self.registros
