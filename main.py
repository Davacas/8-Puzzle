from collections import deque

#Clase que define un nodo en el 8-puzzle.
class Nodo:
    def __init__(self, estado, padre, movimiento, profundidad, piezas_correctas):        
        self.estado = estado                        #Posición atual de las piezas.
        self.padre = padre                          #Nodo desde el que se llega a este nodo.
        self.movimiento = movimiento                #Movimiento para encontrar este nodo desde el padre.
        self.profundidad = profundidad              #Posición del nodo en el árbol de búsqueda.
        self.piezas_correctas = piezas_correctas    #Total de piezas en su lugar para este estado.

    #Método para mover las piezas en direcciones posibles.
    def mover(self, direccion):
        estado = list(self.estado)
        ind = estado.index(0)

        if direccion == "arriba":            
            if ind not in [6, 7, 8]:                
                temp = estado[ind + 3]
                estado[ind + 3] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == "abajo":            
            if ind not in [0, 1, 2]:                
                temp = estado[ind - 3]
                estado[ind - 3] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == "derecha":            
            if ind not in [0, 3, 6]:                
                temp = estado[ind - 1]
                estado[ind - 1] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == "izquierda":            
            if ind not in [2, 5, 8]:                
                temp = estado[ind + 1]
                estado[ind + 1] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None        

    #Método que encuentra y regresa todos los nodos sucesores del nodo actual.
    def encontrar_sucesores(self):
        sucesores = []
        sucesorN = self.mover("arriba")
        sucesorS = self.mover("abajo")
        sucesorE = self.mover("derecha")
        sucesorO = self.mover("izquierda")
        
        sucesores.append(Nodo(sucesorN, self, "arriba", self.profundidad + 1, calcular_heurisitica(sucesorN)))
        sucesores.append(Nodo(sucesorS, self, "abajo", self.profundidad + 1, calcular_heurisitica(sucesorS)))
        sucesores.append(Nodo(sucesorE, self, "derecha", self.profundidad + 1, calcular_heurisitica(sucesorE)))
        sucesores.append(Nodo(sucesorO, self, "izquierda", self.profundidad + 1, calcular_heurisitica(sucesorO)))
        
        sucesores = [nodo for nodo in sucesores if nodo.estado != None]  
        return sucesores

    #Método que encuentra el camino desde el nodo inicial hasta el actual.
    def encontrar_camino(self, inicial):
        camino = []
        nodo_actual = self
        while nodo_actual.profundidad >= 1:
            camino.append(nodo_actual)
            nodo_actual = nodo_actual.padre
        camino.reverse()
        return camino

    #Método que imprime ordenadamente el estado (piezas) de un nodo.
    def imprimir_nodo(self):
        renglon = 0
        for pieza in self.estado:
            if pieza == 0:
                print(" ", end = " ")
            else:
                print (pieza, end = " ")
            renglon += 1
            if renglon == 3:
                print()
                renglon = 0       

#Función que calcula la cantidad de piezas que están en su lugar para un estado dado.
def calcular_heurisitica(estado):
    correcto = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    valor_correcto = 0
    piezas_correctas = 0
    if estado:
        for valor_pieza, valor_correcto in zip(estado, correcto):
            if valor_pieza == valor_correcto:
                piezas_correctas += 1
            valor_correcto += 1
    return piezas_correctas   

#Algoritmo Breadth First Search.
def bfs(inicial, meta):
    visitados = set()   #Conjunto de estados visitados para no visitar el mismo estado más de una vez.
    frontera = deque()  #Cola de nodos aún por explorar. Se agrega el nodo inicial.  
    frontera.append(Nodo(inicial, None, None, 0, calcular_heurisitica(inicial)))
    
    while frontera:                         #Mientras haya nodos por explorar:
        nodo = frontera.popleft()           #Se toma el primer nodo de la cola.

        if nodo.estado not in visitados:    #Si no se había visitado, 
            visitados.add(nodo.estado)      #se agrega al conjunto de visitados.
        else:                               #Si ya se había visitado
            continue                        #se ignora.
        
        if nodo.estado == meta:                         #Si es una meta, 
            print("\n¡Se encontró la meta!")            
            return nodo.encontrar_camino(inicial)       #se regresa el camino para llegar a él y termina el algoritmo.        
        else:                                           #Si no es una meta, 
            frontera.extend(nodo.encontrar_sucesores()) #se agregan sus sucesores a los nodos por explorar.

