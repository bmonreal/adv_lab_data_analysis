
import numpy as np
import matplotlib.pyplot as plt

# calibration constant measured at 11:55
C0 = 4.87052

# results, in pixels, of 30 five-minute runs from 12:00 to 2:30


specDat = np.array([3050.04799962, 3050.65793633, 3050.90569409,
       3050.24155269,
       3050.22787491, 3050.35741371, 3050.43373716, 3050.40810523,
       3050.00879966, 3050.70846062, 3050.43380199, 3049.93443244,
       3050.35913566, 3050.49479939, 3050.43455763, 3050.57309314,
       3050.0926935 , 3050.39308078, 3050.24608074, 3050.09896557,
       3049.95573773, 3050.30141048, 3050.1304266 , 3050.26240642,
       3050.10285653, 3049.28562153, 3049.83249471, 3050.28712602,
       3049.65682186, 3049.0459217 ])

nruns = len(specDat)

# calibration constant measured at 2:35AM
C1 = 4.86894

# wavelength = pixelValue/calibrationConst

runnumber = range(nruns)
pixel_errorbar = 0.1*C0 # 
wl_errorbar = pixel_errorbar/C0 # and it turns out this leads to 0.1/C0/C0 errors on wavelength

# always look a the raw data
                            
plt.ion()
plt.clf()
fig, (ax1,ax2,ax3) = plt.subplots(3,1)

# here is a plot just using the starting calibration.  You can see the drift; runs 16 and higher are all downwards fluctuations.
ax1.errorbar(runnumber,specDat/C0,yerr=wl_errorbar,fmt='g+')
ax1.set_xlabel("run")
ax1.set_ylabel("pixel value")
dumb_average = np.mean(specDat/C0)
ax1.plot(runnumber,[dumb_average,]*nruns,linestyle=":")


#What value do we get if we just trust the recently-calibrated points?
wl0 = specDat[0]/C0
wl1 = specDat[-1]/C1
bestvalue = (wl0+wl1)/2
sem = wl_errorbar/np.sqrt(2)
print("wl0 = %f, wl1=%f, average = %f +/- %f"%(wl0,wl1,bestvalue,sem))


# You might try a linear interpolation of the shifting calibration, but
# it's not going to work great.  Watch this.
cal_line = np.array([C0 + (C1-C0)/(nruns+2)*(i+1) for i in runnumber])
wl_linear = specDat/cal_line
ax2.errorbar(runnumber,wl_linear,yerr=wl_errorbar,fmt='g+')
avg_linear = np.mean(wl_linear)
sem_linear = 0.1/np.sqrt(nruns)
print("average = %f +/- %f"%(avg_linear,sem_linear))
ax2.plot(runnumber,[avg_linear]*nruns,linestyle=":")
'''
This has removed evidence of the early/late drift, BUT maybe has just shifted
the problem to the middle---the 12th through 24th points are all high-fluctuations, 
unlikely if the data were really a constant wavelength.  I don't know what to put 
into my error bar reasoning---are these 30 random normally-distributed fluctuations
or are they miscalibrations?  I don't know! 
'''

# It is tempting to fit a polynomial to the data, but I don't advise it.  Here is why.
for N in [1,2,3,4]:
    coefficients = np.polyfit(runnumber,specDat,N)
    polycal = [np.sum([coefficients[i]*irun**(N-i) for i in range(N+1)]) for irun in runnumber]
    ax3.plot(runnumber,polycal,label="N=%d"%N)
    # it is not dirt-simple to figure out what to do with this particular polynomial; by itself it's not
    # the calibration curve, since we have particular values we think the calibration constant should
    # hit at the beginning and the end.  (I will not actually do this right now since it's annoying.)
ax3.errorbar(runnumber,specDat,yerr=pixel_errorbar,fmt='g+')
'''
What have we learned? Depending on our choice of polynomial, MAYBE we have learned that the 
calibration drifted down linearly, but also that wavelength was sort of high (with many data 
points lying ABOVE 626.226 nm).  Or maybe we learned that the calibration dropped fast at the 
end, the wavelength was fairly low, and the fluctuations sort of nicely alternately low/high/low/high.
YOU CAN'T TELL, so you mustn't pretend that you could tell, reporting the same sort of tiny error bar 
you'd have reported if the calibration was perfectly known.

Nor should you throw up your hands and say "well, I'll report one data point".  You spent a hard night 
at the telescope getting more than one data point.  Here is what I would do.  

0) We know the calibration drifted.  
a) The truth is somewhere between "calibration stayed the same" and "linear drift" 
but we don't know exactly where.
b) The polynomial fits are not nonsense---it DOES look more like the calibration 
changed faster at the end, so let's err towards "stayed the same"
c) Insofar as I trust this, I trust my ability to average together early data points.
d) The question is how many I trust myself to average.  Let's try various numbers.
'''

for n_good_points in range(1,30):
    average_c = np.average(specDat[0:n_good_points]/C0) # using the early coefficient as fixed
    average_l = np.average(wl_linear[0:n_good_points]) # using the linear-drift hypothesis
    ideal_sem = 0.1/np.sqrt(n_good_points) # standard error on the mean is our most optimistic error bar
    print("%d points: model disagreement %f vs optimistic error bar %f"%
              (n_good_points,average_c - average_l,ideal_sem))

'''
As you can see, the linear vs. constant models get further apart gradually, but our 
averaging-data-points-together also builds confidence gradually.  After averaging 5 data points,
our error bar is down to 0.044 nm (good!) while the models only disagree by 0.019 nm.  We can very nearly 
trust the standard-error-on-the-mean here.  After 10 data points, the random error and the model error are
about the same size.   Maybe we should stop there, with a statistical error AND a systematic error.
Such errors are usually added in quadrature.  Let's run that again with different printouts:
''' 

best_value = 0
best_error = 999
best_stat = -1
best_sys = -1
for n_good_points in range(1,30):
    average_c = np.average(specDat[0:n_good_points]/C0) # using the early coefficient as fixed
    average_l = np.average(wl_linear[0:n_good_points]) # using the linear-drift hypothesis
    statistical_error = 0.1/np.sqrt(n_good_points) # standard error on the mean is our most optimistic error bar
    systematic_error = (average_c - average_l)/2
    value_to_report = (average_c + average_l)/2 # split the difference of two models
    total_error = np.sqrt(statistical_error**2 + systematic_error**2)
    print("%d good points: wavelength %f +/- %f"%(n_good_points,value_to_report,total_error))
    if total_error < best_error:
        best_value, best_error, best_stat, best_sys = (
            value_to_report,total_error,statistical_error,np.abs(systematic_error))
    
# in fact it looks like the very best choice (in this picture) is to average the first 12 points:
print("We therefore report %.2f nm +/- %.2f (%.2f stat, %.2f sys))"%(best_value, best_error, best_stat, best_sys))

# If we tried to add weight to our suspicion that the linear-drift model is the less plausible one
# we could build that into our decisionmaking and averaging in some ad-hoc way.

plt.savefig("soln.png")





