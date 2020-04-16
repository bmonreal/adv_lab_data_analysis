import json
import numpy as np
import scipy.stats
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
with open("false_minimum_data.json") as f:
     data = json.load(f)
     exp_y_values = np.array(data["exp_y_values"])

def narrowpeak(x,x0,norm,wid,bg):
    return norm*np.exp(-((x-x0)/wid)**2) + bg

