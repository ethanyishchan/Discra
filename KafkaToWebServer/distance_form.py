


import numpy as np
from math import *
R = 6371000


def haversine2 (pt1, pt2):
	lat1,lon1 = pt1
	lat2,lon2 = pt2

	lat1 = lat1/180.0 * pi
	lat2 = lat2/180.0 * pi
	lon1 = lon1/180.0 * pi
	lon2 = lon2/180.0* pi
	x = (lon2-lon1) * cos((lat1+lat2)/2.0); 
	y = (lat2-lat1); 
	d = sqrt(x*x + y*y) * R;

	print "x,y: " , x * R, y * R
	print "d: ", d

def haversine(pt1, pt2):
	lat1,lon1 = pt1
	lat2,lon2 = pt2

	lat1 = lat1/180.0 * pi
	lat2 = lat2/180.0 * pi
	lon1 = lon1/180.0 * pi
	lon2 = lon2/180.0* pi

	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = (sin(dlat/2.0))**2.0 + cos(lat1) * cos(lat2) * (sin(dlon/2.0))**2 
	c = 2.0 * atan2( sqrt(a), sqrt(1.0-a) ) 
	d = R * c 

	print d

	print "x: ", d * cos(c)
	print "y: ", d * sin(c)
pt1 = (37.422570,-122.176514)
pt2 = (37.426896017,-122.173091007)

print "1"
haversine(pt1, pt2)
print "2"
haversine2(pt1, pt2)

print sqrt(302.269838545**2 + 481.031142978 ** 2)