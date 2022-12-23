import PIL.ImageDraw as ID, PIL.Image as Image

# im mostrará los dos polígonos superpuestos
# im1 mostrará el camino recortado entre dos polígonos
im = Image.new("RGB", (500,500))
im1= Image.new("RGB", (500,500))
dibujar2=ID.Draw(im1)
dibujar = ID.Draw(im)
dibujar.polygon((162, 110, 388, 19, 386, 103, 162, 247), outline = 255, fill=(0,0,255)) #viewport para el recortado
dibujar2.polygon((162, 110, 388, 19, 386, 103, 162, 247), outline = 255, fill=(255,0,0)) # viewport inicial
dibujar.polygon((242, 78, 480, 77, 480, 289, 242, 289), outline = 'white') #poligono a recortar

# Una línea es un camino conectado entre dos puntos
# punto1(x1, y1) y punto2(x2, y2)
def dibujar1(x1, y1, x2, y2):
    dibujar2.line((x1,y1,x2,y2),fill=(0,255,0))

# cada vértice tiene dos dimensiones (x e y)
# Inicialización de vértice o línea
class VerticeBase:
    def init(self, x, y):
        self.x = x
        self.y = y

class Vertice(VerticeBase):
    def init(self, x, y, next = None):
        super(Vertice, self).init(x, y)
        self.next = next

# inicialización del vértice de intersección
class Interseccion(VerticeBase):
    def init(self, x, y, nextS = None, nextC = None, crossDi = -1):
        super(Interseccion, self).init(x, y)
        self.nextS = nextS
        self.nextC = nextC
        self.crossDi = crossDi
        self.used = False

# Manejo de los valores flotantes
def valoresFlotantes(f1, f2):
    prec = 1e-5
    if abs(f1 - f2) < prec:
        return True
    else:
        return False

# Manejo de los valores flotantes grandes
def flotantesGrandes(f1, f2):
    if valoresFlotantes(f1, f2):
        return False
    elif f1 > f2:
        return True
    else:
        return False

# comprobando si el polígono de vértice o no
def esPoligonoVertice(v, list):
    judgeIndex = 0
    for i in range(len(list)):
        j = i + 1
        minY = min(list[i % len(list)].y, list[j % len(list)].y)
        maxY = max(list[i % len(list)].y, list[j % len(list)].y)
        if flotantesGrandes(v.y, maxY) or flotantesGrandes(minY, v.y):
            continue
        if valoresFlotantes(maxY, minY):
            if flotantesGrandes(v.x, max(list[i % len(list)].x, list[j % len(list)].x)):
                judgeIndex += 1
                continue
            elif flotantesGrandes(min(list[i % len(list)].x, list[j % len(list)].x), v.x):
                continue
            else:
                return True
        x = (list[i % len(list)].x - list[j % len(list)].x) / (list[i % len(list)].y - list[j % len(list)].y) * (v.y - list[i % len(list)].y) + list[i % len(list)].x
        if(valoresFlotantes(v.x, x)):
            return None
        if flotantesGrandes(v.x, x):
            judgeIndex += 1
    if judgeIndex % 2 != 0:
        return True
    return False

def getX(v):
    return v.x
def getY(v):
    return v.y

def LineCrossH(y, c1, c2):
    return c1.x + (c2.x - c1.x) * (y - c1.y) / (c2.y - c1.y)
def LineCrossV(x, c1, c2):
    return c1.y + (c2.y - c1.y) * (x - c1.x) / (c2.x - c1.x)

