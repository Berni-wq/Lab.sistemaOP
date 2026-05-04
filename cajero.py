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

# HILO CONSUMIDOR: procesa las transacciones y actualiza el saldo
# Valida que los retiros no dejen el saldo negativo

def procesar_transacciones():
    global saldo
    procesadas = 0
 
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write("=== REGISTRO DE CAJERO AUTOMÁTICO ===\n")
        f.write(f"Saldo inicial: ${saldo:.2f}\n\n")
 
        while procesadas < NUM_OPERACIONES:
            time.sleep(0.5)  # espera un poco antes de intentar procesar
 
            # acquire() → entra a la sección crítica
            semaforo.acquire()
            if operaciones:
                tipo, monto = operaciones.pop(0)  # toma la primera transacción pendiente
 
                if tipo == "DEPÓSITO":
                    saldo += monto
                    estado = " APROBADO"
                elif tipo == "RETIRO":
                    if monto <= saldo:
                        saldo -= monto
                        estado = " APROBADO"
                    else:
                        estado = "✗ RECHAZADO (saldo insuficiente)"
 
                linea = f"{tipo:<10} ${monto:>7.2f}  →  {estado:<30}  Saldo: ${saldo:.2f}"
                print(f"  [Banco]  {linea}")
                f.write(linea + "\n")
                procesadas += 1
            semaforo.release()
            # release()  sale de la sección crítica
 
        # resumen final
        f.write(f"\nSaldo final: ${saldo:.2f}\n")
        f.write("=== FIN DEL REGISTRO ===\n")
