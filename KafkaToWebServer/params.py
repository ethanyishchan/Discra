import numpy as np


def printLinSpace(a):
	s = ""
	for i in a:
		s += str(i) + ','

	print s

#policy 1
# printLinSpace(np.linspace(-120,120,31))

# printLinSpace(np.linspace(3,7,3))

# printLinSpace(np.linspace(0,2 * np.pi, 19))

# printLinSpace(np.linspace(-60,60,31))

# printLinSpace(np.linspace(3,7,3))

# printLinSpace(np.linspace(0,2 * np.pi, 19))

# -5, -2.5, 0.0, 2.5, 5 deg bank
# //  >> Parameter    Value
# //  >> Xmin     -60 m
# //    >> Xmax    60 m
# //    >> Xdim    31
# //  >> Ymin     -60 m
# //    >> Ymax    60 m
# //    >> Ydim    31
# //  >> Vmin    3 m/s
# //    >> Vmax    7 m/s
# //    >> Vdim    3
# //  >> Bmin    0 rad
# //    >> Bmax    2pi rad
# //  >> Bdim    19
# //  >> Minsep    10 m
# //    >> Actions: -5, -2.5, 0.0, 2.5, 5 deg bank
deg_actions = [-5., -2.5, 0.0, 2.5, 5.0]
converted = [x / 180.0 * np.pi for x in deg_actions] 
print converted


# -5, -2.5, 0.0, 2.5, 5 deg bank
# //  >> Parameter    Value
# //  >> Xmin     -120 m
# //    >> Xmax    120 m
# //    >> Xdim    31
# //  >> Ymin     -60 m
# //    >> Ymax    60 m
# //    >> Ydim    31
# //  >> Vmin    3 m/s
# //    >> Vmax    7 m/s
# //    >> Vdim    3
# //  >> Bmin    0 rad
# //    >> Bmax    2pi rad
# //  >> Bdim    25
# //  >> Minsep    10 m
# //    >> Actions: -5, -2.5, 0.0, 2.5, 5 deg bank

printLinSpace(np.linspace(-120,120,31))

printLinSpace(np.linspace(3,7,3))

printLinSpace(np.linspace(0,2 * np.pi, 25))



