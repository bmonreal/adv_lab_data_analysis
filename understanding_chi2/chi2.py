'''
Example code showing some properties of error bars and the chi2 goodness-of-fit test
'''


import numpy as np
from matplotlib import pyplot as plt

plt.ion()
plt.clf()

'''
Let's suppose that the following hypothesis were true and led to the existence of some data. 
The data is "fake_exp_y_values".  
'''

true_mean = 5
true_amp = 100
true_wid = 2
true_offset =10
x_values =  np.array([i for i in np.arange(0,10,0.4)])
exact_y_values = np.array([true_offset + true_amp*
                               np.exp(-((i-true_mean)/true_wid)**2)
                               for i in x_values])
# if this is False, we will look at "fresh" fake data every time we
# run the code. if this is True, there is an immutable fixed dataset
# which you can look at over and over.
if False:
    # when the random seed is hardcoded we get the same Poisson
    # draws every time.  Run np.random.seed() later to reset! 
    np.random.seed(123456789)
    
fake_exp_y_values = np.array([np.random.poisson(y)
                                  for y in exact_y_values])

    
f, (ax1, ax2,ax3,ax4) = plt.subplots(4,1,figsize=(6,8))
ax1.set_title("Hand-comparing (not fitting) a hypothesis to data")   

'''
Normally when you run a fit routine, like scipy.curve_fit, something 
*inside* the fitter is picking parameter values and doing some sort 
of plausibility check.  "Is this parameter set a good match to the 
hypothesis?"   We can do those hypothesis checks ourselves.  This is 
not fitting, just testing.

Let's test the plausibility of the following alternate hypothesis.  
Try adjusting these values yourself!
The hypothesis makes prediuctions which go into "try_these_y_values".
'''
try_mean = 4.8   # Notice the data is generated centered at 5;
# by comparing it to a 4.8 we expect disagreement.
try_amp = 100
try_wid = 2  
try_offset =10
try_these_y_values = np.array([try_offset + try_amp*
                                   np.exp(-((i-try_mean)/try_wid)**2)
                                   for i in x_values])

'''
In experiments like this the appropriate y-error is often the square 
root of the number of counts.  However, there are some subtleties.  
Here, for example, I will enforce that the error never be zero.
'''
y_err = np.array([max(np.sqrt(value),1) for value in fake_exp_y_values])



'''
Always plot your raw data.   Here, we plot data and residuals on the 
same panel.
'''


ax1.plot(x_values,try_these_y_values,label="hypothesis")   
ax1.errorbar(x_values,fake_exp_y_values,yerr=y_err,linestyle='None',
                 label="data",marker='.')   

residuals = fake_exp_y_values-try_these_y_values
ax1.plot(x_values,[0]*x_values)  # draw a line at zero
ax1.errorbar(x_values,residuals,yerr=y_err,linestyle='None',
                 label="residual",marker='.')

ax1.legend()

'''
Plotting the "pulls" shows where your data and hypothesis disagree, 
normalizing the error bars.  The y-axis of the pulls plot is "number 
of error bars".  You can see  which points fluctuted 1-error-bar-up 
or two-error-bars-down or whatever, even when the data has wildly 
varying errors.  
'''

pulls = residuals/y_err
ax2.plot(x_values,[0]*x_values) # draw a line at zero
ax2.errorbar(x_values,pulls,yerr=[1]*len(x_values),linestyle='None',
                 label="pulls",marker='o')
ax2.legend()

'''
we can calculate what the value of chi2 is; if you have already 
calculated the pulls, just take the sum of squares of pulls.
'''

chi2 = sum(pulls*pulls)
chi2ndof = chi2/len(x_values)
ax2.text(0.5,0.1,"chi2/ndof = %f"%(chi2ndof),transform=ax2.transAxes)

'''
The nice thing about knowing the value of chi2 is that there is a
 standard statistical test. "If the fluctuations are just randomness,
 how often does chi2 fluctuate lower than this?".  This probability 
is P(chi2).  If the value of P(chi2) is close to 1.0, then this might
 be telling you something is wrong.  

a) if your model is correct, your data must have come from a rare bad
 fluctuation (which happens sometimes)
b) your model is wrong and your data disagrees with it for reasons 
other than random fluctuations.

If the value of P(chi2) is very close to 0.0, then your data is 
*unusually close* to your model ("it's rare to be lower"), so either:
a) if your model is correct, your data must have come from a rare 
good fluctuation (which happens sometimes)
b) maybe you assigned error bars which are too big

However, although we think of P(chi2)=0.9999 as a problem, 
and P(chi2)=0.0001 as a different problem, it is not correct to say 
"the best P(chi2) is 0.5".  If your fit worked, and your data has 
plausible- and ordinary-looking fluctuations away from the predictions,
 P(chi2) winds up being more or less evenly distributed between 0 and 
1. (Try running a bunch of "good" evaluations and you'll see this.)  

Notice that I get P(chi2) by calling scipy.stats.chi2.cdf.  That's a 
two-argument function.  The second argument is the "number of degrees 
of freedom".  This means: the number of data points MINUS the number 
of parameters your fit-procedure has optimized.  In this code we have 
not optimized anything so we are in the unusual ndof=npoints case.
'''
import scipy.stats
prob_chi2_lower_than_this = scipy.stats.chi2.cdf(chi2,len(x_values))
ax2.text(0.5,0.2,"P(chi2) = %f"%(prob_chi2_lower_than_this),
             transform=ax2.transAxes)

