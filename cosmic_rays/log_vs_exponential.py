'''
Example code showing different options for fits to exponential data
'''


import numpy as np
from matplotlib import pyplot as plt
import scipy.stats
from scipy.optimize import curve_fit

plt.ion()
plt.clf()



'''
Our standard curve-fitting tools always require you to write a function
containing your model.  In scipy.optimize.curve_fit, the function 
specifically takes the x-value as its first argument, and however many
free parameters as the 2nd-thru-nth arguments.

In this snippet, we will compare the two common approaches (a) "take 
the log of the data and fit a line" vs (b) "actually fit an 
exponential function to the data".

In this case I am specifying a function of the form 10^x rather than 
e^x and will do everything in log-10.   The parameter called "wid" 
in the exponential model is the same as the parameter called "a" in 
the linear model.

'''

def exp_model(x,norm,slope):
    return norm*np.power(10,x*slope)  

def linear_model(x,lognorm,slope):
    return x*slope + lognorm

'''
Let's suppose that the following theory were true, and its truth led 
to the existence of some data.  For the sake of writing a little 
tutorial here, I will *generate* fake data in this code snippet, 
but if you had done a real experiment the data would have been 
laboriously obtained from an experimental apparatus.
 
The (true) theory is given in "exact_y_values".
The (fake) data is "exp_y_values".  
'''

true_norm = 1000
true_slope = -0.025
x_values =  np.array([i for i in np.arange(0,40,2)])
exact_y_values = np.array([exp_model(x,true_norm,true_slope) for x in x_values])

'''
Tricky little block:
If this is False, we will look at "fresh" fake data every time 
we run the code.  Do this if you want to see the full scope of possible
behaviors of the code.
If this is True, there is an immutable fixed dataset which you 
can look at over and over.  Do this if you want to debug the code while
looking a particular (if randomly-chosen) realization of the data.
'''
if False:
    np.random.seed(123456789) 

'''
To illustrate the point I'm trying to make, I will choose an error bar
that's constant over the range of the data.  Imagine you have a 
voltmeter with 100-mV noise which is present whether you are measuring
10^4 mV or 100 mV.  The fractional error is larger on the smaller
voltages.  

(This will fail sometimes because the noise will make the "data" 
negative, and you can't take the log of a negative number.  If it 
fails, run it again ... or think about what to modify to handle that 
situation.)   
'''

y_err = np.array([100.0 for x in x_values])   
exp_y_values = np.random.normal(exact_y_values,y_err)

