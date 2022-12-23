import pygame as pg
import os, sys

from Algoritmos.Primitivas.Bresenham import bresenham
from Algoritmos.CohenSutherland import recorteCohenSutherland
from Algoritmos.CyrusBeck import recorteCyrusBeck
from Algoritmos.SutherlandHodgman import recortePoligono
from Algoritmos.WeilerAtherton import recorteWeilerAtherton

# Definimos x_max, y_max y x_min, y_min para el rectangulo
# Dado que los puntos diagonales son suficientes para definir un rectángulo, entonces

""" x_max = 10.0
y_max = 8.0
x_min = 4.0
y_min = 4.0 """

n = 480 #matriz nxn, 480 -> 1:1 pixel
ancho = 720 #ancho de la pantalla
alto = ancho
size = ancho // n #tamaño del lado de cada cuadrado

# origen de coordenadas, cambiar en caso de necesitar
x0 = 20
y0 = n-1

#configuración inicial de la pantalla
def setup():
    global pantalla 
    pg.init()
    pantalla = pg.display.set_mode((ancho, alto))
    pg.display.set_caption('Recorte de Líneas y Polígonos')
    pantalla.fill((255,255,255)) 

""" Creación de la cuadrícula """
def grid():
    x = 0
    y = 0
    limite_horizontal = alto
    limite_vertical = ancho
    for l in range(n+1):
        pg.draw.line(pantalla, (0,0,0), (x,0), (x, limite_horizontal))
        pg.draw.line(pantalla, (0,0,0), (0,y), (limite_vertical, y))
        x += size
        y += size

def put_pixel(x, y, color=(0,0,0)):
    global size
    pg.draw.rect(pantalla, color, ((x0 + x)*size, (y0 - y)*size, size, size))

def pintar_viewport_TBLR(TOP, BOTTOM, LEFT, RIGHT, color=(255,0,0)):
    
    top = bresenham([LEFT, TOP], [RIGHT, TOP]) #linea superior
    bottom = bresenham([LEFT, BOTTOM], [RIGHT, BOTTOM]) #linea inferior
    left = bresenham([LEFT, BOTTOM], [LEFT, TOP]) #linea de la izquierda
    right = bresenham([RIGHT, BOTTOM], [RIGHT, TOP]) #linea de la derecha
    lineas = [bottom, top, left, right]

    for linea in lineas:
        pintar_linea(linea, color=(255,0,0))

def pintar_viewport_vertices(vertices, color=(255,0,0)):
    pintar_poligono(vertices, color=color)

def pintar_viewport_E(EII, ESD):
    
    x_min, y_min = EII
    x_max, y_max = ESD
    
    top = bresenham([x_min, y_max], [x_max, y_max]) #linea superior
    bottom = bresenham([x_min, y_min], [x_max, y_min]) #linea inferior
    left = bresenham([x_min, y_min], [x_min, y_max]) #linea de la izquierda
    right = bresenham([x_max, y_min], [x_max, y_max]) #linea de la derecha
    lineas = [bottom, top, left, right]

    for linea in lineas:
        pintar_linea(linea, color=(0,200,100))

def pintar_linea(puntos, color=(0,0,0)):
    for punto in puntos:
        put_pixel(punto[0], punto[1], color=color)


def pintar_poligono(puntos, color=(0,0,0)):
    for i in range(0, len(puntos)-1): # range(0,4*) 4, 5
        puntos_recta = bresenham(puntos[i], puntos[i+1])
        pintar_linea(puntos_recta, color=color) # pendiente verificar 
    ultima_recta = bresenham(puntos[0], puntos[-1])
    pintar_linea(ultima_recta, color=color)
# bucle infinito para mostrar en patalla todos los elementos gráficos.
def mostrar_juego(viewport, puntos, tipo_viewport=None, tipo_recorte=None): 
    while True:        
        for event in pg.event.get():
            if event.type == pg.QUIT: #para detener la ejecución al cerrar la ventana
                pg.quit()
                sys.exit()

        #pintar el viewport
        if tipo_viewport == 1: # EII y ESD:
            pintar_viewport_E(viewport[0], viewport[1])
        elif tipo_viewport == 2: #TOP, BOTTOM, LEFT, RIGHT
            pintar_viewport_TBLR(viewport[0], viewport[1], viewport[2], viewport[3])
        else:
            pintar_viewport_vertices(viewport, color=(255,0,0))
        
        # pintar la línea o el polígono
        if tipo_recorte == 1: # recorte de línea
            pintar_linea(puntos)
        else: # recorte de polígono
            pintar_poligono(puntos)

        #pintar_linea(bresenham(P1,P2), (200,200,0))
        put_pixel(0, 0, (121,0,128)) #mostrar punto de origen relativo
        #pintar_poligono([[10,10], [20,10], [30, 20], [20, 30], [10, 30],[0,20]])
        #pintar_poligono(((0,0),(100,0),(50,100)))
        #pol = [[100, 290], [100, 210], [275, 230], [150, 250], [275, 270], [100, 290]]
        #pintar_poligono(pol)
        #grid() #mostrar la cuadrícula.
        #pantalla.fill((255,255,255))

        #pg.display.update()
        pg.display.flip() #actualizar el mundo para mostrar nuevos cambios.