#Algoritmo Depth First Search.
def dfs(inicial, meta, profundidad_max):
    visitados = set()   #Conjunto de estados visitados para no visitar el mismo estado más de una vez.
    frontera = deque()  #Pila de nodos aún por explorar. Se agrega el nodo inicial.
    frontera.append(Nodo(inicial, None, None, 0, calcular_heurisitica(inicial)))
    
    while frontera:                         #Mientras haya nodos por explorar:
        nodo = frontera.pop()               #Se toma el primer nodo de la pila.

        if nodo.estado not in visitados:    #Si no se había visitado, 
            visitados.add(nodo.estado)      #se agrega al conjunto de visitados.
        else:                               #Si ya se visitó,
            continue                        #se ignora.
        
        if nodo.estado == meta:             #Si es una meta, se regresa el camino para llegar a él y termina el algoritmo.
            print("\n¡Se encontró la meta!")            
            return nodo.encontrar_camino(inicial)
        else:                               #Si no es una meta:             
            if profundidad_max > 0:                             #Si se estableció una búsqueda con profundidad limitada
                if nodo.profundidad < profundidad_max:          #y no se ha llegado al límite,                 
                    frontera.extend(nodo.encontrar_sucesores()) #se agregan los sucesores a los nodos por explorar.
            else:                                               #Si no se estableció una búsqueda con profundidad limitada,
                frontera.extend(nodo.encontrar_sucesores())     #se agregan los sucesores a los nodos por explorar.

#Algoritmo Hill Climbing.
def hc(inicial):
    visitados = set()  #Conjunto de estados visitados para no visitar el mismo estado más de una vez.
    nodo_actual = Nodo(inicial, None, None, 0, calcular_heurisitica(inicial))

    while nodo_actual.piezas_correctas < 9:             #Mientras el estado actual no tenga todas las piezas en su lugar:
        sucesores = nodo_actual.encontrar_sucesores()   #Se buscan los sucesores del estado actual
        max_piezas_correctas = -1

        #Para cada nodo en los sucesores, se busca el que tenga más piezas en su lugar.
        for nodo in sucesores:   
            if nodo.piezas_correctas >= max_piezas_correctas and nodo not in visitados:
                max_piezas_correctas = nodo.piezas_correctas
                nodo_siguiente = nodo

            visitados.add(nodo_actual)

        #Si el nodo encontrado tiene más piezas en su lugar que el nodo actual, 
        #se asigna como nodo actual para repetir la búsqueda sobre éste.
        if nodo_siguiente.piezas_correctas >= nodo_actual.piezas_correctas:
            nodo_actual = nodo_siguiente
        #Si no, significa que se llegó a un máximo local y el algoritmo no debe seguir.
        else:
            print("\nSe llegó a un máximo local. No se encontró la meta.")
            break
    else:
        print("\n¡Se encontró la meta!")        
    return nodo_actual.encontrar_camino(inicial)

#Función main.
def main():
    estado_final = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    estado_inicial = (4, 2, 1, 7, 3, 5, 0, 8, 6)
    #estado_inicial = (1, 2, 3, 4, 5, 0, 7, 8, 6)   #De este estado se puede resolver en un movimiento.

    #Menú principal
    print("Este programa encuentra la solución al 8-puzzle\nutilizando diferentes algoritmos.")
    print("El estado inicial del juego es: ")
    (Nodo(estado_inicial, None, None, 0, calcular_heurisitica(estado_inicial))).imprimir_nodo()
    print("\n¿Qué algoritmo desea correr? Escriba:")
    print("\t\"bfs\" para  correr Breadth First Search")
    print("\t\"dfs\" para  correr Depth First Search")
    print("\t\"hc\"  para  correr Hill Climbing")
    print("\tCualquier otra cosa para terminar el programa.")
    algoritmo = input("Su elección: ")

    #Selección de algoritmo
    if algoritmo == "bfs" or algoritmo == "BFS":
        print("Corriendo BFS. Por favor espere.")
        nodos_camino = bfs(estado_inicial, estado_final)

    elif algoritmo == "dfs" or algoritmo == "DFS":
        print("\n¿Establecer un límite de profundidad?")
        print("Escriba el límite como un entero mayor que 0")
        print("o cualquier otro entero para continuar sin límite.")
        profundidad_max = int(input("Profundidad: "))
        print("Corriendo DFS. Por favor espere.")
        nodos_camino = dfs(estado_inicial, estado_final, profundidad_max)

    elif algoritmo == "hc" or algoritmo == "HC":
        print("\nCorriendo Hill Climbing. Por favor espere...")
        nodos_camino = hc(estado_inicial)
    
    else:
        return 0

    #Se imprime el camino si existe y si el usuario lo desea.
    if nodos_camino:
        print ("El camino tiene", len(nodos_camino), "movimientos.")
        imprimir_camino = (input ("¿Desea imprimir dicho camino? s/n: "))

        if imprimir_camino == "s" or imprimir_camino == "S":
            print("\nEstado inicial:")
            (Nodo(estado_inicial, None, None, 0, calcular_heurisitica(estado_inicial))).imprimir_nodo()
            print ("Piezas correctas:", calcular_heurisitica(estado_inicial), "\n")
            input("Presione \"enter\" para continuar.")
            
            for nodo in nodos_camino:
                print("\nSiguiente movimiento:", nodo.movimiento)
                print("Estado actual:")
                nodo.imprimir_nodo()
                print("Piezas correctas:", nodo.piezas_correctas, "\n")     
                input("Presione \"enter\" para continuar.")
    else:
        print ("\nNo se encontró un camino con las condiciones dadas.")

    return 0    

if __name__ == "__main__":
    main()