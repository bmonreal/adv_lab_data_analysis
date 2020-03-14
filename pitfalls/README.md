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

You can come close-ish.  Let's try to estimate the average expected value of each datapoint, by using a preliminary fit.  (Actually, you have already done this.)  Now, let's use that fit result to concoct an error bar to assign to each of those points.  Your goal is to answer: (either numerically or analytically) "For a data point X where the Poisson mean is some small number Y, you can predict the probability P of obtaining X>=1.  If you have a Gaussian whose mean is also Y, choose a standard deviation such that the probability of X>=1 is the same value P that is was for the Poissonian."  If your data is mostly zeros and ones, this approach will make the chi^2 calculation get rewarded (or penalized) appropriately.  It thinks it's getting rewarded for hitting the right ratio of zeros and ones in some Gaussian noise---you're the only one who knows that that ratio came from Poissonian noise.  (And note that it will get rewarded a little incorrectly when the data fluctuates up to 2.) 

Using those values as the error bars will let you do a second, improved fit.

Iterating this will converge.

That is about as good as it's possible to do with the chi-squared test statistic.  We can do better with more-complicated tests, like log-likelihood, in the future.

### Summing up this exercise

The point here is not to give you a prescription for how to handle zeros in data.  It is a reminder that:

1) Error bars and test statistics are not black magic.  You can try different ways of approaching them, and test these approaches on fake data. 
2) 

## Exercise 2: The Trials Penalty

You are a particle physicist looking for new particles.  Your detector is sensitive to muon-antimuon pairs crashing into it; since some particles, like many neutral mesons, can decay into muon pairs like this.  For each muon pair in the detector, your analysis has used the muon momenta to calculate the mass of the parent particle that decayed; it can reliably measure the mass to 0.15 GeV. If (for example) a 3.1 GeV meson existed, when you make a histogram "number of particles observed vs. mass", using 0.15 GeV-wide bins, and you would see all these events in the bin containing 3.1 GeV.  Your experiment covers from 1 to 10 GeV in 60 bins.   Unfortunately, when you bin the data and make a histogram, there is a background.  You get an average of 100 events per bin every day, all over your spectrum.

### 2a: Prediction and discovery
A theorist comes to you with the following thought: "I expect there to be a new particle at 5.5 GeV.  I expect it to appear at a rate of 10 events per day.  How long do you have to run to detect it?  The detection needs to be at 95% confidence---the probability that a background-only dataset fluctuates high and tricks us should be only 5%."   How many days do you have to run?  (Think about an analytic solution before moving on to simulations.)  

Take the background-only hypothesis (with the appropriate number of days), run 100 simulations of it, and examine each run for whether there's an accidental 15-event-per-day fluctuation in the 5.5 GeV bin; show that it's around 5% as desired.

(Note: in a real experiment we would also worry about missed detections---what if the signal is really there but fluctuated downward?---but let's ignore that now.) 

### 2b: Search and discovery
A theorist comes to you with a similar idea---a previously-unknown 10-events-per-day meson---but doesn't have a prediction for the mass.  It might be in any bin between 1 and 10 GeV.  How long do you have to run to get a 95%-confident detection?

Take the background-only hypothesis (with the appropriate number of days), run 100 simulations of it, and examine each run for whether there's an accidental 10-event-per-day fluctuation anywhere; show that it's around 5% as desired.

### Summary
The difference between these conditions is called a "trials penalty", the "look-elsewhere effect", or the "multiple comparisons problem".  

## Exercise 3: Run length variations

This actually happened in the late 80s and 90s when several scientists (and nonscientists) claimed they could generate nuclear fusion by running electric currents through deuterium-soaked palladium; generally asserting that  D+D-->3He + n or D+D-->4He + gamma reactions were occurring.  Many people claimed to see extra heat, which they attributed to fusion.  A few claimed to see statistically significant excess neutrons.

Here is how many of these experiments worked:
a) Start neutron counter.  Run for 5 minutes with palladium gizmo turned off.  Interpret the counter value as the natural background 
b) Turn on the gizmo.  While it is running, watch the neutron counter.  If you see a two-sigma excess over background, end the run and log the result.  If it runs for an hour and hasn't shown an excess, end the run.  "These phenomena are fickle," you report.

At the end, report the number of successful runs. 

Simulate this technique and show what can go wrong.
