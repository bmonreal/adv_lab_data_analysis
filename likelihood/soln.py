import json
import numpy as np
import scipy.stats
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

with open("false_minimum_data.json") as f:
     data = json.load(f)
     exp_y_values = np.array(data["exp_y_values"])

x_values = np.arange(0,80,2)
y_err = np.sqrt(exp_y_values)

# define narrowpeak function with four adjustable parameters
def narrowpeak(x,x0,norm,wid,bg):
    return norm*np.exp(-((x-x0)/wid)**2) + bg

# define wrapper function in format needed by least_squares and including data
# first argument is a vector of parameter-values and is "natively" what least_squares
# expects its fun(x) to take
# 2nd and 3rd arguments are our way of passing in our dataset, but need to be explicitly
# force-fed through least_squares
def fun(x,xdata,ydata):
    x0 = x[0]
    norm = x[1]
    wid = x[2]
    bg = x[3]
    return ydata - narrowpeak(xdata,x0,norm,wid,bg) # the function returns an array of residuals

# here is an array of initial guesses to pass in
p0guesses = [61,11,4,11]

# notice that I have not fed in the error bars yet.  You know why?  Because I haven't quite figured out how.
# I think that x_scale=y_err is the correct way to do it, can someone test this and see what happens?
result = scipy.optimize.least_squares(fun, p0guesses,args=[x_values,exp_y_values])
print(result)
