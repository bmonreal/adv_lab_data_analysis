# Statistics and decisionmaking

Sometimes, these error analyses seem like "Prof Monreal told me to analyze error bars so I'll do it".  I would like to work through a few practical examples where they are important---where  either overestimating them OR underestimating them is costly.

## Shutting down LEP in the face of a hint of the Higgs

The LEP electron-positron collider ran from 1989 to 2000.  It was originally designed to deliver collisions with 182 GeV total energy, which were monitored by the four experiments ALEPH, L3, DELPHI, and OPAL.  In 2000, by pushing many subsystems beyond their design values, LEP was able to do some some running at 205 GeV (still a record for electron-positron collisions).  Every energy increase like this gave LEP the ability to search for new never-before-seen particles; there might be a particle you can't make in (say) 195 GeV collisions but you can make at 205 GeV.

In the last months of running, the ALEPH experiment claimed to have seen 8 events that matched the predicted properties of the then-undiscovered Higgs Boson, corresponding to a Higgs with mass 114 GeV.  Here are the claimed observations as of September 5, 2000.  I will report, not a number-of-events, but the "probability that background could fluctuate into a signal this high or higher".  

1. ALEPH claimed their signal was P=1.6e-4
2. L3 claimed their signal was P = 0.84 
3. DELPHI claimed their signal was P = 0.67
4. OPAL claimed their signal was P = 0.47

In other words, only ALEPH saw anything interesting; the others saw events consistent with background.  But ALEPH's signal was "huge".

There are two hypotheses we can consider: (a) there is no 115 GeV Higgs, and ALEPH's rare fluctuation was a fluke or a mistake; and (b) there is really a 115 GeV Higgs (i.e. the true value of X is above zero); ALEPH's reading was high-ish but not too unlikely, and the other three experiments' readings were low-ish but not too unlikely either.

### Exercise 1:

To give us a simple handle on this, let's translate the probabilities above into familiar terms.  Let's say every experiment was measuring a quantity X.  In the null hypothesis, X has a normal distribution with a mean of 0 and a standard deviation of 1.  Translate the probabilities above into the four values of X (X<sub>A</sub>, X<sub>L</sub>, X<sub>D</sub>, X<sub>O</sub>) that the experiments had reported on September 5th.  (Note: the object `scipy.stats.norm` has many useful functions related to normal distributions, in particular `scipy.stats.norm.cdf(x0)` which tells you the probability of drawing X < `x0` and its inverse `scipy.stats.norm.ppf(p)` which tells you what value of `x0` would give a CDF probability `p`.  

IMPORTANT NOTE: after this point in your code/notebook, you will be doing various calculations like "how many standard deviations is X<sub>A</sub> from zero?".  Although I just told you that the standard deviation in any X is 1.00, and many `scipy.stats.norm` functions have `stdev=1` as a default, please enter this as a variable, because we're going to change it later.

If the null hypothesis is true, as we saw, the probability of ALEPH fluctuating this high is  1.6e-4.  What is the probability of _any one_ experiment fluctuating as high as ALEPH did?

Suppose the four experiments can just average their data together to get X<sub>mean</sub>.  What is the standard error on the mean, and what is the statistical significance of its deviation from 0?  

### Exercise 2:

Let's use chi2 to quantify the "weirdness" of the observation.  Calculate chi2 of this dataset  if the null hypothesis is true.  (Having four experiments is like having four points on a curve.)  Calculate P(chi2) using the scipy.stats.chi2.cdf function.  

Now we apply our your parameter-scan skills.  Consider a range of possible values for the expected value of X<sub>E</sub> which is common to all four experiments.  (I.e., as though the Higgs Boson exists are we are trying to determine how often it is produced.)   At what value of X<sub>E</sub> is chi2 minimized?  What is the P(chi2) here?  

### Exercise 3:

Based on ALEPH's excess, LEP ran for an additional month (let's call it "run 2"). In Run 2:

1. ALEPH claimed their signal was P=0.43
2. L3 claimed their signal was P = 9.0e-3
3. DELPHI claimed their signal was P = 0.52
4. OPAL claimed their signal was P = 6.2e-2

Translate these into X-values using the mean=0, sd=1 model as before.  (Since Run 2 is shorter than Run 1 this is not quite right, but let's pretend it is.) 

We can do a couple of things.

1. Treat Run 1 and Run 2 as independent; you now have eight X-values; do the chi2 X<sub>E</sub> scan as before. 
2. For each expriment, average the Run 1 and Run 2 numbers to get its final X (think carefully about the standard deviation on this); repeat the four-X-value chi2 scan as before.

### Exercise 4: The $100M decision

This all happened at the very end of LEP.  The collider was scheduled to be shut down on November 2nd and almost immediately torn out of its tunnels; construction crews were standing by to start the installing the Large Hadron Collider, and delaying them (even by a few months) would have had a huge monetary cost.

Of course, CERN exists to discover things like the Higgs.  It would be terrible to _miss the discovery_ because you failed to follow up on the obvious first hints.  It would also be terrible to _waste a huge amount of money_ chasing an unimportant fluctuation.  In fact, LEP physicists applied to the CERN steering committees to ask to delay the shutdown and run LEP into 2001.

How many more months would YOU ask for?  It would be nice for the data, if it really is a Higgs signal, to be a five-sigma discovery (probability of background fluctuating < 3e-7) at the end of the run.  If the data-so-far really is an unlucky fluctuation of the null hypothesis, how quickly do additional runs make this obvious?  Come up with some plots that would guide the decisionmaking.  The worst outcome, of course, is to spend the money on more running but not to reach a conclusion.

### Exercise 5: Impact of incorrect error bars

One point of this exercise is the importance of the *correctness* of the error bars.

Take all of the X-values you've calculated so far.  You've used them in various probability calculations and various chi2 calculations that assumed sigma=1.00 on the basic experiment-run-data-points.  Let's imagine that, for the same set of X-datapoints, the experimentalists had misunderstood and misreported the error bars.  (At this point you may want to wrap your previous code in a loop which cycles through several different values of sigma.)

#### The failure of being too optimistic

Imagine the experimentalists had been "too optimistic", neglecting a real source of fluctuation in their data, and gone through the process reporting sigma=0.66.  Look at your previous plots and probabilities.  What goes wrong? 

#### The failure of being too conservative

Imagine the experimentalists had been "too conservative"; having measured X, rather than risk being wrong (or: rather than do detailed enough calculations to establish what the error is), assigned a "safer" error bar of sigma=1.5.   Look at your previous plots and probabilities.  What goes wrong?

### Epilogue

After a week of internal debate---both about statistics and about economic and political costs---CERN did not approve the extended LEP run.  The way I heard the story, as soon as the directorate turned down the extension request, they immediatly sent crews in to slice apart key power cables, so the decision would be irreversible and could not be bogged down in appeals.  And we learned in 2012, from the LHC, that the Higgs mass is 125 GeV.  The LEP "evidence" _was_ just a fluctuation.

References:

https://www.cap.bnl.gov/mumu/studyii/editor_meeting/Hanson.pdf  summarizes the whole business
https://onlinelibrary.wiley.com/doi/abs/10.1002/1521-3978%28200112%2949%3A12%3C1147%3A%3AAID-PROP1147%3E3.0.CO%3B2-A is the most comprehensive scientific article I could find on this excess
http://cds.cern.ch/record/462627/files/cer-2215407.pdf documents the request for the "Run 2" month
http://cds.cern.ch/record/476386/files/cer-2229903.pdf documents the later "no consensus
to recommend an extension"

 
