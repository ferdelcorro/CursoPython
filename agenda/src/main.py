# -*- coding: utf-8 -*-
from agenda import Agenda

def main(): 
    obj = Agenda('Hola')
    obj.Leer_archivo()
    opcion = '0'
    contador_errores = 0
    while opcion != '5':
        print '\n'*80
        print '='*30
        print 'Hola manola'
        print '='*30
        print 'opciones'
        print '1) Ver agenda'
        print '2) Agregar registro'
        print '3) Borrar registro'
        print '4) Buscar registro'
        print '5) Salir'
        opcion = raw_input('Ingrese la opcion: ')
        if opcion == '1':
            contador_errores = 0
            result = obj.Listar()
            if len(result) == 0:
                print 'La agenda se encuentra vacìa'
                raw_input('Presione enter para continuar')
            else:
                print result
                raw_input('Presione enter para continuar')
                
            
        elif opcion == '2':
            contador_errores = 0
            nombre = raw_input('Ingrese el nombre: ')
            apellido = raw_input('Ingrese el apellido: ')
            address = raw_input('Ingrese el address: ')
            email = raw_input('Ingrese el email: ')
            phone = raw_input('Ingrese el phone: ')
            result = obj.Guardar(nombre, apellido,
                                 address=address, email=email, phone=phone
                    )
            if result:
                print 'La persona ha sido agregada'
                raw_input('Presione enter para continuar')
            else:
                print 'Ocurriò un error'
                raw_input('Presione enter para continuar')

        elif opcion == '3':
            contador_errores = 0
            nombre = raw_input('Ingrese el nombre: ')
            apellido = raw_input('Ingrese el apellido: ')
            result = obj.Borrar(nombre, apellido)
            if result:
                print 'La persona ha sido borrada'
                raw_input('Presione enter para continuar')
            else:
                print 'Ocurriò un error'
                raw_input('Presione enter para continuar')

        elif opcion == '4':
            contador_errores = 0
            parametro = raw_input('Ingrese un paràmetro de bpusqueda: ')
            result = obj.Buscar(parametro)
            if len(result) != 0:
                print '\n'*5
                print 'Se encontrò'
                print result
                print '\n'*5
                raw_input('Presione enter para continuar')
            else:
                print ('No se encontrò ninguna persona')
                raw_input('Presione enter para continuar')

        elif opcion == '5':
            contador_errores = 0
            confirmacion = raw_input('Està seguro? Y/N: ')
            if confirmacion == 'N' or confirmacion == 'n':
                opcion = 0
                print '\n'*5
                print ('Se cancelo la salida')
                raw_input('Presione enter para continuar')
            else:
                print 'Good bye'
                obj.Escribir_archivo()

        else:
            contador_errores += 1
            if contador_errores >= 3:
                print '\n'*5
                print 'SOS PELOTUDO?'
                print '\n'*5
            print ('No es una opción válida')
            raw_input('Presione enter para continuar')

if __name__ == '__main__':
    main()
