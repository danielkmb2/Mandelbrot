from pylab import *
from numpy import *

RESOLUTION_DPI = .01
ITERATIONS = 100
ZOOM = 2

CENTERX = -1.4
CENTERY = 0
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

def computeMandelbrot(res, z, w, h, cx, cy, its):

	X = arange(
		(-(w / 2) / z) + cx, 
		((w / 2) / z) + cx, 
		res / z)
	Y = arange(
		(-(h / 2) / z) - cy, 
		((h / 2) / z) - cy, 
		res / z)


	Z = [0.+0.j] * (len(X) * len(Y))
	IT = [its] * len(Z)
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

ITERATIONS = 40
for _,ZOOM in enumerate([1,2,4,8,16,32,64,128,256,512,1024]):
	start = time.time()
	img = computeMandelbrot(RESOLUTION_DPI, ZOOM, WIDTH, HEIGH, CENTERX, CENTERY, ITERATIONS)
	imshow(img)
	axis('off')
	#show()

	savefig('examples/mandelbrot_zoom%d_it%d.png' % (ZOOM,ITERATIONS))
	print(time.time() - start)
	ITERATIONS = ITERATIONS + 20
