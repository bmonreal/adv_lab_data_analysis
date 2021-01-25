You are a particle physicist.  A previously-unknown particle has been created in your apparatus; when it appears it decays into a pair of muons.  Each muon enters a region where the magnetic field B makes it curve.  Your apparatus lets you measure the curvature $R$ so you know the muon's momentum _p_ via the Larmour formula.  In the form given below, plugging in _B_ in tesla and _R_ in meters will yield _p_ in the units GeV/c.

_p = BR/3.3356_ 


You also measure the initial direction of each muon track, so you know the angle $\theta$ between them.
 
Once you know the both muons' momenta p<sub>1</sub> and p<sub>2</sub> you can calculate the mass M (the "invariant mass") of the particle that decayed; the formula you should use is: 

_M<sup>2</sup> = p<sub>1</sub> p<sub>2</sub> (1-cos(\theta))_ 

(Note that this is strictly true only for massless particles, which muons are not, but for the purpose of this exercise please treat this as the correct expression.)  

Due to limitations of the spectrometer, there are uncertainties on all of these things.

When the spectrometer measures a radius, it is expected to be accurate to +/- 1cm.
When the spectrometer measures an angle, it is expected to be accurate to +/- 0.01 radians.

To activate the spectrometer, you have turned on an expensive power supply that delivers 100.000 Amps of current through a large coil; you know the power supply is reliable and steady to a precision of 0.001 Amps.  Secondly, you took a portable Gaussmeter and measured the magnetic field to be B=1.023 Tesla.  However, the gaussmeter manual says to assume 1% uncertainty in the field value, so you write down B = 1.023 +/- 0.01023.  You know that the magnetic field is proportional to the current, but unfortunately this Gaussmeter has limited your knowledge of what the proportionality *is*.  

Finally, some of the muon pairs that have entered the spectrometer are NOT from the interesting mystery particle; they have random momenta and random directions, and in this particular spectrometer they end up reconstructing to a "flat" background, fairly uniformly distributed over masses. That's the hope, anyway.  

1. EXAMINE THE DATA: The above describes what *should* have happened.  Remember that real instruments sometimes do things they shouldn't.  Look at the data set and see if there are any datapoints or data subsets you have reason not to trust.    

2. HISTOGRAM: Each muon pair recorded can be translated into an M value.  Any one such evaluation is not, unfortunately, the exact mass of the unknown particle, since there are errors in R1,R2,theta, and B.   Compute M for each particle-pair and make a histogram of the results.  Choose histogram bin widths---not too many or too few---such that the background, the signal peak, and the width of the signal peak are reasonably visible.  Make sure you can label the y-axis with the correct units. 

3. COUNTING STATISTICS: If you knew the true underlying theory and all the parameters, you'd be able to predict the long-term-average contents of each bin of your histogram: you could make statements like "The fifth bin gets an average of 33.2234 events per hour".  But the arrival/nonarrival of events in that bin is subject to Poisson statistics.  For a bin with N counts, you can assign sqrt(N) as the uncertainty in the count---unless N=0 in which case you should assign 1.0.  (Neither of these assignments are precisely justified but they are fine in this case.)  Put these error bars on your plotted histogram in an attractive and professional-looking way. 

4. FIND THE MASS AND WIDTH: Do a four-parameter nonlinear fit to the shape of the histogram.  Your model should add a flat "background" of unknown height and a Gaussian-shaped "signal" of unknown mean, width, and normalization.  Make sure you explicitly tell the fitter to use the counting errors you calculated above.

5. ASSIGN STATISTICAL AND SYSTEMATIC ERRORS TO THE MASS. Your knowledge of the mass is limited *both* by:
   1. statistical fluctuations in the pattern of detector errors---the coin-flip nature of whether the detector response fluctuated high or low---which your fitting procedure should be able to tell you about.
   2. the magnetic field uncertainty. Does the fitter have any way to know what the magnetic field is?

6. BONUS: INTERPRET THE WIDTH.  Your nonlinear fit will tell you the width of the observed peak.  Is this the width you expect from the propagation of spectrometer-related errors?  If so, the particle itself must have a "narrow" decay peak.  On the other hand, if the observed width is larger than you can blame on the spectrometer, maybe the particle itself (or some other effect) is contributing additional broadening to the muon pair invariant mass distribution.  (A particle will have a "decay width", i.e. a broad M distribution, if it is short lived; this is just the Heisenberg energy-time uncertainty principle.)  Report any conclusions you can draw from the width.

7. DISCUSS THE RESULTS. In the beginning of this exercise I described how we expect the apparatus and the data to behave; does anything about the plotted/fitted data deviate from that expectation?  Does it affect your confidence in the result and your choice of error bars? 
