# Minimize your own function

For most of the class we have been talking about properties of the quantity 'chi^2'.   Chi-squared is what we call a "test statistic"---a single number that tells you how close your model is to your data.  For chi2 we have already seen the two aspects we care about:

1. If you adjust your model parameters in a way that minimizes chi^2, you've found a particularly attractive set of model parameters.
2. When you choose model parameters near-but-not-exactly at the minimum, the behavior of chi^2 can be translated into uncertainties.

Chi^2 is not the only test statistic that has this property.  Let's look at some other ones.

## A level deeper than curve_fit

Deep in the source code, `curve_fit` is just a user-friendly 'wrapper' function.  The ugly details---deciding which parameters to adjust, deciding when to stop, deciding what errors to report---are handled by either  `scipy.optimize.leastsq` or  `scipy.optimize.least_squares`.  It is worth looking at the [documentation for this](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html#scipy.optimize.least_squares) function because it documents some interesting options.  But it's also worth understanding what it does.

We should contrast the call with `curve_fit`.  For `curve_fit` you pass in (a) a function, which, on evaluation with parameters fed in, returns a theory curve (b) an array of data points.  `curve_fit` evaluates the function, subtracts the data points, and gets an array of residuals.  (As you have now done several times, an array of residuals can be quickly turned into a chi2 value via,. e.g., `sum((residuals/errors)**2)`.)

`scipy.optimize.least_squares` doesn't care about your data points.  It wants to be passed a function which, on evaluation with parameters fed in, returns an array of residuals.  "You may at this point have two questions," said your professor, actually meaning that he has two things to point out.

### Why not go all the way and say "pass in a function that returns chi^2 and I'll minimize that"?

The answer is that `least_squares` can be coaxed into minimizing test statistics other than chi2.  Part of the evidence for this is in the documentation.  Look at what `least_squares` does if you use the optional argument `loss=`:

```
   loss : str or callable, optional
        Determines the loss function. The following keyword values are allowed:
            * 'linear' (default) : ``rho(z) = z``. Gives a standard
              least-squares problem.
            * 'soft_l1' : ``rho(z) = 2 * ((1 + z)**0.5 - 1)``. The smooth
              approximation of l1 (absolute value) loss. Usually a good
              choice for robust least squares.
            * 'huber' : ``rho(z) = z if z <= 1 else 2*z**0.5 - 1``. Works
              similarly to 'soft_l1'.
            * 'cauchy' : ``rho(z) = ln(1 + z)``. Severely weakens outliers
              influence, but may cause difficulties in optimization process.
            * 'arctan' : ``rho(z) = arctan(z)``. Limits a maximum loss on
            a single residual, has properties similar to 'cauchy'.

        If callable, it must take a 1-d ndarray ``z=f**2`` and return an
        array_like with shape (3, m) where row 0 contains function values,
        row 1 contains first derivatives and row 2 contains second
        derivatives. Method 'lm' supports only 'linear' loss.
    f_scale : float, optional
        Value of soft margin between inlier and outlier residuals, default
        is 1.0. The loss function is evaluated as follows
        ``rho_(f**2) = C**2 * rho(f**2 / C**2)``, where ``C`` is `f_scale`,
        and ``rho`` is determined by `loss` parameter. This parameter has
        no effect with ``loss='linear'``, but for other `loss` values it is
        of crucial importance.

```

What this means is that `least_squares` will let you interfere with the calculation of the test statistic you're going to minimize.  The chi^2 you have calculated in the past has been basically `sum(pull^2)`.  Every fluctuation gets squared and the squares are added up.   What if you did `sum(arctan(pull^2))`?  That'd look like standard chi^2-adding-up of small pulls (because arctan(x) &asymp; x for x<1) but suppresses the importance of large pulls.  What if you did `sum(abs(pull))` (the option 'soft_l1' above is an approximation to this)?

#### Exercise 1:
Take the dataset and four-parameter model from [deep_dive/](deep_dive/) (and sensible starting guesses). Continue using `curve_fit` but try each of the five `loss=` options and a few different values of `f_scale=` (These arguments are handed down from `curve_fit` to `least_squares`.)  You will also have to pass argument `method='trf'`, which affects the minimum-search strategy but not, as you can confirm, the result.  By looking at the function, can you reason about why different treatments of outliers have the effects shown?

Try again, with a fake dataset generated from this code:
```
	true_y_values = narrowpeak(x_values,60,20,3,10)
	exp_y_values_ng = true_y_values + np.random.laplace(0,np.sqrt(true_y_values))
```

The Laplace distribution will spit out many more ugly outliers than the normal distribution.  What do the different loss functions do?

### Why would I ever call `least_squares` when `curve_fit` can do the same thing?

You use `curve_fit` if you have a set of parameters, and changing them changes the _parameterized theory curve_.  What if some of your parameters are easier to understand as affecting the _data_?

Imagine you are at a semiconductor fab.  You have gone through 10000 samples of a new transistor and, using an apparatus involving a temperature controller, determined their threshhold voltages `Vth`.  You are confident that a histogram of Vth will be a normal distribution, which you'd like to fit to find the mean `Vth_0` and width `sigma_Vth`.  However, you have learned that the temperature contoller was haunted; the data points you thought were at `T` were in fact at `T + a*T^2`.  If you knew `a` you could correct the `Vth` values easily and make a corrected histogram.  However, `a` is itself unknown and have to be found by the fitter.  

In this case, if you are given `a,Vth_0,sigma_Vth` it is easy to compute the residuals (by using `a` to transform the data before histogramming, and `Vth_0,sigma_Vth` to subtract from the histogram) and quite hard to write a general function of the sort used by `curve_fit`.  


#### Exercise 2:

Re-run exercise 1 by calling `least_squares` directly rather than `curve_fit`.  (This is just as an exercise and does not have the interesting features above, that is for next week.)  You will need to write a wrapper function which, internally, calls `narrowpeak`; more annoyingly, you will have to use a `lambda:` trick (or something similar) to deliver the actual *dataset* into the function.

#### Exercise 3:

Here is an alternative hypothesis for describing the Exercise 1 data.  Write a residuals-calculating function that reflects it:

"The y-values are mostly described by the narrowpeak() function; however, find the datapoint with the worst positive residual `R`, subtract `A*R` from that point, and add `B*R` to the point with the worst negative residual.

(There is no physical excuse for this, I am just trying to concoct something that fits in the 'transform the data during the fit' category.)

## Non-chi2 loss functions

The point of the above is to wean ourselves off `curve_fit`, which had previously tied us to chi^2 and chi^2-based fitting, and get closer to doing raw minimization on our own test statistics.  But that is probably for next week.