""" Puntos de la EII y la ESD """
def definir_viewport_E():
    print("Ingrese los valores de la EII y la ESD del viewport")
    x1 = int(input("Ingrese x1: "))
    y1 = int(input("Ingrese y1: "))
    x2 = int(input("Ingrese x2: "))
    y2 = int(input("Ingrese y2: "))
    
    return [(x1,y1), (x2,y2)]

def definir_viewport_TBLR():
    top = int(input("Ingrese el valor para TOP: "))
    bottom = int(input("Ingrese el valor para BOTTOM: "))
    left = int(input("Ingrese el valor para LEFT: "))
    right = int(input("Ingrese el valor para RIGHT: "))

    return [top, bottom, left, right]

def definir_viewport_puntos():
    num_vertices = int(input("Ingrese el número de vértices del polígono de recorte (viewport): "))
    print("Ingrese los valores de cada punto para el viewport (en sentido horario)")
    lista_vertices = list()
    for i in range(num_vertices):
        lista_vertices.append((int(input(f"Ingrese x{i}: ")),int(input(f"Ingrese y{i}: "))))
    return lista_vertices

def ingresar_datos_linea():
    print("Ingrese los puntos inicial y final de la línea")
    x1 = int(input("Ingrese x1: "))
    y1 = int(input("Ingrese y1: "))
    x2 = int(input("Ingrese x2: "))
    y2 = int(input("Ingrese y2: "))

    return (x1,y1),(x2,y2)
    
def ingresar_datos_poligono():
    num_vertices = int(input("Ingrese el número de vértices del polígono: "))
    vertices_poligono = []
    for i in range(num_vertices):
        print(f"vértice {i}:")
        vertices_poligono.append(tuple([int(input("ingrese el valor de x: ")), int(input("ingrese el valor de y: "))]))
    return n, vertices_poligono

def seleccionar_algoritmo_linea():
    print("Seleccione el número del algoritmo que quiere usar:")
    print("1. Cohen-Sutherland")
    print("2. Cyrus-Beck")
    alg = int(input("Algoritmo: "))
    return alg

def seleccionar_algoritmo_poligono():
    print("Seleccione el número del algoritmo que quiere usar:")
    print("1. Sutherland-Hodgman")
    print("2. Weiler-Atherton")
    alg = int(input("Algoritmo: "))
    return alg

def puntos_a_string(puntos):
    lista = ""
    for punto in puntos:
        lista += str(punto[0])
        lista += " "
        lista += str(punto[1])
        lista += " "
    return lista

def agrupar(lista, n):
    i = 0
    nlista = [] #Lista
    while(i < len(lista)):
        nlista.append(lista[i:i+n])
        i += n
    return list(nlista)

setup() #pantalla

if __name__ == "__main__":
    """ x1 = 1
    y1 = 2
    x2 = 23
    y2 = 12
    vertices = [[5, 5], [20, 2], [16, 10], [10, 10]]
    puntos = CyrusBeckClip([x1,y1], [x2,y2], vertices_viewport=vertices)
    i_0 = puntos.index(puntos[0])
    i_f = puntos.index(puntos[1]) """
    """ print("i_0 = ", i_0)
    print("i_f = ", i_f)
    print("dentro: ", puntos[i_0:i_f+1]) """
    #mostrar_juego(viewport, puntos[i_0:i_f+1]) #mostrar el juego en pantalla.
    """ poligono = [[100,290],[100,210],[275,230],[150,250],[275,270],[100,290]]
    viewport =  [[200, 200], [400, 200], [400, 300], [200, 300]]
    nuevos_puntos = sutherlandHodgmanClip(poligono, viewport)
    mostrar_juego(viewport, nuevos_puntos, tipo_viewport=3, tipo_recorte=2) """
    print(definir_viewport_puntos())