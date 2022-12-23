#Programa en Python para la implementacion del algoritmo Cohen Sutherland para recorte de línea.

# Definición de códigos de región
INSIDE = 0 # 0000
LEFT = 1 # 0001
RIGHT = 2 # 0010
BOTTOM = 4 # 0100
TOP = 8	 # 1000

# Definimos x_max, y_max y x_min, y_min para el rectangulo
# Dado que los puntos diagonales son suficientes para definir un rectángulo
""" xMax = 10.0
yMax = 8.0
xMin = 4.0
yMin = 4.0 """

# Función para calcular el código para un punto (x, y)
def calcularCodigo(x, y, x_min, y_min, x_max, y_max):
	code = INSIDE
	if x < x_min:	 #izquierda del rectángulo
		code |= LEFT
	elif x > x_max: #derecha del rectángulo
		code |= RIGHT
	if y < y_min:	 #debajo del rectángulo
		code |= BOTTOM
	elif y > y_max: #encima del rectángulo
		code |= TOP

	return code


# Implementación del algoritmo Cohen-Sutherland 
# para recortar una linea de un punto a otro, P1 = (x1, y1) a P2 = (x2, y2)
def recorteCohenSutherland(P1, P2, EII=None, ESD=None):
	x1, y1 = P1
	x2, y2 = P2
	x_min, y_min = EII
	x_max, y_max = ESD
	# Compute region codes for P1, P2
	code1 = calcularCodigo(x1, y1, x_min, y_min, x_max, y_max)
	code2 = calcularCodigo(x2, y2, x_min, y_min, x_max, y_max)
	accept = False

	while True:

		# Si ambos extremos se encuentran dentro del rectángulo
		if code1 == 0 and code2 == 0:
		    accept = True
		    break

		# Si ambos extremos están fuera del rectángulo
		elif (code1 and code2) != 0:
			break

		# Algún segmento se encuentra dentro del rectángulo.
		else:
            # Tendriamos 3 casos
			# Línea necesita recorte
            # Al menos uno de los puntos está afuera,
            # seleccionarlo
			x = 1.0
			y = 1.0
			if code1 != 0:
				code_out = code1
			else:
				code_out = code2

			# Encontrar el punto de intersección
			# para ello tenemos la formula de  y = y1 + slope * (x - x1),
			# x = x1 + (1 / slope) * (y - y1)
			if code_out & TOP:
				# punto está encima del rectángulo de recorte
				x = x1 + (x2 - x1) * \
								(y_max - y1) / (y2 - y1)
				y = y_max

			elif code_out and BOTTOM:	
				# el punto está debajo del rectángulo de recorte
				x = x1 + (x2 - x1) * \
								(y_min - y1) / (y2 - y1)
				y = y_min

			elif code_out and RIGHT:	
				# el punto está a la derecha del rectángulo de recorte
				y = y1 + (y2 - y1) * \
								(x_max - x1) / (x2 - x1)
				x = x_max

			elif code_out and LEFT:		
				# el punto está a la izquierda del rectángulo de recorte
				y = y1 + (y2 - y1) * \
								(x_min - x1) / (x2 - x1)
				x = x_min

			# Ahora encontraremos el punto de intersección x, y
            # Reemplazando el punto fuera del rectángulo de recorte por el punto de intersección
			if code_out == code1:
				x1 = x
				y1 = y
				code1 = calcularCodigo(x1, y1, x_min, y_min, x_max, y_max)

			else:
				x2 = x
				y2 = y
				code2 = calcularCodigo(x2, y2, x_min, y_min, x_max, y_max)

	if accept:
		return [[int(x1),int(y1)],[int(x2),int(y2)]]
	else:	
		return False

if __name__ == "__main__":
	# Guión del controlador
    # Segmento de primera línea
	# P11 = (5, 5), P12 = (7, 7)
	resultado = recorteCohenSutherland([5, 5],[ 7, 7])
	print("res: ", resultado)

	# Segmento de segunda línea
	# P21 = (7, 9), P22 = (11, 4)
	recorteCohenSutherland([7, 9], [11, 4])

	# Segmento de Tercera Línea
	# P31 = (1, 5), P32 = (4, 1)
	recorteCohenSutherland([1, 5], [4, 1])