from pylab import *
from numpy import *

def mandelbrot(a, iterations):
	z = 0
	for n in range(iterations): # para cada Zn de la sucesión...
		# se sabe que los puntos cuya distancia al origen es superior a 2, 
		# es decir, x^2 + y^2 >= 4 no pertenecen al conjunto. Por lo tanto
		# basta encontrar un solo término de la sucesión que verifique |zn| > 2 
		# para estar seguro de que c no está en el conjunto.
		if abs(z) > 2:
			# el valor de los puntos que no pertenecen al conjunto indican la 
			# velocidad con la que diverge (tiende al infinito, en módulo) la 
			# sucesión correspondiente a dicho punto
			return n

		z = z*z + a

	return iterations # esto podría ser NaN para ser mas exactos...

def computeMandelbrot(dpi, scale, w, h, cx, cy, iterations):

	X = arange((-(w / 2) / scale) + cx, ((w / 2) / scale) + cx, dpi / scale)
	Y = arange((-(h / 2) / scale) - cy, ((h / 2) / scale) - cy, dpi / scale)
	term_vector = [0.+0.j] * (len(X) * len(Y)) 	# inicializar el vector de términos

	i = 0
	for x in range(0, len(X)):
		for y in range(0, len(Y)):
			term_vector[i] = X[y] + 1j * Y[x]	# completar con el valor de cada término	
			i = i + 1

	iteration_vector = [iterations] * len(term_vector)

	import multiprocessing
	m_set_vector = []
	with multiprocessing.Pool() as pool:		# computar velocidad de escape del conjunto
		m_set_vector = list(pool.starmap(mandelbrot, zip(term_vector, iteration_vector)))

	return reshape(m_set_vector, (len(Y), len(X)))

ITERATIONS = 50
RESOLUTION_DPI = .01
CENTERX = -1.4
CENTERY = 0.0
WIDTH = 5
HEIGH = 5

def generageZoomSecuence():
	import time
	for _,ZOOM in enumerate([1,2,4,8,16,32,64,128,256,512,1024]):
		start = time.time()
		img = computeMandelbrot(RESOLUTION_DPI, ZOOM, WIDTH, HEIGH, CENTERX, CENTERY, ITERATIONS)
		imshow(img)
		axis('off')
		#show()
		savefig('examples/mandelbrot_zoom%d_it%d.png' % (ZOOM,ITERATIONS))

		print(time.time() - start)
		ITERATIONS = ITERATIONS + 20


img = computeMandelbrot(RESOLUTION_DPI, 1, WIDTH, HEIGH, CENTERX, CENTERY, 100)
imshow(img)
axis('off')
show()
