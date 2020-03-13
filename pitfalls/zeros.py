def decaycurvewithbackground(t,n0,lifetime,background):
	return n0*np.exp(-t/lifetime) + background

timepoints = array([ 0. ,  0.5,  1. ,  1.5,  2. ,  2.5,  3. ,  3.5,  4. ,  4.5,  5. ,
        5.5,  6. ,  6.5,  7. ,  7.5,  8. ,  8.5,  9. ,  9.5, 10. , 10.5,
       11. , 11.5, 12. , 12.5, 13. , 13.5, 14. , 14.5, 15. , 15.5, 16. ,
       16.5, 17. , 17.5, 18. , 18.5, 19. , 19.5])

data = array([34, 16, 13, 15, 12,  4,  8, 12,  8,  9,  7,  6,  6,  3,  2,  5,  1,
        3,  3,  1,  1,  2,  1,  3,  1,  1,  0,  2,  1,  0,  0,  2,  0,  0,
        1,  0,  0,  0,  0,  0])
