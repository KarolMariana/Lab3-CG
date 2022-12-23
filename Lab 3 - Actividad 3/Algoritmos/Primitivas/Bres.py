def bresenham(x1, y1, x2, y2, dx, dy, decide):
    puntos = []
    pk = 2 * dy - dx
    for i in range(dx+1):
        puntos.append([x1, y1])
        x1 += 1 if x1<x2 else -1
        if pk < 0:  
            if decide == 0:
                pk = pk + 2 * dy
            else:
                pk = pk + 2 * dy
        else:
            y1 += 1 if y1<y2 else -1
            pk = pk + 2 * dy - 2 * dx

def main(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if (dx > dy):
        bresenham(x1, y1, x2, y2, dx, dy, 0)
    else: 
        bresenham(x1, y1, x2, y2, dy, dx, 1)

    if __name__ == '__main__':
        puntos = main(4,4,4,8)
        print("puntos bres: ", puntos)