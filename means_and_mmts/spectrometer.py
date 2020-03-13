'''
Spectrometer data for analysis

The spectrometer reports data in "pixels" ("the spectral line is centered
on Pixel Number 1043" for example.))

The calibration procedure gives you a constant C such that:

wavelength = pixel_number/C
'''

# calibration constant measured at 11:55
C0 = 4.87052

# results, in pixels, of 30 five-minute runs from 12:00 to 2:30

array([3050.625299  , 3050.5716135 , 3050.57443349, 3050.58456106,
       3050.58506468, 3050.5355407 , 3050.55156444, 3050.46639054,
       3050.49527075, 3050.45896641, 3050.42196708, 3050.39065337,
       3050.37932101, 3050.31912267, 3050.30228834, 3050.26154572,
       3050.17310133, 3050.13821682, 3050.09134651, 3050.02361094,
       3049.98759453, 3049.97093948, 3049.89926661, 3049.86881862,
       3049.82807496, 3049.76572713, 3049.71390768, 3049.67835994,
       3049.64947573, 3049.60446763])

# calibration constant measured at 2:35AM
C1 = 4.86894