def cortarLineaVertical(s1, s2, list):
    assert valoresFlotantes(s1.x, s2.x)
    crossXs = []
    x = s1.x

    shearedList = [Vertice(r.x, r.y) for r in list]

    minY = min(s1.y, s2.y)
    maxY = max(s1.y, s2.y)

    for i in range(len(list)):
        vertex = list[i]
        c1 = shearedList[i % len(list)]
        c2 = shearedList[(i + 1) % len(list)]

        if(valoresFlotantes(c1.x, c2.x) and valoresFlotantes(c1.x, x)):
            continue
        if(flotantesGrandes(c1.x, x) and flotantesGrandes(c2.x, x)):
            continue
        if(flotantesGrandes(x, c1.x) and flotantesGrandes(x, c2.x)):
            continue

        y = float('%.9f' % LineCrossV(x, c1, c2))

        inters = Interseccion(x, y)

        next = None
        if((flotantesGrandes(y, minY) and flotantesGrandes(maxY, y))
         or (c2.y == y and x == s2.x)
         or (c1.y == y and x == s1.x)
            or (valoresFlotantes(c2.x, x) and valoresFlotantes(y, s1.y))
            or (valoresFlotantes(c1.x, x) and valoresFlotantes(y, s2.y))
            or (valoresFlotantes(y, minY) and (not valoresFlotantes(c1.x, x)) and (not valoresFlotantes(c2.x, x)))
            or (valoresFlotantes(y, maxY) and (not valoresFlotantes(c1.x, x)) and (not valoresFlotantes(c2.x, x)))):
            while not ((isinstance(vertex, Vertice) and isinstance(vertex.next, Vertice)) or (isinstance(vertex, Interseccion) and isinstance(vertex.nextS, Vertice))):
                if isinstance(vertex, Vertice):
                    assert isinstance(vertex.next, Interseccion)
                    if (flotantesGrandes(c2.x, c1.x) and flotantesGrandes(vertex.next.x, inters.x)) or (flotantesGrandes(c1.x, c2.x) and flotantesGrandes(inters.x, vertex.next.x)):
                        break
                    vertex = vertex.next
                else:
                    assert isinstance(vertex.nextS, Interseccion)
                    if (flotantesGrandes(c2.x, c1.x) and flotantesGrandes(vertex.nextS.x, inters.x)) or (flotantesGrandes(c1.x, c2.x) and flotantesGrandes(inters.x, vertex.nextS.x)):
                        break
                    vertex = vertex.nextS
            if isinstance(vertex, Vertice):
                next = vertex.next
            else:
                next = vertex.nextS
            if isinstance(vertex, Vertice):
                vertex.next = inters
            else:
                assert isinstance(vertex, Interseccion)
                vertex.nextS = inters
            inters.nextS = next
            if valoresFlotantes(c1.x, x):
                assert not valoresFlotantes(c2.x, x)
                if flotantesGrandes(c2.x, x):
                    inters.crossDi = 0
                else:
                    inters.crossDi = 1
            elif flotantesGrandes(c1.x, x):
                inters.crossDi = 1
            else:
                inters.crossDi = 0
            if flotantesGrandes(s2.y, s1.y):
                inters.crossDi = 0 if inters.crossDi == 1 else 1

            crossXs.append(inters)
    return crossXs

