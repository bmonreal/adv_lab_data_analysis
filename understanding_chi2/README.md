# Understanding the chi2 test statistic

Please check out the code [[chi2.py]] in this directory.  Scroll through it and READ THE COMMENTS. Fire up your favorite Python interpreter and run this code, which should spit out a multipanel plot walking you through the comparison of some data (with fluctuations) to a fit function (without fluctuations). 

Then write your own code, `my_chi2.py`, which does the following exercises.  If possible, generate and save a three-panel plot with a nice visualization of the three answers.  Make sure the code my_chi2.py (and the plot!) are put under version control and pushed to GitHub.

# Exercise 1:
Copy the block of code that generates `fake_exp_y_values` into your code. 

Write a function that calculates chi2 given (a) the data array, (b) the theory array, and (c) the error bar array.

1) Run 1000 iterations of the fake-data-generation and chi2-calculation, and plot a histogram of all the chi2 values that come out.
2) Get the data from the histogram into an array for analysis (slightly tricky!)
	1) Find the mean chi2 value.
	2) Find the chi2 value for which only 31% of the trials fluctuated higher.
	2) Find the chi2 value for which only 4.5% of the trials fluctuated higher.

# Exercise 2: chi2 goes down when you have free parameters
In the previous exercise, you took the `exact_y_values` array as the thing you would compare to the real data.  This time you will do a fit using using scipy.optimize.curve_fit().

1) Run 1000 iterations of the fake-data-generation.  For each iteration, do a fit for the best values of the mean, amp, width, and offset.  (You may use the known values as your starting guess.)  Use the best-fit-curve to calculate chi2, and plot a histogram of all the chi2 values that come out.
2) Show that the chi2 values are systematically lower.  This is expected because the "number of degrees of freedom" is smaller here by -4.

# Exercise 3: Robustness of chi2

Repeat exercise 1 and tell me whether the chi2 statistic is robust (i.e., whether the histogram looks roughly the same) if:

1) the data points don't have Poisson errors, they "digital" fluctuations: with equal probability, add -1, 0, or +1 to each data point.  (The "error bar" on this is +/-1, just like a Gaussian random fluctuation.)

2) before analysis, the "worst" two data points are removed from the dataset

3) rather than reporting the chi2 of the dataset, you always run three experiments and report only the best of the three.
