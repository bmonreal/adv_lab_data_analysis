# The basic of means and averaging

One of the basic principles of statistics is understanding when *more measurements* is better than *fewer measurements*.  In a stats class you might explore that by learning mathematical facts derived by people like Fisher, Pearson, or Kolmogorov.  Here we will try to discover these facts experimentally.

Imagine an apparatus whose job is monitoring the wavelength of a stellar spectral line.  The underlying truth is that the line is at 588.9950 nm. Each run of your apparatus requires a 5-minute exposure and its wavelength-result has random fluctuations whose standard deviation is 0.1 nm.  If you took one such exposure you would have a result with an error bar of 0.1 nm.

The standard statistical claim is that, if the single-run error is X, and you average together N runs, the error on the average is X/sqrt(N); this is called the "standard error on the mean."  In this lab, we will explore that fact and its implications and exceptions.

## Exercise 1 (solo)

Simulate N runs of such an experiment by having Python generate a set of random numbers with the specified properties.  Here is a code snippet to get you started:

```
true_wl = 588.9950
sigma_run = 0.1
rundata = [true_wl + np.random.normal(0,sigma_run) for i in range(N)]
```

For several values of N, calculate the average of N runs.  Plot this average as a function of N and show that it gets closer to the mean following the expected 1/sqrt(N) behavior.  You should see that 68% of the runs are within 1-standard-error of the truth.

Your plot should be able to convince me that the improvement is really 1/sqrt(N) and not 1/N or some other factor.  

## Exercise 2 (solo)

Repeat the "average together N runs" thing above, making a set of 10 complete-N-run-experiments for each N.  For each N you can now calculate the standard deviation (i.e., the actual observed standard error on the mean) using the set of 10 experiments.  Make a plot with N on the x-axis, and standard-deviation-of-the-experiments on the y-axis, as a clearer test of the 1/sqrt(N) expectation.

## Exercise 3 (with a lab partner)

We said earlier that a run (with 0.1nm precision) takes 5 minutes.  However, finding the absolute values of the wavelengths involves a calibration procedure that takes a long time, and the calibration constants drift over time---it's a slow drift, and not necessarily linear, but it does mean you *cannot* just average together all your data.  Please analyze the dataset from [spectrometer.py](spectrometer.py) and provide your best estimate of the wavelength of the line observed (and put an error bar on this estimate) Can you do better than 0.1 nm?  