ax2.legend()


'''
If your hypothesis agrees with your data as well as possible, the pulls
 should follow a Gaussian distribution centered at zero and with width 
1.  Sometimrs a histogram is a good way to look at this. In particular, the pulls distribution lets you see whether a "bad chi2" is dominated 
by random-looking behavior (just a wide distribution of pulls, maybe 
telling you your datapoints' error bars were assigmed too small) or 
dominated by outliers (a nice Gaussian distribution of width 1 _plus_ 
a couple of points far away) or something else.

In the default settings of this code, you will probably see a bimodal 
histogram---the hypothesized curve (and parameter choices) yield many 
datapoints overshooting or undershooting the theory (mostly by small 
amounts) and "surprisingly few" landing right in the middle.  
'''
counts, bins,patches = ax3.hist(pulls,label="histogram of pulls",
                                    histtype='step')
ax3.text(0.1,0.9,"mean=%f"%(np.mean(pulls)),transform=ax4.transAxes)
ax3.text(0.1,0.7,"stdev=%f"%(np.std(pulls)),transform=ax4.transAxes)

'''
we'll draw a Gaussian on here to show what the pulls distribution 
should have looked like if the data/curve disagreement had been only 
random fluctuations.
'''

norm = sum(counts)
binned_gaussian = np.array([0.0]*len(counts))
bin_centers = np.array([0.0]*len(counts))
for i in range(len(counts)):
    bin_centers[i] = (bins[i+1]+bins[i])/2.0
    bin_width =  (bins[i+1]-bins[i])
    binned_gaussian[i] = (1/np.sqrt(2*np.pi)*np.exp(-0.5*bin_centers[i]**2))*bin_width*norm
ax3.errorbar(bin_centers,binned_gaussian,yerr=np.sqrt(binned_gaussian),label="expectation")

ax3.legend(loc="upper right")

'''
Finally, let's do a classic Monte Carlo exercise.   Imagine we had 
done the experiment 50 times.  50 times we'll test it against the 
"bad hypothesis" and 50 times we'll do a fit to find the "best 
hypothesis" (the actual truth---not even the fit result) 

Notice that SOMETIMES the "bad hypothesis" gives a totally-reasonable-
looking P(chi2)---right in the middle of the range that the "best fit" 
would give.  That's why we have error bars!  Sometimes the data's 
fluctuations genuinely make it "fit well" to something that happens to 
be wrong, and there is no diagnostic in the world that will change 
that. 

Notice that SOMETIMES the "best hypothesis" gives a P(chi2) near the 
top of the range---in the region we associate more with bad fits!  
That's why we can't be too strict about what sort of fit we call 
reasonable and what kind we don't.  P(chi2)=0.9 is often reasonable. 
P(chi2)=0.99 is rarely, but not never, obtained from reasonable 
fluctuations.  P(chi2)=0.999 is pushing it further but it DOES HAPPEN. 
'''

bad_hypothesis_Pchi2 = np.array([0.]*50)
best_hypothesis_Pchi2 = np.array([0.]*50)
for irun in range(50):
    # generate a new fake experiment
    fake_exp_y_values = np.array([np.random.poisson(y)
                                      for y in exact_y_values])
    # try this "bad" hypothesis and see how it matches
    try_these_y_values = np.array([try_offset +
                    try_amp*np.exp(-((i-try_mean)/try_wid)**2)
                    for i in x_values])
    y_err = np.array([max(np.sqrt(value),1)
                        for value in fake_exp_y_values])

    residuals = fake_exp_y_values-try_these_y_values
    pulls = residuals/y_err
    chi2 = sum(pulls**2)
    bad_hypothesis_Pchi2[irun] = scipy.stats.chi2.cdf(chi2,len(x_values))
    
    # try the "best" hypothesis and see how it matches
    residuals = fake_exp_y_values-exact_y_values
    pulls = residuals/y_err
    chi2 = sum(pulls**2)
    best_hypothesis_Pchi2[irun] = scipy.stats.chi2.cdf(chi2,
                                len(x_values))


ax4.hist(bad_hypothesis_Pchi2,label="bad hypothesis",histtype='step')
ax4.hist(best_hypothesis_Pchi2,label="best hypothesis",histtype='step')
ax4.legend()
    
