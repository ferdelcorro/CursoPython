import threading
import random
import time

elementos = {
    1: 'Asado',
    2: 'Helado',
    3: 'Manzana',
    4: 'Fideos',
    5: 'Lasagna',
    6: 'Pizza',
    7: 'Poio',
    8: 'Milanesas',
    9: 'Tomates verdes fritos',
    0: 'Chocolates'
}

pila = []

vivo = []


def vida_soft(p_vivo):
    time.sleep(20)
    print "Muerte"
    p_vivo.append(False)
    return


def productor(p_pila, p_vivo):
    while len(p_vivo) == 0:
        if len(p_pila) < 10:
            new_element = elementos[int(random.random()*10)]
            #print "Poductor: %s" % new_element
            print p_pila
            p_pila.append(new_element)
        rnd_time = random.random()
        while rnd_time > 0.5:
            rnd_time = random.random()
        time.sleep(rnd_time)
    return


def consumidor(nro, p_pila, p_vivo):
    while len(p_vivo) == 0:
        if len(p_pila) > 0:
            elemento_tmp = p_pila.pop()
            #print 'Consumidor(%i): %s ' % (nro, elemento_tmp)
            print p_pila
        rnd_time = random.random()
        while rnd_time < 0.5:
            rnd_time = random.random()
        time.sleep(rnd_time)
    return

t_vida = threading.Thread(target=vida_soft, args=(vivo,))
t_vida.start()
t_productor = threading.Thread(target=productor, args=(pila, vivo))
t_productor.start()
for i in range(3):
    t_consumidor = threading.Thread(target=consumidor, args=(i, pila, vivo))
    t_consumidor.start()