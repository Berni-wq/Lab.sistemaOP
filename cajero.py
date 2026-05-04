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

# HILO PRODUCTOR: genera transacciones aleatorias
# Simula clientes haciendo depósitos o retiros en el cajero

def generar_transacciones():
    tipos = ["DEPÓSITO", "RETIRO"]
    for i in range(NUM_OPERACIONES):
        tipo = random.choice(tipos)
        monto = round(random.uniform(50, 500), 2)
        
        # acquire() "tomo el semáforo", bloqueo a otros hilos
        semaforo.acquire()
        operaciones.append((tipo, monto))
        print(f"  [Cajero] Transacción ingresada: {tipo} ${monto}")
        semaforo.release()
        # release() "libero el semáforo", el otro hilo puede entrar
        
        time.sleep(0.3)  # simula el tiempo entre operaciones reales