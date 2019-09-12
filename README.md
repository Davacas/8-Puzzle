# 8-Puzzle
Solución al 8-puzzle utilizando BFS, DFS o Hill Climbing.

El programa abstrae el tablero como tuplas de números donde el 0 representa un espacio en blanco, de modo que el estado:<br>
| 1 | 2 | 3 |<br>
| 4 | 5 | 6 |<br>
| 7 | 8 |&nbsp;&nbsp;&nbsp;&nbsp;|<br>
se traduce a: (1, 2, 3, 4, 5, 6, 7, 8, 0).

Tanto el estado inicial como el estado final están hardcodeados en la función main.<br>
El estado inicial es: (4, 2, 1, 7, 3, 5, 0, 8, 6)<br>
El estado final es:   (1, 2, 3, 4, 5, 6, 7, 8, 0)

Al iniciar, el programa muestra un menú al usuario preguntando cual de los tres algoritmos correr. Posteriormente permite imprimir la solución encontrada (si es que se encontró).

A futuro, se pretende que el usuario pueda teclear el estado inicial y pueda jugar libremente.
