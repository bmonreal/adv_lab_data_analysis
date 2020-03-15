# Fitting exponential data: some pitfalls and a real example

## Exercise 1
In a separate exercise, I wrote up notes walking through some exponentially-falling data.  Fitting it via the technique "take the log of the y-values, than fit a straight line" gives notably different results than "fit to an exponential function".  Please load and run the code at [log_vs_exponential.py](log_vs_exponential.py) and try to understand what it's doing.

## Exercise 2: Pierre Auger data
Let's try that on some real data. I have uploaded here the current published spectrum of ultra-high-energy cosmic rays from the Pierre Auger experiment, downloaded from [auger.org](https://www.auger.org/index.php/document-centre/finish/115-data/5045-combined-spectrum-data-2019) and published in [these ICRC proceedings](https://arxiv.org/abs/1909.09073).

Ultrahigh energy cosmic rays are common at lower energies and rarer at higher energies.  In particular, they roughly follow a "power law" distribution; the flux per unit energy is proportional to the energy to some power.

```
def fluxmodel(energy,scale,exponent):
	return scale*np.power(energy,exponent)
```

While exponentials turn into straight lines on a semilog plot (because log(Ae^(Bx)) = B\*x + log(A)), power laws turn into straight lines on a log-log plot (because log(A\*x^B) = log(A) + B\*log(x))

### 2a: understand the Auger data as given
Get the Auger data file read into useful Python arrays.  This is a histogram, but already on a log-10-scaled x-axis, so let's be careful for a second.  The first column is the log10 of the energy of that bin center (with the energy measured in eV).  The first data point tells you about the flux in the region 10^(16.50) eV < E < 10^(16.60) eV (in other words from 3.16e+16 to 3.98e+16), while the last data point tells you about the flux from 10^(20.1) to 10^(10.2) eV (in other words from 1.26e+20 to 1.58e+20 eV).  The later bins are much wider than the earlier ones!  In fact, the bin widths increase linearly with the energy.

Normally you ought to express a flux as a flux *density*, and report something like "events per [m^-2 s^-1 sr^-1 eV^-1]".  But here they have multiplied this conventional flux density (called "J") by the event energy ("E").  Unit-wise, this is why column 2 is "J\*E in [m^-2 s^-1 sr^-1]" and doesn't quite look like a flux density.  (They do this because a plot of "J\*E vs E" has the same powerlaw as the plot of "counts per bin vs E" in the presence of the uneven binning.)

That is a roundabout way of saying: we don't care too much about the extra factor of E, because *for power-law data*, multiplying the data by any power of E leaves you with data that still obeys a power law.

The third and fourth columns of the data are the error bars, given separately for positive and negative fluctuations.  They're almost all equal, or very nearly so, so you may treat them as symmetric.

1) Your assignment: Prove the "power law data times E^x is still power law data" statement.
2) Plot the Auger data on a log-log plot.  Choose a power-of-E to multiply by such that it becomes fairly easy to see the error bars.

### 2b: Fitting a simple power law
Focus on the region from 10^17.3 to 10^18.5 eV.
1) Do a linear fit to log(J) vs log(E) to find the spectral index.
2) Write a power-law fit function and do a nonlinear fit to find the spectral index.

### 2c: Fitting a broken power law
The data over 10^16.5--10^18.5 region is a bad fit to a power law.  Try to describe this data as a "broken power law": one exponent applying to the low region, another exponent applying to the high region.  You should use the fitter to find the optimum break point.  Note that it should only be a four-parameter fit (two exponents, one scale, and the breakpoint) and the function should be guaranteed to be continuous at the point of the change in exponents.

The breakpoint is called the "ankle" of the cosmic ray energy spectrum.

### 2d: In case your other instructors are phoning it in in coronavirus season and you're feeling under-challenged.
The Pierre Auger paper linked above gives (page 16, equation 3.1) the nine-parameter fit function that describes the entire spectrum.  Neat, huh?  If you are feeling ambitious, see if you can get this function to fit the data and reproduce the published numbers. 