def cortarLinea(s1, s2, list):
 
    if valoresFlotantes(s1.x, s2.x):
        return cortarLineaVertical(s1, s2, list)
    crossXs = []

    slope = (s2.y - s1.y) / (s1.x - s2.x)
    y = s1.x * slope + s1.y
    shearedList = [Vertice(r.x, r.x * slope + r.y) for r in list]

    minX = min(s1.x, s2.x)
    maxX = max(s1.x, s2.x)

    for i in range(len(list)):
        vertex = list[i]
        c1 = shearedList[i % len(list)]
        c2 = shearedList[(i + 1) % len(list)]   

        if(valoresFlotantes(c1.y, c2.y) and valoresFlotantes(c1.y, y)):
            continue
        if(flotantesGrandes(c1.y, y) and flotantesGrandes(c2.y, y)):
            continue
        if(flotantesGrandes(y, c1.y) and flotantesGrandes(y, c2.y)):
            continue

        x = float('%.9f' % LineCrossH(y, c1, c2))
        npy = y - x * slope
        inters = Interseccion(x, npy)

        next = None
        if((flotantesGrandes(x, minX) and flotantesGrandes(maxX, x))
        or (c2.y == y and x == s2.x)
        or (c1.y == y and x == s1.x)
        or (valoresFlotantes(c2.y, y) and valoresFlotantes(x, s1.x))
        or (valoresFlotantes(c1.y, y) and valoresFlotantes(x, s2.x))
        or (valoresFlotantes(x, minX) and (not valoresFlotantes(c1.y, y)) and (not valoresFlotantes(c2.y, y)))
        or (valoresFlotantes(x, maxX) and (not valoresFlotantes(c1.y, y)) and (not valoresFlotantes(c2.y, y)))):
            while not ((isinstance(vertex, Vertice) and isinstance(vertex.next, Vertice)) or (isinstance(vertex, Interseccion) and isinstance(vertex.nextS, Vertice))):
                if isinstance(vertex, Vertice):
                    assert isinstance(vertex.next, Interseccion)
                    if (flotantesGrandes(c2.x, c1.x) and flotantesGrandes(vertex.next.x, inters.x)) \
                            or (flotantesGrandes(c1.x, c2.x) and flotantesGrandes(inters.x, vertex.next.x))\
                            or (flotantesGrandes(c1.y - c1.x * slope, c2.y - c2.x * slope) and flotantesGrandes(inters.y, vertex.next.y))\
                            or (flotantesGrandes(c2.y - c2.x * slope, c1.y - c1.x * slope)  and flotantesGrandes(vertex.next.y, inters.y)):
                        break
                    vertex = vertex.next
                else:
                    assert isinstance(vertex.nextS, Interseccion)
                    if (flotantesGrandes(c2.x, c1.x) and flotantesGrandes(vertex.nextS.x, inters.x))\
                            or (flotantesGrandes(c1.x, c2.x) and flotantesGrandes(inters.x, vertex.nextS.x))\
                            or (flotantesGrandes(c2.y - c2.x * slope, c1.y - c1.x * slope) and flotantesGrandes(inters.y, vertex.nextS.y))\
                            or (flotantesGrandes(c2.y - c2.x * slope, c1.y - c1.x * slope) and flotantesGrandes(vertex.nextS.y, inters.y)):
                        break
                    vertex = vertex.nextS
            if isinstance(vertex, Vertice):
                next = vertex.next
            else:
                next = vertex.nextS
            if isinstance(vertex, Vertice):
                vertex.next = inters
            else:
                assert isinstance(vertex, Interseccion)
                vertex.nextS = inters
            inters.nextS = next
            if valoresFlotantes(c1.y, y):
                assert not valoresFlotantes(c2.y, y)
                if flotantesGrandes(y, c2.y):
                    inters.crossDi = 0
                else:
                    inters.crossDi = 1
            elif flotantesGrandes(y, c1.y):
                inters.crossDi = 1
            else:
                inters.crossDi = 0

            if flotantesGrandes(s2.x, s1.x):
                inters.crossDi = 0 if inters.crossDi == 1 else 1
   
            crossXs.append(inters)

    return crossXs

def processNoCross(listS, listC):
    sInC = esPoligonoVertice(listS[0], listC)
    if sInC:
        return listS
    cInS = esPoligonoVertice(listC[0], listS)
    if cInS:
        return listC
    return []

def imprimirLista(start, isS):
    assert isinstance(start, Vertice)
    next = start.next
    print("------------------------------------------------------------------")
    if isS:
        print("Lista de forma de polígono1: ")
        print(str(start.x) + "," + str(start.y))
        while next != start:
            print(str(next.x) + "," + str(next.y))
            if isinstance(next, Vertice):
                next = next.next
            else:
                assert isinstance(next, Interseccion)
                print(next.crossDi)
                next = next.nextS
    else:
        print("Lista de forma de polígono1: ")
        print(str(start.x) + "," + str(start.y))
        while next != start:
            print(str(next.x) + "," + str(
                next.y))
            if isinstance(next, Vertice):
                next = next.next
            else:
                assert isinstance(next, Interseccion)
                print(next.crossDi)
                next = next.nextC
    print("------------------------------------------------------------------")

def Compose(list):
    result = []
    for inters in list:
        assert isinstance(inters, Interseccion)
        if(not inters.used) and inters.crossDi == 0:
            oneResult = []
            oneResult.append(Vertice(inters.x, inters.y))
            inters.used = True
            loopvar = inters.nextS

            while loopvar != None:
                oneResult.append(Vertice(loopvar.x, loopvar.y))
                if isinstance(loopvar, Interseccion):
                    curr = loopvar
                    curr.used = True
                    next = curr.nextS if curr.crossDi == 0 else curr.nextC
                elif isinstance(loopvar, Vertice):
                    curr = loopvar
                    next = curr.next
                if next is inters:
                    break
                loopvar = next
            result.append(oneResult)
    for vertexs in result:
        for i in range(len(vertexs)):
            if i >= len(vertexs):
                break
            u = vertexs[i % len(vertexs)]
            v = vertexs[(i + 1) % len(vertexs)]
            if(valoresFlotantes(u.x, v.x) and valoresFlotantes(u.y, v.y)):
                vertexs.pop(i)
            i -= 1
    return result

