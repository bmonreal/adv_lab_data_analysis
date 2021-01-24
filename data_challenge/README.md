You are a particle physicist.  A previously-unknown particle has been created in your apparatus; when it appears it decays into a pair of muons.  Both muons enter a region where the magnetic field B makes them curve.  Since you can measure the track's curvature $R$ you know the particle's momentum $p$ via the Larmour formula.  In the form given below, plugging in B in tesla and R in meters will yield p in GeV/c.

$p = BR/3.3356$ 


You also measure the initial direction of each muon track, so you know the angle $\theta$ between them.
 
Once you know the two muon momenta p<sub>1</sub> and p<sub>2</sub> you can calculate the mass M (the "invariant mass") of the particle that decayed; the formula you use is: 

$M^2 = p_1 p_2 (1-cos(\theta)) $

Due to limitations of the spectrometer, there are uncertainties on all of these things.

When the spectrometer measures a radius, it is expected to be accurate to +/- 1cm.
When the spectrometer measures an angle, it is expected to be accurate to +/- 0.01 radians.

To activate the spectrometer, you have turned on an expensive power supply that delivers 100.000 Amps of current through a large coil; you know the power supply is reliable and steady to a precision of 0.001 Amps.  Secondly, you took a portable Gaussmeter and measured the magnetic field to be B=1.023 Tesla.  However, the gaussmeter manual says to assume 1% uncertainty in the field value, so you write down B = 1.023 +/- 0.01023.  You know that the magnetic field is proportional to the current, but unfortunately this Gaussmeter has limited your knowledge of what the proportionality *is*.  

Finally, some of the muon pairs that have entered the spectrometer are NOT from the interesting mystery particle; they have random momenta and random directions, so they evaluate to fairly-random values of M.

0) EXAMINE THE DATA: The above describes what *should* have happened.  Remember that real instruments sometimes do things they shouldn't.  Look at the data set and see if there are any datapoints or data subsets you have reason not to trust.    

a) HISTOGRAM: Each muon pair recorded can be translated into an M value.  Any one such evaluation is not, unfortunately, the exact mass of the unknown particle, since there are errors in R1,R2,theta, and B.   Compute M for each particle-pair and make a histogram of the results.  Choose histogram bin widths---not too many or too few---such that the background, the signal peak, and the width of the signal peak are reasonably visible.  Make sure you can label the y-axis with the correct units. 

b) COUNTING STATISTICS: You will find some values of M with surprisingly many events and others with surprisingly few.  In an experiment like this, the events wind up in the bins they do by a random process following Poisson statistics.   A bin where theory tells you to predict N events is likely to wind up with a number of events fluctuating in the range $N \pm \sqrt(N)$.  It's not precisely correct, but it is pretty fair to reverse that reasoning: a bin with N events observed should be assigned an uncertainty of $\sqrt(N)$.  Put these error bars on your plotted histogram.

c) FIND THE MASS AND WIDTH: Do a four-parameter nonlinear fit to the shape of the histogram.  Your model should add a flat "background" of unknown height and a Gaussian-shaped "signal" of unknown mean, width, and normalization.  Make sure you explicitly tell the fitter to use the counting errors you calculated above.

d) ASSIGN STATISTICAL AND SYSTEMATIC ERRORS TO THE MASS. Your knowledge of the mass is limited *both* by: (a) statistical fluctuations in the pattern of detector errors---the coin-flip nature of whether the detector response fluctuated high or low---and which is visible to your fit routine---and (b) by the magnetic field uncertainty. Does the fitter have any way to know what the magnetic field is?   

e) BONUS: INTERPRET THE WIDTH.  Your nonlinear fit will tell you the width of the observed peak.  Is this the width you expect from the propagation of spectrometer-related errors?  If so, the particle itself must have a "narrow" decay peak.  On the other hand, if the observed width is larger than you can blame on the spectrometer, maybe the particle itself (or some other effect) is contributing additional broadening to the muon pair invariant mass distribution.  (A particle will have a "decay width", i.e. a broad M distribution, if it is short lived; this is just the Heisenberg energy-time uncertainty principle.)  Report any conclusions you can draw from the width.
