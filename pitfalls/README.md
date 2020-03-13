# Pitfalls

In this set of exercises, we will simulate datasets where common fit procedures run into trouble.

## Exercise 1: How do we handle zeros?

Consider an experiment trying to measure the lifetime of a radioactive nucleus.  The expected number of nuclei decaying in the window between t and t+dt is described by a function like this:

```
def decaycurve(t,n0,lifetime):
	return n0*np.exp(-t/lifetime)
```

but there is also sometimes background noise, at entirely random times, which makes it look like a nucleus decayed at that time.

```
def decaycurvewithbackground(t,n0,lifetime,background):
	return n0*np.exp(-t/lifetime) + background
```

You are used to the idea of calculating the error on *counting data* by taking the square root of the number of counts.  We can't do that here because so many of the datapoints are zero.

### Exercise 1a:
Fit the dataset supplied in [zeros.py](zeros.py) and determine n0, the lifetime, and the background.  Try each of the following strategies:
1) Discard all the zero-valued points from the dataset.
2) Set the error bars to sqrt(N) but with a minimum of 1.00

## Exercise 1b:
Do you believe either answers in 1a?  Pick a values of n0,lifetime, and background corresponding to the numbers you found above.  Run a fake-data-generation-and-fitting exercise involving at least 50 datasets, for one or the other of the methods above.

1) "Did the fit work?"  Each run of the dataset-generation-and-fitting process  gives you a lifetime and a lifetime-error.  Devise a way to present this set of results that tells me whether the fits "worked" or not.

### Exercise 1c (with a partner):

What *should* the error bar be?  In truth, if you have a theory which predicts "if the theory is true, this data point has an 80% probability of being 0, 15% 1, and 5% 2, etc., for an average of 0.2", then ... we have a small problem.  This is not a Gaussian distribution, so there is no way that a chi-squared distribution will respond *quite* correctly when presented with situations like "the data is a 2 where the theory predicted 0.3"

You can come close-ish.  Let's try to estimate the average expected value of each datapoint, by using a preliminary fit.  (Actually, you have already done this.)  Now, let's use that fit result to concoct an error bar to assign to each of those points.  Your goal is to answer: (either numerically or analytically) "For a data point X where the Poisson mean is some small number Y, you can predict the probability P of obtaining X>=1.  If you have a Gaussian whose mean is also Y, choose a standard deviation such that the probability of X>=1 is the same value P that is was for the Poissonian."

Using those values as the error bars will let you do a second, improved fit.

Iterating this will converge.

That is about as good as it's possible to do with the chi-squared test statistic.  We can do better with more-complicated tests, like log-likelihood, in the future.


