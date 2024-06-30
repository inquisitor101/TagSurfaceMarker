# Imported libraries/functions.
import sys 
import numpy as np



# Function that returns the indices on all surfaces, based on a clockwise convention.
def SurfaceIndicesClockwise(nx, ny):

    # Total number of (unique) indices on the entire boundary.
    ns = 2*nx + 2*ny - 4;

    # Create the indices for all boundaries first.
    boundary = np.zeros( ns, dtype=int )

    # Counter for boundary indices.
    s = 0

    # The following is based on the convention of a Plot3D file.
    # The indices are using the clockwise convention. 
    # NOTE, they also assume that the indices:
    # [0]       : top-left corner.
    # [nx]      : top-right corner.
    # [nx*ny]   : bottom-right corner.
    # [nx*ny-nx]: bottom-left corner.
    
    # JMAX surface.
    for i in range(nx):
        boundary[s] = i 
        s += 1
    
    # IMAX boundary, exclude the first index since it is included in JMAX.
    for j in range(1, ny-1):
        boundary[s] = j*nx + nx - 1 
        s += 1
    
    # JMIN surface, exclude the first indix since it is included in IMAX.
    for i in range(1, nx):
        boundary[s] = nx*ny - i 
        s += 1
    
    # IMIN boundary, exclude the first and last indices since they are included in IMAX/IMIN.
    for j in range(ny-1, 0, -1):
        boundary[s] = j*nx 
        s += 1

    # Return the boundary indices.
    return boundary


# Function that returns the indices for the line from I0 to I1, based on the clockwise direction.
def FindIndicesLineClockwise(I0, I1, nx, ny, boundary):

    # Make the boundary indices periodic, in case a marker has nodes 
    # in the beginning and ending of the boundary array.
    B = boundary
    B = np.append(B, B)

    # Starting index.
    iStartList = np.where( B == I0 )
    iEndList   = np.where( B == I1 )
    
    # Take the first location of iStart and iEnd.
    iStart = iStartList[0][0]
    iEnd   = iEndList[0][0]

    # Take the periodicity of the indices into account, if needed.
    if iStart > iEnd:
        iEnd = iEndList[0][1]

    # Determine the size of the indices on this marker.
    ns = iEnd - iStart + 1

    # Initialize the array of indices of this marker.
    marker = np.zeros( ns, dtype=int )

    # Deduce the indicial values.
    s = 0
    for i in range(iStart, iEnd+1):
        marker[s] = B[i]
        s += 1
     
    # Return the list of indices on this marker.
    return marker


# Function that returns true/false on whether the entire boundary is included in markers.
def MarkersContainEntireBoundary(marker, nx, ny):
    
    # Default error flag.
    found = True

    # Number of markers.
    nMarker = len(marker)

    # Extract the surface marker indices over entire grid.
    S0 = SurfaceIndicesClockwise(nx, ny)
    
    # Number of surface points on the grid.
    ns = len(S0)

    # Make the boundary indices periodic, similar to the trick above in FindIndicesLineClockwise.
    S = np.append(S0, S0)

    # Initialize an array of size boundary indices and with zero values.
    v = np.zeros( nx*ny, dtype=int )

    # Loop over all the marker indices and process data.
    for i in range(nMarker):
 
        # For simplicity, abbreviate the current marker indices.
        m = marker[i][1]       

        # Find the index of the first marker point. Recall, the indices are clockwise.
        I0 = np.where( S == m[0] )

        # Consistency check.
        if len(I0) != 1 or len(I0[0]) != 2: found = False

        # Always take the first value, since periodicity is already accounted for.
        I0 = I0[0][0]

        # Extract the number of indices on this marker.
        for j in range( len(m) ):
            
            # Increment this index by one, since it is on a marker.
            v[m[j]] += 1 
             
            # Check that the points are in the clockwise convention.
            if m[j] != S[I0+j]: found = False
  
    # Not the most efficient memory-wise, but it sure is simply for now.
    v = v[S0]

    # Ensure all boundary indices are tagged.
    t = np.where( v == 0 )
    if len(t)  != 1 or len(t[0])  != 0:          found = False
    t = np.where( v == 1 )
    if len(t)  != 1 or len(t[0])  != ns-nMarker: found = False
    t = np.where( v == 2 )
    if len(t)  != 1 or len(t[0])  != nMarker:    found = False
    if v.min() != 1 or v.max() != 2:             found = False

    # All went well.
    return found