if any([x <= 0 for x in exp_y_values]):
    raise ValueError("This run happened to have some negative data.  
It's not going to behave well when we take logs.  Instead of writing 
code to clean it up (that's your job) I have opted to exit.  Run again
and it'll probably work.") 

f, (ax1,ax2,ax3,ax4) = plt.subplots(4,1,figsize=(8,8))
ax1.set_title("Exponential data")

'''
EXAMPLE 1: Take logs of data and fit a straight line, IGNORING THE 
ERROR BARS.  This is th "default" approach you will see in many 
student writeups involving exponential data.  I want to emphasize 
that it's not a great idea.  This fit will work, BUT ... 
'''
logdata = np.log10(exp_y_values)   
logtruth = np.log10(exact_y_values)

'''
First, how do you even put an error bar on the log10 of a value?  In 
the limit of small errror bars, this is how, and it's about as good 
as you can do in practice.  When the error bars are a large fraction 
of the data value, you properly speaking would need *asymmetric* error
bars, and that's a whole other thing.  (See the README.md for why.)
'''
logerrorbars = (y_err/exp_y_values)/np.log(10)

'''
But we're not going to tell scipy.curve_fit about those error bars.  
We'll use the defaults.
'''

popt, pcov = curve_fit(linear_model, x_values, logdata)

uncertainties = [np.sqrt(pcov[i][i]) for i in range(len(pcov))]

for i,pname in enumerate(["lognorm","slope"]):
    print("%d %s = %f +/- %f"%(i,pname,popt[i],uncertainties[i]))
ex1slope = popt[1]
ex1err = uncertainties[1]

best_fit = np.array([linear_model(x,*popt) for x in x_values])

ndof = len(x_values) - 2
chi2 = sum(((best_fit - logdata)/logerrorbars)**2)
pchi2 = scipy.stats.chi2.cdf(chi2,ndof)

'''
What you will probably see is that the fit has converged, and the 
chi2 is *absurdly* small, yielding a P(chi2) that's "too good to be 
true" and unlikely to have arisen from real fluctuations.
'''

ax1.errorbar(x_values,logdata,yerr=logerrorbars,marker="*",
                 linestyle=" ",label="data")
ax1.plot(x_values,logtruth,label="truth",linestyle=":")
ax1.plot(x_values,best_fit,label="best_fit")
ax1.text(0.3,0.9,"Example 1: straight-line fit ignoring errors",
             transform=ax1.transAxes)
ax1.text(0.3,0.1,"chi2=%f, P=%f"%(chi2,pchi2),transform=ax1.transAxes)
ax1.legend()


'''
EXAMPLE 2: Same as above, but this time we tell the fitter to use the 
(logged) error bars.

'''

popt, pcov = curve_fit(linear_model, x_values, logdata,
                           sigma=logerrorbars,absolute_sigma=True)
uncertainties = [np.sqrt(pcov[i][i]) for i in range(len(pcov))]

ex2slope = popt[1]
ex2err = uncertainties[1]


for i,pname in enumerate(["lognorm","slope"]):
    print("%d %s = %f +/- %f"%(i,pname,popt[i],uncertainties[i]))

best_fit = np.array([linear_model(x,*popt) for x in x_values])

chi2 = sum(((best_fit - logdata)/logerrorbars)**2)
pchi2 = scipy.stats.chi2.cdf(chi2,ndof)

ax2.errorbar(x_values,logdata,yerr=logerrorbars,marker="*",
                 linestyle=" ",label="data")
ax2.plot(x_values,logtruth,label="truth",linestyle=":")
ax2.plot(x_values,best_fit,label="best_fit")
ax2.text(0.3,0.9,"Example 1: straight-line fit using errors",
             transform=ax2.transAxes)

ax2.text(0.3,0.1,"chi2=%f, P=%f"%(chi2,pchi2),
             transform=ax2.transAxes)

ax2.legend()


'''
EXAMPLE 3: Fit an exponential curve using the real model

We're not going to take any logs, we're going to fit the real model 
to the real data (data and noise in mV or whatever), and use a real 
log axis to plot it.
'''


popt, pcov = curve_fit(exp_model, x_values, exp_y_values,p0=[1e4,0.05],sigma=y_err,absolute_sigma=True)

uncertainties = [np.sqrt(pcov[i][i]) for i in range(len(pcov))]
ex3slope = popt[1]
ex3err = uncertainties[1]

for i,pname in enumerate(["norm","slope"]):
    print("%d %s = %f +/- %f"%(i,pname,popt[i],uncertainties[i]))

best_fit = np.array([exp_model(x,*popt) for x in x_values])

chi2 = sum(((best_fit - exp_y_values)/y_err)**2)
pchi2 = scipy.stats.chi2.cdf(chi2,ndof)

ax3.errorbar(x_values,exp_y_values,yerr=y_err,marker="*",linestyle=" ",label="data")
ax3.plot(x_values,exact_y_values,label="truth",linestyle=":")

ax3.plot(x_values,best_fit,label="best_fit")
ax3.set_yscale('log')
ax3.text(0.3,0.9,"Example 3: exponential fit",transform=ax3.transAxes)

ax3.text(0.3,0.1,"chi2=%f, P=%f"%(chi2,pchi2),transform=ax3.transAxes)


ax3.legend()

'''
Here we summarize the three results.   You should see that the no-error
-bars fit is Pretty Bad, the other two are Pretty Good, but the real 
non-straight-line  model fit is systematically a bit better.   The 
linearized fit works OK in many cases but is notably bad at handling 
outliers.   
'''

ax4.errorbar([1,],[ex1slope,],yerr=[ex1err,],
                 label="line fit, no err",marker='o')
ax4.errorbar([2,],[ex2slope,],yerr=[ex2err,],
                 label="line fit w/ err",marker='o')
ax4.errorbar([3,],[ex3slope,],yerr=[ex3err,],
                 label="raw data fit",marker='o')
ax4.plot([0,4],[true_slope,true_slope],
             linestyle=":",color='red')
ax4.legend()
