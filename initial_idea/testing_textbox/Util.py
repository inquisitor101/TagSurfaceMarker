# Imported libraries/functions.
import numpy as np


# Function that returns the indices of a 3D array of 2D arrays of varying size.
def Indices1DArrayFrom3D(n):

    # Extract dimensions.
    nArray = len(n)
    
    I0 = np.zeros( nArray+1, dtype=int )
    for i in range(nArray):

        tmp = 1
        for j in range( len(n[0]) ):
            tmp *= n[i][j]

        I0[i+1] = I0[i] + tmp

    return I0
