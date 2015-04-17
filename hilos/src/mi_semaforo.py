import threading
import random
from time import sleep

semaforo = 0
fin = False
comidas = {
    1: 'asado',
    2: 'hamburguesa',
    3: 'helado',
    4: 'ensalada',
    5: 'lomito',
    6: 'poio',
    7: 'pizza',
    8: 'milanesa',
    9: 'chocolate',
    10: 'tomates'
}


def worker(count):
    #print 'soy un hilo (%s, %i)' % (random.random(), int(random.random()))
    #aca llamo a las variables globales definidas arriba
    global semaforo
    global fin
    #quiero q los hilos entren en orden, 0, 1, 2, ...
    if count == semaforo:
        for x in range(10):
            print 'soy el hilo %i en su corrida numero %i' % (count, x)
            sleep(1)

            #termine las iteraciones, dejemos que entre el otro hilo
            if x == 9:
                print 'Termine con el hilo %i' % count
                semaforo = semaforo + 1

                #se ejecutaron todos mis hilos, seteemos semaforo a 0 
                #para no dejarlo en 3, no es necesario en realidad
                if semaforo == 3:
                    semaforo = 0
                    #lo seteo a True para que en el else, termine
                    fin = True

    #aca hago que los hilos a los q no les corresponde el semaforo se vuelvan a llamar
    else:
        if not fin:
            sleep(3)
            worker(count)

    return


threads = list()

for i in range(3):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()