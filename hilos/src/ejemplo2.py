from threading import Thread, Condition
import time, random


class Productor(Thread):
    def __init__(self, lista, condicion):
        Thread.__init__(self)
        self.lista = lista
        self.condicion = condicion

    def run(self):
        while True:
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


class Consumidor(Thread):
    def __init__(self, lista, condicion):
        Thread.__init__(self)
        self.lista = lista
        self.condicion = condicion

    def run(self):
        while True:
            self.condicion.acquire()
            #print'condicion adquirida por %s' % self.name
            while True:
                if self.lista:
                    lista = self.lista.pop()
                    #print '%d removido de la lista por %s' % (lista, self.name)
                    break
                #print'Condicion espera por %s' % self.name
                self.condicion.wait()
            #print'condicion liberada por %s' % self.name
            self.condicion.release()


def main():
    lista = []
    condicion = Condition()
    hilo1 = Productor(lista, condicion)
    hilo2 = Consumidor(lista, condicion)
    hilo1.start()
    hilo2.start()
    hilo1.join()
    hilo2.join()

main()
