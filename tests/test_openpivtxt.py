#!/usr/bin/python

from vecpy import loadvec
from vecpy import vecPlot
from vecpy.vecClass import vec
import matplotlib.pyplot as plt


test_dir = "tests/data"
lst = loadvec.read_directory(test_dir)
data = loadvec.get_data_openpiv(lst[0],test_dir)
# dt = loadvec.get_dt(lst[0],test_dir)
dt = 1.0 # there is no dt in OpenPIV files
x,y,u,v,chc = loadvec.vecToMatrix(data)
vec = vec(x,y,u,v,chc,dt,lUnits='pix',tUnits = 'dt')


resolution = 1.0/71.96 #[mm/px]
# vec.rotate(0)
vec.scale(resolution)

plt.figure()
vecPlot.genQuiver(vec)
plt.show()

plt.figure()
vecPlot.genVorticityMap(vec)
plt.show()