def decode(lists):
    results = []
    for list in lists:
        result = ""
        for v in list:
            result += "%f %f " % (v.x, v.y)
        result = result.strip()
        results.append(result)
    return results

def encode(Str):
    myList = []
    list_float = list(map(float, Str.strip().split()))
    X = list_float[0::2]
    Y = list_float[1::2]
    assert len(X) == len(Y)
    for i in range(len(X)):
        if (not valoresFlotantes(X[i], X[i - 1])) or (not valoresFlotantes(Y[i], Y[i - 1])):
            myList.append(Vertice(X[i], Y[i]))
    return myList


def transDirect(list):
    newList = []
    for i in range(len(list)):
        newList.append(list[len(list) - 1 - i])
    return newList

def toClockwise(list):
    maxX = -1
    mark_i = -1

    for i in range(len(list)):
        if list[i].x > maxX:
            maxX = list[i].x
            mark_i = i
    v1 = Vertice(list[mark_i].x - list[mark_i - 1].x, list[mark_i].y - list[mark_i - 1].y)
    v2 = Vertice(list[(mark_i + 1) % len(list)].x - list[mark_i].x, list[(mark_i + 1) % len(list)].y - list[mark_i].y)
    crossPr = v1.x * v2.y - v2.x * v1.y
    while valoresFlotantes(crossPr, 0):
        mark_i += 1
        v2 = Vertice(list[(mark_i + 1) % len(list)].x - list[mark_i % len(list)].x,
                    list[(mark_i + 1) % len(list)].y - list[mark_i % len(list)].y)
        crossPr = v1.x * v2.y - v2.x * v1.y
    assert not valoresFlotantes(crossPr, 0)
    if crossPr < 0:
        return transDirect(list)
    else:
        return list

def recorteWeilerAtherton(poly1, poly2, output_clockwise = True):

    listS = encode(poly1)
    listC = encode(poly2)
    listS = toClockwise(listS)
    listC = toClockwise(listC)
    listI = []

    for i in range(len(listS)):
        listS[i - 1].next = listS[i]
    for i in range(len(listC)):
        listC[i - 1].next = listC[i]

    for cutStartIdx in range(len(listC)):
        s1 = listC[cutStartIdx]
        s2 = listC[(cutStartIdx + 1) % len(listC)]

        inters = cortarLinea(s1, s2, listS)
        if len(inters) == 0:
            continue

        if valoresFlotantes(s1.x, s2.x):
            assert not valoresFlotantes(s1.y, s2.y)
            if flotantesGrandes(s2.y, s1.y):
                inters.sort(key=getY)
            else:
                inters.sort(key=getY, reverse=True)
        elif flotantesGrandes(s2.x, s1.x):
            inters.sort(key=getX)
        else:
            inters.sort(key=getX, reverse=True)

        for v in inters:
            listI.append(v)

        s1.next = inters[0]
        for i in range(len(inters) - 1):
            inters[i].nextC = inters[i + 1]
        inters[len(inters) - 1].nextC = s2


    if len(listI) == 0:
        return decode([processNoCross(listS, listC)])

    results = Compose(listI)
    if not output_clockwise:
        results_ = []
        for result in results:
            result = transDirect(result)
            results_.append(result)
        results = results_
    return  decode(results)

if __name__ == 'main':
    poly1 = "240 76 480 75 480 287 240 287" #poligono a recortar
    poly2 = "160 108 386 19 384 102 160 245" #viewport
    point = recorteWeilerAtherton(poly1, poly2)
    points = point[0].split(' ')
    """ print("puntos: ", list(map(lambda x: int(float(x)), points)))
    print(points[0]) """
    """ i = 0
    while i < 8:
        if i == 6:
            draw1(float(points[i]),float(points[i+1]),float(points[0]),float(points[1]))
        else:
            draw1(float(points[i]),float(points[i+1]),float(points[i+2]),float(points[i+3]))
        i = i + 2

    im.show()
    im1.show() """