'''
False Minima

Sometimes you will try to run a curve fit and get an obviously-garbage result.  If it isn't some other bug in your code, it could be that the fitter is stuck in a False Minimum.  This code will run a fit that gets stuck in such a minimum and another that gets out.
'''

import numpy as np
from matplotlib import pyplot as plt
import scipy.stats
from scipy.optimize import curve_fit

plt.ion()
plt.clf()


f, (ax1,ax2,ax3) = plt.subplots(3,1,figsize=(8,8))
ax1.set_title("Fits in and out of a false minimum")

'''
The particular function we will try out is a narraw Gaussian on top of a background.   We're going to fix the widths but float the centroid and norm.
'''

def narrowpeak(x,x0,norm):
    return norm*np.exp(-((x-x0)/3.0)**2) + 10

'''
Here we generate the fake data; I am going to fix the random seed because I want this to behave the way I'm talking about, which might not happen in every instance.  In fact I'm not sure I can guarantee that this code will produce the same output in a different version of Python since it depends on hidden implementation details.  This works the way I say it does in scipy 1.4.1 and numpy 1.15.4.
'''

true_norm = 20
true_x0 = 60
params = [true_x0,true_norm]

x_values = np.arange(0,80,2)
exact_y_values = np.array([narrowpeak(x,*params) for x in x_values])
# if you want to try this again with fresh fluctuations, switch this test to False.
# I cannot guarantee that all the interesting crashes and failures and whatnot will occur.
# The JSON file contains the data and fit-pathologies I am discussing below.  However, 
# I am not sure if it is robust to small changes in code version.  All I will say is it
# "worked" in Python 3.7.1, numpy 1.15.4, scipy 1.4.1   
if True:
    import json
    with open("false_minimum_data.txt") as f:        
        data = json.load(f)
        exp_y_values = np.array(data["exp_y_values"])
else: # in particular, the line below would reproduce the saved data if you preceded it with np.random.set_seed(123456).  Remember to re-randomize it afterwards with set_seed() and no argument, or it may confuse you later in the session.
    exp_y_values = np.array([np.random.poisson(y) for y in exact_y_values])
    
y_err = np.sqrt(exp_y_values)

ax1.errorbar(x_values,exp_y_values,yerr=y_err,marker="o",linestyle=" ",label="data")

popt, pcov = curve_fit(narrowpeak, x_values, exp_y_values,sigma=y_err,absolute_sigma=True)
best_fit = np.array([narrowpeak(x,*popt) for x in x_values])
ax1.plot(x_values,best_fit,label="best_fit")

uncertainties = [np.sqrt(pcov[i][i]) for i in range(len(pcov))]
for i,pname in enumerate(["x0","norm"]):
    print("%d %s = %f +/- %f"%(i,pname,popt[i],uncertainties[i]))

chi2 = np.sum(((exp_y_values - best_fit)/y_err)**2)
ndof = len(x_values) - 4 # four degrees of freedom used up by four-paramter fit
prob=print("chi2=%f, ndof=%f, chi2/ndof=%f, prob=%f"%(chi2,ndof,chi2/ndof,scipy.stats.chi2.cdf(chi2,ndof)))
ax1.set_xlim(0,80)

ax1.legend()

''' 
Diagnosis: it's a disaster.  The fitter decided that the "gaussian" should be a negative-valued DIP that's a close match to a small downward fluctuation near x=5.  How did it get THAT??  It is sometimes useful to see what a fitter is actually trying.  Let's try just once to run a fit function with an internal logger.   Unfortunately Python logging (as best I can undersrequires a bunch of faff so here we just use a print statement.  
'''


def verbose_narrowpeak(x,x0,norm):
    # it SO HAPPENS that scipy will vector-evaluate this so the function is only
    # called once per loop.  If you want to do this in a situation where that's
    # not true, do something like "if x==0: print()" so the print statement
    # only goes off once per curve-fit-attempt.
    #
    # Note: It'd be nice to replace these print statements with a real logging stream
    # and do some visualization of where the fitter goes.
    print("trying %06.10f %06.10f"%(x0,norm))
    return norm*np.exp(-((x-x0)/3.0)**2) + 10

popt, pcov = curve_fit(verbose_narrowpeak, x_values, exp_y_values,sigma=y_err,absolute_sigma=True)

'''
What you will see in the output is extremely simple.  The fitter started with x0=0 and tested the goodness of fit.  It tried fluctuating x0 up a tiny bit.  It tried fluctuating norm up a tiny bit.  It then took a few (random) big jumps in both parameters and fluctuated a tiny bit around each one.  What it's going is asking if it sees a direction in which chi^2 is decreasing.  A few jumps later it has tried values near x0=2.7826258008 and near x0=6.6773004680 and concluded it can improve chi2 by going between those two values; its search is remarkably fast after that.  Notice that it evaluates the "best fit" value once and only once; it has already circled the minimum, sort of, in both parameters.  It never got anywhere near trying x0=60, as it so happens, so it never saw even a hint of the chi2 improvement that would result there.
'''

