import numpy as np
wavelength = 626.34
constant = np.array([(3050+0.6*np.cos(np.pi*i/40.0))*(1/wavelength) for i in range(30)])

exactdata = constant*wavelength
realdata = np.random.normal(exactdata,0.1/constant)
errorbar = 0.1/constant
runnumber = np.array(range(30))
