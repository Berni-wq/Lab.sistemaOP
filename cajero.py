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
semaforo = threading.Semaphore(1)

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
        
        # acquire() "tomo el semaaforo", bloqueo a otros hilos
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
 
            # acquire() entra a la sección crítica
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
        
if _name_ == "_main_":
    print("\n=== SIMULADOR DE CAJERO AUTOMÁTICO ===")
    print(f"Saldo inicial: ${saldo:.2f}")
    print("Iniciando hilos...\n")
 
    hilo_productor  = threading.Thread(target=generar_transacciones)
    hilo_consumidor = threading.Thread(target=procesar_transacciones)
 
    # Ambos hilos arrancan "al mismo tiempo"
    # Sin el semáforo, podrían leer/escribir saldo simultáneamente → corrupción de datos
    hilo_productor.start()
    hilo_consumidor.start()
 
    hilo_productor.join()   # espera a que el productor termine
    hilo_consumidor.join()  # espera a que el consumidor termine
 
    print(f"\nSaldo final: ${saldo:.2f}")
    print(f"Registro guardado en '{archivo_salida}'")
    print("=== FIN ===\n")

 # RESPUESTAS A PREGUNTAS a) – f)

 
# a) ¿Qué es la sincronización de procesos?
#    Es el conjunto de mecanismos que coordinan el acceso de múltiples hilos
#    o procesos a recursos compartidos, garantizando que las operaciones se
#    ejecuten en un orden correcto y sin interferencias. Sin sincronización,
#    dos hilos pueden leer y escribir el mismo dato al mismo tiempo,
#    produciendo resultados incorrectos (race condition).

# b) ¿Qué es un semáforo?
#    Es una variable entera protegida que soporta dos operaciones atómicas:
#    acquire() (wait/P): decrementa el contador. Si llega a 0, el hilo se bloquea
#    hasta que otro hilo libere el semáforo.
#    release() (signal/V): incrementa el contador y despierta a un hilo en espera.
#    Con valor inicial 1 actúa como mutex (exclusión mutua binaria).
#    Con valor mayor, permite que N hilos accedan simultáneamente al recurso.

# c) ¿Qué es un mutex?
#    Mutex significa "mutual exclusion" (exclusión mutua). Es un mecanismo de
#    sincronización que garantiza que solo UN hilo pueda acceder a una sección
#    crítica a la vez. A diferencia del semáforo, el mutex tiene dueño: solo el
#    hilo que lo adquirió puede liberarlo. En Python se implementa con
#    threading.Lock(). Es más simple que el semáforo pero menos flexible.

# d) ¿Qué es un monitor?
#    Es una estructura de sincronización de alto nivel que encapsula variables
#    compartidas, procedimientos y la sincronización en un solo módulo.
#    Garantiza que solo un hilo ejecute cualquier procedimiento del monitor
#    a la vez. En Python se aproxima con threading.Condition(), que combina
#    un lock con la capacidad de esperar y notificar condiciones específicas.

# e) ¿Qué es una variable condicional?
#    Es un mecanismo que permite a un hilo suspenderse y esperar hasta que
#    otro hilo le notifique que cierta condición se cumplió. Se usa siempre
#    dentro de un monitor o lock. Sus operaciones principales son:
#    wait(): libera el lock y suspende el hilo hasta recibir una notificación.
#    notify(): despierta a un hilo que esté esperando la condición.
#    En Python se implementa con threading.Condition().

# f) Conclusión comparativa
#    El semáforo es una solución intermedia entre el Lock y el Monitor:
#    más flexible que el Lock porque puede controlar cuántos hilos acceden
#    simultáneamente (no solo uno), pero más simple que el Monitor porque
#    no encapsula datos ni lógica, solo controla el acceso.
#    En nuestro cajero bancario fue la elección ideal: necesitábamos que
#    exactamente UN hilo modificara el saldo a la vez, y el semáforo con
#    valor 1 lo garantiza de forma clara y directa.
#    Comparado con el Algoritmo del Panadero (Grupo 2), el semáforo es
#    mucho más simple de implementar porque delega el control al sistema
#    operativo en vez de resolverlo por software puro.
#    La desventaja del semáforo es que si olvidas el release(), produces
#    un deadlock. El Monitor lo evita mejor porque gestiona eso internamente.
