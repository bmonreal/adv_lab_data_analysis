import json
import numpy as np
import scipy.stats
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
with open("false_minimum_data.json") as f:
     data = json.load(f)
     exp_y_values = np.array(data["exp_y_values"])

def narrowpeak(x,x0,norm):
    return norm*np.exp(-((x-x0)/3.0)**2) + 10

     
def verbose_narrowpeak(x,x0,norm):
    print("trying %06.10f %06.10f"%(x0,norm))
    return norm*np.exp(-((x-x0)/3.0)**2) + 10

f, (ax1,ax2,ax3,ax4) = plt.subplots(4,1,figsize=(8,10))
ax1.set_title("Fits in and out of a false minimum")


x_values = np.arange(0,80,2)

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

# plot a 1D scan of the best fit means

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
ax3.set_xlabel("fixed x0")
ax2.legend()



# plot a 1D scan of the best fit means focusing on the true minimum

mean_scan_values = np.arange(55,65,0.1)
mean_scan_results = [0]*len(mean_scan_values)
for itrial,fix_mean in enumerate(mean_scan_values):
    tmppopt, tmppcov = curve_fit(lambda x, norm: narrowpeak(x,fix_mean,norm), x_values, exp_y_values,sigma=y_err,absolute_sigma=True)
    
    tmpbest_fit = np.array([narrowpeak(x,fix_mean,tmppopt[0]) for x in x_values])
    tmpchi2 = np.sum(((exp_y_values - tmpbest_fit)/y_err)**2)
    mean_scan_results[itrial] = tmpchi2


# do the curve fit properly to get parameters
popt, pcov = curve_fit(narrowpeak, x_values, exp_y_values,sigma=y_err,absolute_sigma=True,p0=[60,1])
x0err = np.sqrt(pcov[0,0])
ax3.plot(mean_scan_values,mean_scan_results,label="chi2 scan of means")

# check chi2 at three values
for check_at_x0_plus_this,label_position in zip([-x0err,0,x0err],[50,-00,-25]):
    fix_mean = popt[0]+check_at_x0_plus_this
    tmppopt, tmppcov = curve_fit(lambda x, norm: narrowpeak(x,fix_mean,norm), x_values, exp_y_values,sigma=y_err,absolute_sigma=True)
    tmpbest_fit = np.array([narrowpeak(x,fix_mean,tmppopt[0]) for x in x_values])
    tmpchi2 = np.sum(((exp_y_values - tmpbest_fit)/y_err)**2)
    ax3.annotate("x0=%.2f chi2=%.2f"%(fix_mean,tmpchi2),(fix_mean,tmpchi2),(0,label_position),textcoords="offset points",arrowprops={"arrowstyle":'->'})    

ax3.set_ylabel("chi2")
ax3.set_xlabel("fixed x0")
ax3.legend()

# do that again at the bad fit point

mean_scan_values = np.arange(0,10,0.1)
mean_scan_results = [0]*len(mean_scan_values)
for itrial,fix_mean in enumerate(mean_scan_values):
    tmppopt, tmppcov = curve_fit(lambda x, norm: narrowpeak(x,fix_mean,norm), x_values, exp_y_values,sigma=y_err,absolute_sigma=True)
    
    tmpbest_fit = np.array([narrowpeak(x,fix_mean,tmppopt[0]) for x in x_values])
    tmpchi2 = np.sum(((exp_y_values - tmpbest_fit)/y_err)**2)
    mean_scan_results[itrial] = tmpchi2


# do the curve fit properly to get parameters
popt, pcov = curve_fit(narrowpeak, x_values, exp_y_values,sigma=y_err,absolute_sigma=True,p0=[1,1])
x0err = np.sqrt(pcov[0,0])
ax4.plot(mean_scan_values,mean_scan_results,label="chi2 scan of means")

# check chi2 at three values
for check_at_x0_plus_this,label_position in zip([-x0err,0,x0err],[50,-50,0]):
    fix_mean = popt[0]+check_at_x0_plus_this
    tmppopt, tmppcov = curve_fit(lambda x, norm: narrowpeak(x,fix_mean,norm), x_values, exp_y_values,sigma=y_err,absolute_sigma=True)
    tmpbest_fit = np.array([narrowpeak(x,fix_mean,tmppopt[0]) for x in x_values])
    tmpchi2 = np.sum(((exp_y_values - tmpbest_fit)/y_err)**2)
    ax4.annotate("x0=%.2f chi2=%.2f"%(fix_mean,tmpchi2),(fix_mean,tmpchi2),(0,label_position),textcoords="offset points",arrowprops={"arrowstyle":'->'})    

    
ax4.set_ylabel("chi2")
ax4.set_xlabel("fixed x0")
ax4.legend()



    
# Actually it is nice to be able to do a 2D plot by writing a function that packages up the whole calculation.
# later we can write this with a curve_fit, etc. inside the function, and accepting arbitrary fixed_param argument lists.

def get_chi2_with_fixed(func,xdata,ydata,sigma,fixedx0,fixednorm):
    theory = func(xdata,fixedx0,fixednorm)
    return sum(((theory-ydata)/sigma)**2)

fixedx0range = np.arange(58,64,0.3)
fixednormrange = np.arange(10,30,1)

z = [[get_chi2_with_fixed(narrowpeak,x_values,exp_y_values,y_err,x0,norm) for x0 in fixedx0range] for norm in fixednormrange]
plt.clf()

cs = plt.contourf(fixedx0range,fixednormrange,z,levels=20)
cbar = plt.colorbar(cs)
plt.show()





