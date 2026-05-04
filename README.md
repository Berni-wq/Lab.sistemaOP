# Lab.sistemaOP
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
