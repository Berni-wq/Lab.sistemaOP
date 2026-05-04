#Grupo: 04 | Técnica: Semáforos (threading.Semaphore)
#Integrantes: Bernardo Casanga, Maximiliano Uribe,
#Esteban Cortés, Felipe Segura
#Asignatura: Sistemas Operativos | Universidad La Serena
import threading
import random
import time

#SEMÁFORO: controla el acceso al saldo compartido.
#Valor inicial 1 = solo UN hilo puede operar a la vez.
#Si fuera 2, dos hilos podrían modificar el saldo al mismo tiempo o sea error.
#semaforo = threading.Semaphore(1)

saldo = 1000.0        # saldo inicial compartido entre ambos hilos
operaciones = []      # lista compartida: el productor escribe, el consumidor lee
NUM_OPERACIONES = 8
archivo_salida = "resultados.txt"
