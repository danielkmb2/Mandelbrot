from pylab import *
from numpy import *

RESOLUTION_DPI = .01
ITERATIONS = 200
ZOOM = 1024

CENTERX = 0.3
CENTERY = 0.025
WIDTH = 5
HEIGH = 5

def mandelbrot(a):
	z = 0
	for n in range(ITERATIONS): # para cada Zn de la sucesión...
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

	return ITERATIONS # esto podría ser NaN para ser mas exactos...

def computeMandelbrot():

	X = arange(
		(-(WIDTH / 2) / ZOOM) + CENTERX, 
		((WIDTH / 2) / ZOOM) + CENTERX, 
		RESOLUTION_DPI / ZOOM)
	Y = arange(
		(-(HEIGH / 2) / ZOOM) - CENTERY, 
		((HEIGH / 2) / ZOOM) - CENTERY, 
		RESOLUTION_DPI / ZOOM)


	Z = [0.+0.j] * (len(X) * len(Y))
	IT = [ITERATIONS] * len(Z)
	i = 0
	for x in range(0, len(X)):
		for y in range(0, len(Y)):
			Z[i] = X[y] + 1j * Y[x]
			i = i + 1

	import multiprocessing
	pool = multiprocessing.Pool()
	l = list(pool.map(mandelbrot, Z))
	return reshape(l, (len(Y), len(X)))


import time

start = time.time()
img = computeMandelbrot()
print(time.time() - start)

imshow(img)
#show()
savefig('mandelbrot_zoom%d_it%d.png' % (ZOOM,ITERATIONS))
