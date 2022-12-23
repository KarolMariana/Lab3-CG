import numpy as np

#vertices = [[10,10], [20,10], [20,20], [10,20]]
#vertices = [[200, 50], [250, 100], [200, 150], [100, 150], [50, 100], [100, 50]]
# parece ser que los vertices van en sentido antihorario
n = 4

def dot(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2

def recorteCyrusBeck(P1, P2, n, vertices_viewport=None, EII=None, ESD=None):
    x1, y1 = P1
    x2, y2 = P2
    vertices = list()
    if (EII and ESD):
        x_min, y_min = EII
        x_max, y_max = ESD
        vertices = [[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]]
    else:
        vertices = vertices_viewport
    normal = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    for i in range(0, n):
        normal[i][1] = vertices[(i + 1) % n][0] - vertices[i][0]
        normal[i][0] = vertices[i][1] - vertices[(i + 1) % n][1]

    dx = x2 - x1
    dy = y2 - y1

    dp1e = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    for i in range(0, n):
        dp1e[i][0] = vertices[i][0] - x1
        dp1e[i][1] = vertices[i][1] - y1

    numerador = [0, 0, 0, 0, 0, 0]
    denominador = [0, 0, 0, 0, 0, 0]

    for i in range(0, n):
        numerador[i] = dot(normal[i][0], normal[i][1], dp1e[i][0], dp1e[i][1])
        denominador[i] = dot(normal[i][0], normal[i][1], dx, dy)

    t = [0, 0, 0, 0, 0, 0]
    tE = np.array([0])
    tL = np.array([1])

    for i in range(0, n):
        t[i] = float(numerador[i]) / float(denominador[i])
        if denominador[i] > 0:
            tE = np.append(tE, t[i])
        else:
            tL = np.append(tL, t[i])

    temp0 = np.amax(tE)
    temp1 = np.amin(tL)

    if temp0 > temp1:
        return

    nuevo_X1 = float(x1) + float(dx) * float(temp0)
    nuevo_Y1 = float(y1) + float(dy) * float(temp0)
    nuevo_X2 = float(x1) + float(dx) * float(temp1)
    nuevo_Y2 = float(y1) + float(dy) * float(temp1)
    puntos =  [[int(nuevo_X1), int(nuevo_Y1)], [int(nuevo_X2), int(nuevo_Y2)]]
    return puntos
    

if __name__ == '__main__':
    """ x1 = int(input("x1: "))
    y1 = int(input("y1: "))
    x2 = int(input("x2: "))
    y2 = int(input("y2: ")) """
    x1 = 9
    y1 = 60
    x2 = 20
    y2 = 90
    vertices = [[160, 50], [80, 80], [10, 80], [10, 50]]
    #vertices = [[5,5], [10,10], [16,10],  [20,2]]
    resultado = recorteCyrusBeck([x1,y1], [x2,y2], vertices_viewport=vertices)
    print("nuevos puntos: ", resultado)