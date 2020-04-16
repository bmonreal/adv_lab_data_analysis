# Minimize your own function

For most of the class we have been talking about properties of the quantity 'chi^2'.   Chi-squared is what we call a "test statistic"---a single number that tells you how close your model is to your data.  For chi2 we have already seen the two aspects we care about:

1. If you adjust your model parameters in a way that minimizes chi^2, you've found a particularly attractive set of model parameters.
2. When you choose model parameters near-but-not-exactly at the minimum, the behavior of chi^2 can be translated into uncertainties.

Chi^2 is not the only test statistic that has this property.  Let's look at some other ones.

## A level deeper than curve_fit

Deep in the source code, `curve_fit` is just a user-friendly 'wrapper' function.  The ugly details---deciding which parameters to adjust, deciding when to stop, deciding what errors to report---are handled by (usually, I think) `scipy.optimize.least_squares`.  It is worth looking at the [documentation for this](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html#scipy.optimize.least_squares) function because it documents some interesting options.  But it's also worth understanding what it does.

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
```

What this means is that `least_squares` will let you interfere with the calculation of the test statistic you're going to minimize.  The chi^2 you have calculated in the past has been basically `sum(pull^2)`.  Every fluctuation gets squared and the squares are added up.   What if you did `sum(arctan(pull^2))`?  That'd look like standard chi^2-adding-up of small pulls (because arctan(x) &asymp; x for x<1) but suppresses the importance of large pulls.  What if you did `sum(abs(pull))` (the option 'soft_l1' above is an approximation to this)?

### Exercise 1:
Take the dataset and four-parameter model from [deep_dive/](deep_dive/) (and sensible starting guesses). Continue using `curve_fit` but try each of the five `loss=` options.  (These arguments are handed down from `curve_fit` to `least_squares`.)  


