from re import X
import gamelib

o = "o"
x = "x"
celda = "-"
celda_t = 50

ANCHO_VENTANA = 300
ALTO_VENTANA = 300

def juego_crear():
    """Inicializar el estado del juego"""

    tabla = [[celda for c in range(10)]  for f in range(10)]

    return tabla

def crear_tabla(juego):
    """ Crea la grilla a partir del turno correspondiente en el juego. """

    tabla = []

    for f in range(len(juego)):
        fila = []
        for c in range(len(juego[0])):
            fila.append(juego[f][c])
        tabla.append(fila)

    return tabla

def hay_celda(juego, x, y):
    "Devuelve True si hay una celda vacia en la posicion x ---> (columna), y ---> (fila). "

    if juego[y][x] == celda:
        return True
    return False

def hay_o(juego, x, y):
    "Devuelve True si hay una o en la posicion x ---> (columna), y ---> (fila). "

    if juego[y][x] == o:
        return True
    return False

def turno(juego):
    """ Devuelve el jugador del turno correspondiente. """

    juego = crear_tabla(juego)
    contador = 0

    for f in juego:
        contador += f.count(o) + f.count(x)

    if contador % 2 == 0:
        return o

    return x
    
def juego_actualizar(juego, x, y):
    """Actualizar el estado del juego

    x e y son las coordenadas (en pixels) donde el usuario hizo click.
    Esta función determina si esas coordenadas corresponden a una celda
    del tablero; en ese caso determina el nuevo estado del juego y lo
    devuelve.
    """
    x = x//celda_t
    y = y//celda_t
    juego_n = crear_tabla(juego)

    if x < len(juego_n[0]) and y < len(juego_n) and hay_celda(juego_n, x, y):
        juego_n[y][x] = turno(juego)

    return juego_n
    
def juego_mostrar(juego):
    """Actualizar la ventana"""

    juego_n = crear_tabla(juego)

    gamelib.draw_begin()
    for y, fila in enumerate(juego_n):
        for x in range(len(fila)):
            if hay_celda(juego_n, x, y):
                gamelib.draw_rectangle(
                    x * celda_t, 
                    y * celda_t, 
                    x * celda_t + celda_t, 
                    y * celda_t + celda_t,
                    outline='white', 
                    fill='black')
            elif hay_o(juego_n, x, y):
                gamelib.draw_oval(
                    x * celda_t, 
                    y * celda_t, 
                    x * celda_t + celda_t, 
                    y * celda_t + celda_t, 
                    outline='yellow', 
                    fill='red')
            else:
                gamelib.draw_line(
                    x * celda_t, 
                    y * celda_t, 
                    x * celda_t + celda_t, 
                    y * celda_t + celda_t,  
                    fill='yellow', 
                    width=2)
                gamelib.draw_line(
                    x * celda_t, 
                    y * celda_t + celda_t, 
                    x * celda_t + celda_t, 
                    y * celda_t,  
                    fill='yellow', 
                    width=2)
                    
    gamelib.draw_text('Juego: cinco en línea', 100, len(juego) * celda_t + 20, size = 11)
    gamelib.draw_text(f'Es el turno de: {turno(juego)}', 400, len(juego) * celda_t + 20, size = 14)
    gamelib.draw_end()

def main():
    juego = juego_crear()

    # Ajustar el tamaño de la ventana
    gamelib.resize(len(juego[0]) * celda_t, len(juego) * celda_t + celda_t)

    # Mientras la ventana esté abierta:
    while gamelib.is_alive():
        # Todas las instrucciones que dibujen algo en la pantalla deben ir
        # entre `draw_begin()` y `draw_end()`:
        juego_mostrar(juego)

        # Terminamos de dibujar la ventana, ahora procesamos los eventos (si el
        # usuario presionó una tecla o un botón del mouse, etc).

        # Esperamos hasta que ocurra un evento
        ev = gamelib.wait()

        if not ev:
            # El usuario cerró la ventana.
            break

        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            # El usuario presionó la tecla Escape, cerrar la aplicación.
            break

        if ev.type == gamelib.EventType.ButtonPress:
            # El usuario presionó un botón del mouse
            x, y = ev.x, ev.y # averiguamos la posición donde se hizo click
            juego = juego_actualizar(juego, x, y)

gamelib.init(main)