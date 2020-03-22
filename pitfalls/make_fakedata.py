import numpy as np
def decaycurvewithbackground(t,n0,lifetime,background):
	return n0*np.exp(-t/lifetime) + background


# this is the fake data for zeros.py
n0=20
lifetime=3.7
background=0.2

timepoints = np.arange(0,20,0.5)
exact_data = decaycurvewithbackground(timepoints,n0,lifetime,background)
real_data = np.random.poisson(exact_data)

# this is the fake data for outliers.py


