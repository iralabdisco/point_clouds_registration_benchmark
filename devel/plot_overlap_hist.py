import numpy, matplotlib.pyplot

data = numpy.loadtxt("apartment_global.txt", skiprows=1, usecols=3) 
matplotlib.pyplot.hist(data, bins='auto', color='lightblue') 
matplotlib.pyplot.show()
