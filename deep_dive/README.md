# A deep dive into the minimizer

The data file [false\_minimum\_data.json](false\_minimum\_data.json) is a JSON file containing an array of y-values.  (JSON is a useful format for saving data to text files; in Python it is like getting text files to store dicts.)  Here is how to import it:

```
with open("false_minimum_data.txt") as f:
     data = json.load(f)
     exp_y_values = np.array(data["exp_y_values"])
```

(The x-values are sequential integers.)  These y-values are fluctuations around the following hypothesis:


```
def narrowpeak(x,x0,norm):
    return norm*np.exp(-((x-x0)/3.0)**2) + 10

true_norm = 20
true_x0 = 60
params = [true_x0,true_norm]

x_values = np.arange(0,80,2)
exact_y_values = np.array([narrowpeak(x,*params) for x in x_values])
```

In other words it's a narrow Gaussian peak.  I have hardcoded the width=3, fixed background = 10, but you can adjust x0 (where the peak is) and norm (the peak amplitude) when you are running the fit.


## Exercise 1: watch the fit crash

Using `scipy.optimize.curve_fit` but *without supplying an initial guess* (or with initial guesses of the default `[1,1]`) to fit the given experimental data to the `narrowpeak` function.  Make a plot of the best fit, and do a  chi^2 test to quantify how bad the fit is.  

The result should be terrible; the fit gets stuck in a "false minimum".  One way out of this (which you may know) is to use a "better" initial guess.  But in real life you don't always know what initial guess might be "better".  

## Exercise 2: a full parameter scan

What is the fit routine doing?  It's doing little tests where it tries to vary each parameter, evaluates chi2 for each parameter set, and identifies directions for further variations which it hopes will lead to the minimum chi2.  It doesn't try *all* the possible parameter values.  But you can!  Here is how, within the simple `curve_fit` function.

We want to take our `narrowpeak` function, force Python to choose a particular value of `x0`, but (given that) let the minimizer find the best value of other parameters (here it's just `norm`.) 

To do that, we don't actually feed the whole `narrowpeak` function into `curve_fit`.  Instead, the Python `lambda` statement used below is sort of an on-the-fly redefinition of the function; instead of telling `curve_fit` to minimize a two-paramter function narrowpeak(x,mean,norm), we are asking it to minimize a one-parameter function.  To explain the Python, you can imagine that we defined the function like this:

```
fix_mean = 1.0 # pick some value of the mean
def unnamed_function(x,norm):
    return narrowpeak(x,fix_mean,norm)

curve_fit(unnamed_function,x_values,exp_y_values,,sigma=y_err,absolute_sigma=True)
```

The Python "lambda" feature basically lets you do that redefinition---it's called an "anonymous function"---inline with your code.  The entire first argument of `curve_fit`, below, is a temporary definition of a one-parameter function (which happens to be the `narrowpeak`-with-a-fixed-mean we want).  `curve_fit` sees that function and minimizes it just like it would have done above. 

```
fix_mean = 1.0 # pick some value of the mean
popt, pcov = curve_fit(lambda x, norm: narrowpeak(x,fix_mean,norm), x_values, exp_y_values,sigma=y_err,absolute_sigma=True)

```

Your assignment is to write a loop that (a) tries all possible values of `x0`, from say 0 to 100, and (b) does a fit with that mean fixed, and (c) evaluate chi2 for the result.

Make a plot where the y-axis is the best-fit-chi^2-at-this-fixed-mean, and the x-axis is the fixed mean.  Now, look back at Exercise 1.  What value of `x0` did the Exercise 1 fit identify as "best"?  What features on the chi^2 scan explains that result?

# Exercise 3: How the fitter got where it did

Repeat exercise 1 but with this fit function:

```
def verbose_narrowpeak(x,x0,norm):
    print("trying %06.10f %06.10f"%(x0,norm))
    return norm*np.exp(-((x-x0)/3.0)**2) + 10
```

Using this function will show you (in a printout) what values of x0 and norm the fitter attempted to look at.
1) What does it do to get started?
2) Does it test parameter-variations one parameter at a time, or changing both together?  
3) What evaluations does it do at or near the minimum?

# Exercise 4: Understanding the true minimum and the relationship between chi2 and the parameter errors

OK, now that we have done a full parameter scan, we can stop pretending we don't know what the true minimum is.  Run the ordinary minimization process one more time, this time using a better initial guess so that the minimizer finds the true minimum.

Evaluate chi2 at three specific points:
1) At exactly the best fit values.
2) Look at the error in x0 reported by the fitter.  Add one error bar to x0, then use the Exercise 2 method to get the best possible chi2 there.
3) Same, but at x0 _minus_ one error bar.

What is the relationship in chi2 between those three evaluations? 

# Exercise 5: Exclusion plots in 2D

(will add)
