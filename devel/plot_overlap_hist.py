import numpy, matplotlib.pyplot, sys

data = numpy.loadtxt(sys.argv[1], skiprows=1, usecols=3) 
matplotlib.pyplot.hist(data, bins='auto', color='lightblue') 
matplotlib.pyplot.show()
