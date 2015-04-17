from threading import Thread, Condition
import time, random


class Terminador(Thread):
    def __init__(self, time):
        Thread.__init__(self)
        self.time = time

    def run(self):
        time.sleep(10)
        print '10 segundos, chau\n'
        self.time.append(False)
        print 'hilo3 dead\n'


class Productor(Thread):
    def __init__(self, lista, condicion, consumidores, time):
        Thread.__init__(self)
        self.lista = lista
        self.condicion = condicion
        self.consumidores = consumidores
        self.time = time

    def run(self):
        while len(self.time) == 0:
            lista = random.randint(0, 10)
            self.condicion.acquire()
            #print 'Condicion adquirida por %s' % self.name
            self.lista.append(lista)
            #print '%d agregado a la lista por %s' % (lista, self.name)
            #print 'Condicion notificada por %s' % self.name
            self.condicion.notify()
            #print 'Condicion liberada por %s' % self.name
            self.condicion.release()
            print '='*self.lista[0]
            time.sleep(random.random())

        #Esto es porque si no, el consumidor queda colgado en el segundo while, 
        #por el self.condicion.wait()
        for i in range(self.consumidores):
            self.condicion.acquire()
            self.condicion.notify()
            self.condicion.release()
        self.__stop = True
        print 'hilo1 dead\n'
        return


class Consumidor(Thread):
    def __init__(self, lista, condicion, i, time):
        Thread.__init__(self)
        self.lista = lista
        self.condicion = condicion
        self.number = i
        self.time = time

    def run(self):
        while len(self.time) == 0:
            self.condicion.acquire()
            #print'condicion adquirida por %s %i' % (self.name, self.number)
            while len(self.time) == 0:
                if self.lista:
                    lista = self.lista.pop()
                    print '%d removido de la lista por %s number %i' % (lista, self.name, self.number)
                    break
                #print'Condicion espera por %s' % self.number
                self.condicion.wait()
            #print'condicion liberada por %s' % self.number
            self.condicion.release()
        self.__stop = True
        print 'hilo2 number %i dead\n' % self.number
        return


def main():
    lista = []
    fin = []
    cant_hilos = 3

    condicion = Condition()
    hilo1 = Productor(lista, condicion, cant_hilos, fin)
    #hilo2 = Consumidor(lista, condicion, fin)
    hilo3 = Terminador(fin)

    #Creemos varios consumidores, para hacerlo divertido
    for i in range(cant_hilos):
        hilo2 = Consumidor(lista, condicion, i, fin)
        hilo2.start()
    hilo1.start()
    #hilo2.start()
    hilo3.start()
    hilo1.join()
    #hilo2.join()
    hilo3.join()

if __name__ == "__main__":
    main()