'''
Let's do a parameter scan and see what the "false minimum" can look like.  We will try each value of x0 and fit for the remaining parameter "norm".
This particular (lambda-based)) parameter scan trick is documented in fit_and_parameter_scan.py.
'''

mean_scan_values = np.arange(0,80,0.1)
mean_scan_results = [0]*len(mean_scan_values)
for itrial,fix_mean in enumerate(mean_scan_values):
    tmppopt, tmppcov = curve_fit(lambda x, norm: narrowpeak(x,fix_mean,norm), x_values, exp_y_values,sigma=y_err,absolute_sigma=True)
    
    tmpbest_fit = np.array([narrowpeak(x,fix_mean,tmppopt[0]) for x in x_values])
    tmpchi2 = np.sum(((exp_y_values - tmpbest_fit)/y_err)**2)
    mean_scan_results[itrial] = tmpchi2
    
ax2.plot(mean_scan_values,mean_scan_results,label="chi2 scan of means")
ax2.scatter([popt[0]],[chi2])
ax2.annotate("best fit from 1st plot is x0=%f chi2=%f"%(popt[0],chi2),(popt[0],chi2),(0,-50),textcoords="offset points",arrowprops={"arrowstyle":'->'})
ax2.set_xlim(0,80)
ax2.set_ylabel("chi2")
ax2.set_xlabel("fixed x0")
ax2.legend()


'''
In that plot you can see the problem: the value of chi^2 DOES have a minimum near x=5.   The fitter got into it and had no way of knowing that x0 near 60 would give it an even better minimum.  This is a case where the fitter needed the INITIAL GUESSES to be ok.  In fact, scipy.curve_fit has by default "initial guess for every parameter is 1.0". Let's do another scan, not scanning fixed-x0 values, but scanning x0 guesses.

'''


mean_scan_values = np.arange(0,80,1)
mean_scan_x0out = [0]*len(mean_scan_values)

for itrial,fix_mean in enumerate(mean_scan_values):
    try:
        popt, pcov = curve_fit(narrowpeak, x_values, exp_y_values,sigma=y_err,absolute_sigma=True,p0 = [fix_mean,1.0])
        best_fit = np.array([narrowpeak(x,fix_mean,popt[0]) for x in x_values])
        chi2 = np.sum(((exp_y_values - best_fit)/y_err)**2)
        mean_scan_x0out[itrial] = popt[0]
    except RuntimeError:
        print("failed to converge when guess=",fix_mean)
        mean_scan_x0out[itrial] = -1.0

legendhack = True 
for fitx0,scanx0 in zip(mean_scan_x0out,mean_scan_values):
    if fitx0==-1.0:
        ax3.plot([0,80],[scanx0,scanx0],color='red') # draw red lines at failed convergences
        if legendhack:
            ax3.plot([0,80],[scanx0,scanx0],color='red',label="failed convergence") # this is a humiliatingly hacky way to get ONLY ONE red line into the legend
            legendhack = False
        
ax3.plot(mean_scan_x0out,mean_scan_values,label="x0 fit results from various starting guesses",linestyle=":",marker='.')
ax3.annotate("wide range of guesses lead here",(true_x0,true_x0),(-200,0),textcoords="offset points",arrowprops={"arrowstyle":'->'})
ax3.set_xlim(0,80)
ax3.set_ylabel("starting guess")
ax3.set_xlabel("best fit x0 given guess")
ax3.legend()
''' 
You will see that MANY initial guess values end up trapped in weird false minima; some fits (with guesses well above the good region) failed to converge entirely.  I used a try/except block to let the code exit normally. 

NOTE: It is possible that the value that causes this event is specific to my exact version of scipy, etc..  If the choices below don't throw a runtime error for you, choose values that do (or ignore this block.) 
'''

try:
    popt, pcov = curve_fit(verbose_narrowpeak, x_values, exp_y_values,sigma=y_err,absolute_sigma=True,p0=[78,1.0])
except RuntimeError as inst:
    print("the fitter has thrown a runtime exception.  We have caught it to avoid a crash. Here is the error:")
    print(type(inst))
    print(inst.args)
    print(inst)
'''
In this case, the fitter's first wild guess is that the peak is off to the left and low-amplitude.  Its second wild guess is at 67 and higher-amplitude.  The latter must have been slightly worse, because it goes back to trying high x0 values.  Unfortunately, the VERY LAST data point fluctuates up.  The fitter learns quickly that it can reduce chi2---probably solely in the sense of getting the curve a tiny bit closer to this one point---by putting what would probably turn out to be an arbitrarily-tall peak arbitrarily-far to the right.  Since there is no "minimum" it will find to tell it to stop, it just keeps adjusting until it runs out of tries.  

Computers are dumb sometimes.  ALWAYS look at your failed fits, because you are smarter than the fitter.  Don't just crank up the "maximum number of calls", or lower the tolerances, or throw up your hands and say "it didn't work for some reason".  There are ways to diagnose a failed fit.  In this case, eyeball-examination of the data and choosing x0 "fairly near 60" will lead to the fitter finding the true minimum.
''' 

