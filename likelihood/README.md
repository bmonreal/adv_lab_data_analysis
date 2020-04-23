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
d            * 'arctan' : ``rho(z) = arctan(z)``. Limits a maximum loss on
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

The Laplace distribution will spit out many more ugly outliers than the normal distribution.  How do the different loss functions handle them?

### Why would I ever call `least_squares` when `curve_fit` can do the same thing?

You use `curve_fit` if you have a set of parameters, and changing them changes the _parameterized theory curve_.  What if some of your parameters are easier to understand as affecting the _data_?

Imagine you are at a semiconductor fab.  You have gone through 10000 samples of a new transistor and, using an apparatus involving a temperature controller, determined their threshhold voltages `Vth`.  You are confident that a histogram of Vth will be a normal distribution, which you'd like to fit to find the mean `Vth_0` and width `sigma_Vth`.  However, you have learned that the temperature contoller was haunted; the data points you thought were at `T` were in fact at `T + a*T^2`.  If you knew `a` you could correct the `Vth` values easily and make a corrected histogram.  However, `a` is itself unknown and have to be found by the fitter.  

In this case, if you are given `a,Vth_0,sigma_Vth` it is easy to compute the residuals (by using `a` to transform the data before histogramming, and `Vth_0,sigma_Vth` to subtract from the histogram) and quite hard to write a general function of the sort used by `curve_fit`.  


#### Exercise 2:

Re-run exercise 1 by calling `least_squares` directly rather than `curve_fit`.  (This is just as an exercise and does not have the interesting features above, that is for next week.)  You will need to write a wrapper function which, internally, calls `narrowpeak`; more annoyingly, you will have to use a `lambda:` trick (or something similar) to deliver the actual *dataset* into the function.

#### Exercise 3:

Here is an alternative hypothesis for describing the Exercise 1 data.  Write a residuals-calculating function that reflects it:

"The y-values are correctly described by the narrowpeak() function, however, the evenly spaced x-values are wrong.  The apparatus responds a little slowly after a large signal comes in.  The datapoint which is recorded at `x = x[i]` was actually taken at `x = x[i] - a*np.abs(y[i-i] - bg)` where `a` is some small delay parameter."  

