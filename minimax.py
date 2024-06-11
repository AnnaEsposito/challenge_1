import random

tamaño_tablero = 5
pos_salida = (3, 2)  # ruta de salida del raton 

def movimientos_posibles(posicion, tamaño_tablero):
    x, y = posicion
    movimientos = [
        (x - 1, y),  # arriba
        (x + 1, y),  # abajo
        (x, y - 1),  # izquierda
        (x, y + 1)   # derecha
    ]
    return [(x, y) for x, y in movimientos if 0 <= x < tamaño_tablero and 0 <= y < tamaño_tablero]

def imprimir_tablero(tamaño, pos_gato, pos_raton,mensaje=None):
    if mensaje:
        print(mensaje)
    for i in range(tamaño):
        for j in range(tamaño):
            if (i, j) == pos_gato:
                print('G', end=' ')
            elif (i, j) == pos_raton:
                print('R', end=' ')
            else:
                print('.', end=' ')
        print()
    print()

def utilidad(pos_gato, pos_raton):
    if pos_gato == pos_raton:
        return float('inf')  # Gato gana
    dist = abs(pos_gato[0] - pos_raton[0]) + abs(pos_gato[1] - pos_raton[1])
    return -dist  # Menor distancia es peor para el ratón

def minimax(pos_gato, pos_raton, profundidad, maximizando):
    if profundidad == 0 or pos_gato == pos_raton:
        return utilidad(pos_gato, pos_raton)
    
    if maximizando:
        max_eval = float('-inf')
        for movimiento in movimientos_posibles(pos_gato,tamaño_tablero):
            eval = minimax( movimiento, pos_raton, profundidad - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for movimiento in movimientos_posibles(pos_raton,tamaño_tablero):
            eval = minimax(pos_gato, movimiento, profundidad - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


def movimiento_raton(pos_raton, pos_salida, tamaño_tablero):
    posibles_movimientos = movimientos_posibles(pos_raton, tamaño_tablero)
    mejor_movimiento = None
    mejor_distancia = float('inf')
    
    for movimiento in posibles_movimientos:
        distancia = abs(movimiento[0] - pos_salida[0]) + abs(movimiento[1] - pos_salida[1])
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_movimiento = movimiento
    
    return mejor_movimiento

def jugar(tamaño, pos_gato, pos_raton, profundidad, max_turnos,pos_salida):
    tablero = (tamaño, pos_gato, pos_raton)
    turno_gato = True
    turno_actual = 0
    
    #Para imprimir el estado inicial del tablero
    imprimir_tablero(tamaño, pos_gato, pos_raton, mensaje="Estado inicial del tablero:")

    while pos_gato != pos_raton and turno_actual < max_turnos:  
        imprimir_tablero(tamaño, pos_gato, pos_raton)

        if turno_gato:
            mejor_movimiento = None
            mejor_valor = float('-inf')
            for movimiento in movimientos_posibles(pos_gato, tamaño):
                valor = minimax(movimiento, pos_raton, profundidad, False)
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = movimiento
            print(f"Turno {turno_actual + 1}: El gato se mueve de {pos_gato} a {mejor_movimiento}")
            pos_gato = mejor_movimiento
        else:
            nuevo_movimiento_raton = movimiento_raton(pos_raton, pos_salida, tamaño)
            print(f"Turno {turno_actual + 1}: El ratón se mueve de {pos_raton} a {nuevo_movimiento_raton}")
            pos_raton = nuevo_movimiento_raton
       
        turno_gato = not turno_gato
        turno_actual += 1

        
        if pos_raton == pos_salida:
            imprimir_tablero(tamaño, pos_gato, pos_raton)
            print("El ratón ha escapado!")
            return
    
    imprimir_tablero(tamaño, pos_gato, pos_raton)
    if pos_gato == pos_raton:
        print("El gato ha capturado al ratón!")
    else:
        print("Se acabaron los intentos")

# Inicializar y jugar
jugar(tamaño=5, pos_gato=(0, 0), pos_raton=(4, 4), profundidad=3, max_turnos=10,pos_salida=pos_salida)
