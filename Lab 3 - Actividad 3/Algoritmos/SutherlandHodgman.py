import numpy as np
import warnings

# LOS PUNTOS DEBEN SER PRESENTADOS EN EL SENTIDO DE LAS AGUJAS DEL reloj O 
# DE LO CONTRARIO ESTO NO FUNCIONARÁ

class recortePoligono:
    
    def init(self,warn_if_empty=True):
        self.warn_if_empty = warn_if_empty
    
    def adentro(self,p1,p2,q):
        R = (p2[0] - p1[0]) * (q[1] - p1[1]) - (p2[1] - p1[1]) * (q[0] - p1[0])
        if R <= 0:
            return True
        else:
            return False

    def calcularInterseccion(self,p1,p2,p3,p4):
        
        """
        Dados los puntos p1 y p2 en la línea L1, calcule la ecuación de L1 en el formato de 
        y = m1 * x + b1. Además, dados los puntos p3 y p4 en la línea L2, calcule la ecuación 
        de L2 en el formato de y = m2 * x + b2.
        
        Para calcular el punto de intersección de las dos rectas, igualar
        las dos ecuaciones de línea juntas
        
        m1 * x + b1 = m2 * x + b2
        
        y resolver para x. Una vez obtenido x, sustituirlo en uno de los
        ecuaciones para obtener el valor de y.
        
        si una de las rectas es vertical, entonces la coordenada x del punto de 
        intersección será la coordenada x de la recta vertical. Tenga en cuenta 
        que no es necesario verificar si ambas líneas son verticales (paralelas), 
        ya que esta función solo se llama si sabemos que las líneas se cruzan.
        """
        
        # si la primera línea es vertical
        if p2[0] - p1[0] == 0:
            x = p1[0]
            
            # pendiente e intersección de la segunda línea
            m2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
            b2 = p3[1] - m2 * p3[0]
            
            # y-coordenada de intersección
            y = m2 * x + b2
        
        # si la segunda línea es vertical
        elif p4[0] - p3[0] == 0:
            x = p3[0]
            
            # pendiente e intercepción de la primera línea
            m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
            b1 = p1[1] - m1 * p1[0]
            
            # y-coordenada de intersección
            y = m1 * x + b1
        
        # si ninguna de las lineas es vertical
        else:
            m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
            b1 = p1[1] - m1 * p1[0]
            
            # pendiente e intersección de la segunda línea
            m2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
            b2 = p3[1] - m2 * p3[0]
        
            # x-coordenada de intercesión
            x = (b2 - b1) / (m1 - m2)
        
            # y-coordenada de intercesión
            y = m1 * x + b1
        
        interseccion = (x,y)
        
        return interseccion
    
    def recorteSutherlandHodgman(self,sub_polygon,recortarPoligono):
        
        poligonoFinal = sub_polygon.copy()
        
        for i in range(len(recortarPoligono)):
            
            # almacena los vértices de la siguiente iteración del procedimiento de recorte
            sigPoligono = poligonoFinal.copy()
            
            # almacena los vértices del polígono recortado final
            poligonoFinal = []
            
           # estos dos vértices definen un segmento de línea (borde) en el recorte
           # polígono. Se supone que los índices se envuelven, de modo que si
           # i = 1, entonces i - 1 = K.
            c_edge_start = recortarPoligono[i - 1]
            c_edge_end = recortarPoligono[i]
            
            for j in range(len(sigPoligono)):
                
                # estos dos vértices definen un segmento de línea (borde) en el sujeto
                # polígono
                s_edge_start = sigPoligono[j - 1]
                s_edge_end = sigPoligono[j]
                
                if self.adentro(c_edge_start,c_edge_end,s_edge_end):
                    if not self.adentro(c_edge_start,c_edge_end,s_edge_start):
                        interseccion = self.calcularInterseccion(s_edge_start,s_edge_end,c_edge_start,c_edge_end)
                        poligonoFinal.append(interseccion)
                    poligonoFinal.append(tuple(s_edge_end))
                elif self.adentro(c_edge_start,c_edge_end,s_edge_start):
                    interseccion = self.calcularInterseccion(s_edge_start,s_edge_end,c_edge_start,c_edge_end)
                    poligonoFinal.append(interseccion)
        
        return np.asarray(poligonoFinal)
    
    def call(self,A,B):
        recortarPoligono = self.recorteSutherlandHodgman(A,B)
        """ if len(clipped_polygon) == 0 and self.warn_if_empty:
            warnings.warn("No intersections found. Are you sure your \
                          polygon coordinates are in clockwise order?")
         """
        return recortarPoligono

if __name__ == 'main':
    
    # algunos polígonos de prueba
    
    sutherlandHodgmanClip = recortePoligono()
    
    # cuadrados
    # sujeto_polígono = [(-1,1),(1,1),(1,-1),(-1,-1)]
    # polígono_recortado = [(0,0),(0,2),(2,2),(2,0)]
    
    # cuadrados: diferente orden de puntos
    subject_polygon = [(-1,-1),(-1,1),(1,1),(1,-1)]
    clipping_polygon = [(2,0),(0,0),(0,2),(2,2)]
    
    # triangulos
    # sujeto_polígono = [(0,0),(2,1),(2,0)]
    # polígono_recortado = [(1,0.5),(3,1.5),(3,0.5)]
    
    # estrella y cuadrado
    #subject_polygon = [(0,3),(0.5,0.5),(3,0),(0.5,-0.5),(0,-3),(-0.5,-0.5),(-3,0) ,(-0.5,0.5)]
    #clipping_polygon = [(-2,-2),(-2,2),(2,2),(2,-2)]
    
    # estrella y triangulo
    # sujeto_polígono = [(0,3),(0.5,0.5),(3,0),(0.5,-0.5),(0,-3),(-0.5,-0.5),(-3,0) ,(-0.5,0.5)]
    # polígono_recortado = [(0,2),(2,-2),(-2,-2)]
    
    subject_polygon = np.array(subject_polygon)
    clipping_polygon = np.array(clipping_polygon)

    print("subject_polygon: ", subject_polygon)
    print("clipping_polygon: ",clipping_polygon)
    clipped_polygon = sutherlandHodgmanClip(subject_polygon, clipping_polygon)
    print("res: ",clipped_polygon)