(There is no physical excuse for this, I am just trying to concoct something that fits in the 'transform the data during the fit' category; I hope `a` will evaluate to a small number, since I did not put such an effect into the fake data, but I haven't tried it yet.)

## Non-chi2 loss functions

OK, at this point let's get into the real stuff.  The underlying science of "fitting a curve" is just finding the minimum value of a multiparameter function.  There are dozens or hundreds of strategies for doing this; picking the right strategy is not usually an interesting problem for a physicist.  (Go ask a computer scientist or applied mathematician.)  The basic Python routine we will use is `scipy.optimize.minimize`.  Please start by queueing up the [documentation for that](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize).  Most of the arguments are vaguely like those of `least_squares`, except the first.

The first argument is simply "give me a function which, given a parameter-choice vector, returns a scalar value".  To make things simple, let's do a very simple chi2 minimization.

Here is an example of a chi2 function definition and a `minimize` call.  

```
def f2min_my_model_chi2(params,xdata,ydata,yerr):
    ymodel = my_model(xdata,params)
    return sum(((ydata - ymodel)/yerr)**2)
	
guesses = [1,1,1,1]
my_results = minimize(f2min_my_model_chi2,guesses,args=(x_values,y_values,y_errors))
best_fit_params = my_results['x']
```

The parameter errors are a bit obscure---unsurprisingly, since `minimize` does not know anything about our problem; it does not even know that we have a data- or error-related problem at all.  What it does do is measure the second derivatives of the function around the minimum and report this; it's the "inverse Hessian matrix" and, in the specific case where `fun` is spitting out chi2, it's basically the covariance matrix.

```
uncertainties =  [np.sqrt(my_results['hess_inv'].todense()[i,i]) for i in range(len(guesses))]
```

### Exercise 4:  Fit some data

The following data (x,y, and errors) is supplied.  The underlying theory here is that `y` has a sigmoid form (specifically, an arctangent); you have to use four parameters to describe its asymptotic low value, its asymptotic high value, its `x`-offset (what value of `x` is the midpoint), and the steepness of the transition.

```
x_values =  array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10])
y_values = array([1.65115602, 2.03701695, 2.53525369, 3.05232566, 3.43550141,
         3.84288164, 4.12987307, 4.30959107, 4.39539739, 4.66194378])
y_errors = array([0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06])
```

Write the function `my_model()` and make this code work.   

### Exercise 5:  Use bounds

One of the reasons `minimize` is so complicated is the existence of optional `bounds` and `constraints`.  Here is a fake-data-generator which will compel you to use them.  

```
def my_model_with_a_sqrt(x,params):
    return params[0] + x*params[1] + np.sqrt(x*params[2])

x_values = np.array([1,2,3,4,5,6,7,8,9,10])
true_params = [5.4,0.4,0.3] # shhhh, don't look at this
input_variance = 0.06 # seeekrit
y_errors = np.ones(len(y_values))*input_variance

y_theory = my_model_with_a_sqrt(x_values,true_params) 
y_values = np.random.normal(y_theory, input_variance)
```

Why do we have to use bounds here?  Look at the `sqrt` in our function definition.  The minimizer doesn't "know" it's in there, it is just throwing parameter choices in and seeing what comes out.  Unfortunately in this case, sometimes it may take a stab at `params[2] < 0`, take the square root of a negative number, and the model will throw an error.  

There are three ways to address this.  Please try each of them.

#### 5a. Redefine the parameters.
Sometimes it is possible to rewrite the function slightly.  Can you devise a function with the same shape (or class of shapes) as my three-parameter `my_model_with_a_sqrt` but that doesn't have this problem at all?  

#### 5b. Use bounds.

The `minimize` function allows you to pass in the optional argument `bounds=`.  The sqrt-related crashes can easily be treated as a `bounds` problem; you have to tell the minimizer that the third parameter's lower and upper limits are `(0,None)`; it will then not attempt to adjust the parameter below zero.  Implement this and run it, printing out the parameter values and error bars.

Important pedagogical note: bounds can only be used safely to prevent the minimizer from _exploring_ a problematic region.  (You can use them to keep away from a known false minimum, for example.)  You want the minimizer to "bounce off" the bounds and find a minimum somewhere in the allowed region.  Run the fake-data-generation and (bounded) minimization problem several times; do you see any runs where the minimizer thinks `params[2]==0` (right at the bound) is the best fit value?  What happened? 

Important science note: supposing the fitter could tell you, believably, that it concluded `params[2] = 0.1 +/- 0.5`; given that negative values are "unphysical", how do you interpret the error bars?  

#### 5c. Use constraints (optional, a bit Python-hacker-y)

The `minimize` function allows `constraints=` to be passed in.  Constraints can be used to set interdependencies among variables; maybe your function (or your physics) requires that `params[0] < params[1]`; maybe a conservation law enforces that all of your parameters sum to zero; that sort of thing.  It does not do anything different than `bounds` in this case but it might be worth reading that part of the documentation.

### Exercise 6: Log likelihood minimization

To understand why `chi2` minimizers work, we had to jump through some mental hoops to explain why the sum-of-squares-of-pulls is related to how-likely-the-data-is-to-look-like-Y.   A lot of modern stats methods skip that, and just ask the "how likely" question directly in the minimization process.

Every time we encounter a data point `y_exp[i]`  (bearing a fluctuation governed by `y_err[i]`) and a hypothesis `y_th[i]`, we can ask: "if `y_th[i]` were true, how likely is `y_exp[i]`?"  We have already asked this, when the fluctuations were Gaussian, using the normal distribution CDFs.   (Here we will use the PDF, not the CDF.)

```
p[i] = scipy.stats.norm.pdf(y_exp[i],y_th[i],y_err[i])
```

When you have many data points, the probability of getting that whole ensemble is actually the *product* of all the probabilities.

```
ptot = 1
for prob in p:
	ptot = ptot*prob
```

If you maximized `ptot`, you'd have the best fit, just as if you minimized `chi2`.  (Notice we don't have a maximizer, we have a minimizer; we'd "minimize `-ptot`") However, it so happens that these long product calculations are prone to numerical errors.  What if we take the log of `ptot`?  The log of a product is the sum of the logs of the multiplicands.

`logPtot = sum(np.log(p))`

That quantity is the "log likelihood".  "Why is that worth computing?  Who cares?  It's easy to compute but it's not the thing we wanted to maximize!" you might say.  It's true, but remember that we wanted to maximize something.  The maximum of `ptot` is in exactly the same place as the maximum of the log of `ptot`.

#### Exercise 6a: Refit the exercise-4 dataset using log likelihoods

Write a function that returns the *negative* log likelihood of the data-theory comparison from Exercise 4, with the arctangent.  Use `scipy.minimize` to find the minimum negative log likelihood, e.g the maximum likelihood.

NOTE: when you are looking at any of the scipy.stats probability distributions

#### Exercise 6a: Refit the exercise-1 fake dataset using log likelihoods

Remember the Exercise 1 narrowpeak distribution---the one where we generated Laplacian noise?  You can use `scipy.stats.laplace.pdf` to get probabilities.  

Notice that, in the fake data generation step, we got the error bars (i.e. the fluctuation sizes) from the theory values.  Rather than passing `y_err` as one of the function parameters, please calculate it inside the function and use the calculated values as your errors.  (This was impossible with `curve_fit`; `least_squares` could have done it but we didn't bother previously.)

When you did Exercise 1, the interpretation of `chi2` was tricky (and the fits correspondingly wonky sometimes) because we were "adding up pulls"---but when we relied on mathmatical properties of the `chi2` statistics, we were implicitly relying on the pulls being normally distributed.  That problem is gone; your likelihood-PDF-lookups are putting in the relevant data from the actual relevant distributions.

### Error estimation using likelihoods (LL)

One neat thing you can do with likelihoods is the following.  Remember what we did with 2D chi2 parameter scans?  Try lots of different parameter inputs for the function, evaluate chi2, make a contour plot?  Well, we were making contour plots of the fairly-unintuitive parameter "chi2" and looking for also-fairly-unintuitive "region where chi2 deviates from its minimum a certain amount".

We can do something similar with our likelihood function---scan lots of values of input parameters---but this time the estimator we get out is physically or mathematically meaningful---it's a probability.  (Well, it's the log of a probability so you can get the probability back out of it.)  2D probability density functions are pretty easy to plot and easy to think about.   In fact, N-dimensional probability density functions are fairly easy to think about.  One thing that is particularly fine thing to do is to find the average value of a distribution.

Let's look at that arctan dataset from above;

```
x_values =  array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10])
y_values = array([1.65115602, 2.03701695, 2.53525369, 3.05232566, 3.43550141,
         3.84288164, 4.12987307, 4.30959107, 4.39539739, 4.66194378])
y_errors = array([0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06])
```

This time I will give you the function

```

def my_model(x,params):
    return params[0]*(np.arctan((x - params[1])/params[2]) + np.pi/2)/np.pi + params[3]
```

and tell you three of the four parameters: `[5.4,3.4,???,0.03]`.  I have left out the "steepness" parameter.

#### Exercise 7a: Do a one-dimensional scan
Try calculating the log-likelihood values obtained with values of `try_steepness= np.arange(-10,10,0.1)`.  By examination of that scan (not a fit) find the best fit value of the steepness.

#### Exercise 7b: Just straight-up find the centroid
You have a vector called `try_steepness` and another vector (called, say, `ll_values`) representing negative log-likelihoods.  Undo the log thing (it was just a numerical trick anyway, right?) and calculate `likelihood = np.exp(-ll_values)`.  Is there a calculation you can do that yields the mean steepness?  How close is it to the traditional minimization-based "best fit"?  

#### Exercise 7c: Error bars
The correct way to think about uncertainty in the likelihoods world is: can I draw a region on the `steepness` axis that encompasses 68% of the probability space?  There are actually various ways to approach that, depending on how you want to treat the symmetries---is it "68% of probability, with 34% above and 34% below the centroid"?  Or is it "68% of probability, picking high and low points of equal likelihoods with the centroid between them"?  Try to find a sensible error bar to put on this parameter.

#### Exercise 7d: Multidimensional sampling

The very neat thing about likelihoods is that the above 1D reasoning works very well in arbitrary numbers of dimensions.  Implement a 3-parameter model (say, fixing the fourth parameter at 0.03 and varying the other three); maybe try

```
try_range= np.arange(0,10,0.5)
try_x0= np.arange(0,5,0.5)
try_steepness= np.arange(0,5,0.5)
```

which will need 2000 calls to your LL function.  From the raw likelihood values, calculate the centroid of the probability distribution of each parameter.

Modern likelihood analysis takes basically this approach to "fitting"---just throwing in parameter-choices and evaluating likelihoods, never "minimizing" in the mathematical sense.  The Exercise 7d version was a simple scan, which did a lot of its 2000 computationally-expensive evaluations in "useless" regions of parameter space that don't affect things much; a family of common techniques suitable for everyday fitting, called Markov Chain Monte Carlo (MCMC), jump around the parameter space and try to spend less time in the useless regions and more time in regions of high likelihood.  We do not have time in this semester to teach you MCMC properly, but knowing how to write a likelihood function (as you now do) is one of the big barriers to entry in the field.  To learn more, I recommend the (STAN)[https://mc-stan.org/] software packages.  Good luck!





