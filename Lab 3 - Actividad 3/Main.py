from InterfaceG import *
import numpy as np
    
if __name__ == '__main__':
    tipo_recorte = int(input("Ingrese 1 para recorte de líneas o 2 para polígonos: "))
    tipo_viewport = int(input("Ingrese la forma en la que quiere ingresar el viewport: 1 para EEI y ESD y 2 para (TOP, BOTTOM, LEFT, RIGHT) y 3 para ingresar cada vértice: "))
    
    if tipo_viewport == 1: # EII Y ESD
        puntos_viewport = definir_viewport_E() 
    elif tipo_viewport == 2: # TOP, BOTTOM, LEFT, RIGHT
        puntos_viewport = definir_viewport_TBLR()
    else: # todos los vértices
        puntos_viewport = definir_viewport_puntos()

    if tipo_recorte == 1: # recorte de líneas
        P1, P2 = ingresar_datos_linea()
        puntos_linea_completa = bresenham(P1, P2)
        #print ("todos los puntos: ", puntos_linea_completa)
        alg = seleccionar_algoritmo_linea()
        #print("puntos: ", P1, P2)
        if alg == 1: #Cohen-Sutherland
            puntos_linea_recorte = recorteCohenSutherland(P1, P2, EII=puntos_viewport[0], ESD=puntos_viewport[1])
            if not puntos_linea_recorte:
                print("La linea no está dentro del viewport.")
                mostrar_juego(puntos_viewport, puntos_linea_completa, tipo_viewport=tipo_viewport, tipo_recorte=1)
            else:
                #i_0 = puntos_linea_completa.index(puntos_linea_recorte[0])
                #i_f = puntos_linea_completa.index(puntos_linea_recorte[1])
                #puntos_dentro = puntos_linea_completa[i_0:i_f+1]
                puntos_dentro = bresenham(puntos_linea_recorte[0], puntos_linea_recorte[1])
                mostrar_juego(puntos_viewport, puntos_dentro, tipo_viewport=tipo_viewport, tipo_recorte=1)
        else: #Cyrus-Beck
            puntos_linea_recorte = recorteCyrusBeck(P1, P2, len(puntos_viewport),vertices_viewport=puntos_viewport)
            if not puntos_linea_recorte:
                print("La línea no se está dentro del viewport.")
                mostrar_juego(puntos_viewport, puntos_linea_completa, tipo_viewport=tipo_viewport, tipo_recorte=1)
            else:
                #i_0 = puntos_linea_completa.index(puntos_linea_recorte[0])
                #i_f = puntos_linea_completa.index(puntos_linea_recorte[1])
                #puntos_dentro = puntos_linea_completa[i_0:i_f+1]
                puntos_dentro = bresenham(puntos_linea_recorte[0], puntos_linea_recorte[1])
                mostrar_juego(puntos_viewport, puntos_dentro, tipo_viewport=tipo_viewport, tipo_recorte=1)
    else: # recorte de polígonos
        n, puntos_poligono = ingresar_datos_poligono()
        alg = seleccionar_algoritmo_poligono()
        if alg == 1: #Sutherland-Hodgman
            sutherlandHodgmanClip = recortePoligono()
            subject_polygon = np.array(puntos_poligono)
            clipping_polygon = np.array(puntos_viewport)
            """ print("subject_polygon: ", subject_polygon)
            print("clipping_polygon: ",clipping_polygon) """
            puntos_poligono_recorte = sutherlandHodgmanClip(subject_polygon, clipping_polygon)
            if not list(puntos_poligono_recorte) or len(puntos_poligono_recorte) == 0: 
                print("El polígono no está dentro del polígono de recorte.")
                mostrar_juego(puntos_viewport, puntos_poligono, tipo_viewport=tipo_viewport, tipo_recorte=2)
            else:
                mostrar_juego(puntos_viewport, puntos_poligono_recorte, tipo_viewport=tipo_viewport, tipo_recorte=2)
        else:  # Weiler-Atherton
            puntos_string = puntos_a_string(puntos_poligono)
            viewport_string = puntos_a_string(puntos_viewport)
            """ print("puntos string: ", puntos_string)
            print("viewport string: ", viewport_string) """
            puntos_poligono_recorte = recorteWeilerAtherton(puntos_string, viewport_string)[0].split(' ')
            puntos_poligono_recorte = list(map(lambda x: int(float(x)), puntos_poligono_recorte))
            puntos_poligono_recorte = agrupar(puntos_poligono_recorte, 2)

            if not puntos_poligono_recorte: 
                print("El polígono no está dentro del polígono de recorte.")
                mostrar_juego(puntos_viewport, puntos_poligono, tipo_viewport=tipo_viewport, tipo_recorte=2)
            else:
                 mostrar_juego(puntos_viewport, puntos_poligono_recorte, tipo_viewport=tipo_viewport, tipo_recorte=2)