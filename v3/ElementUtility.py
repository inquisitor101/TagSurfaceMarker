# Imported libraries/functions.
import os
import sys
import math
import numpy as np


# Global variables for IMIN, IMAX, JMIN, JMAX nodal indices in an element.
IMIN = int(0)
IMAX = int(1)
JMIN = int(2)
JMAX = int(3)


# Function that returns number of elements in 1D from number of points, given a polynomial order.
def DetermineNumberOfElements(nPoints, nPoly):

    # Number of nodes in 1D over a single element.
    nNode = int(nPoly+1)

    # Estimate the number of elements.
    nElem = int( (nPoints-1)/nPoly )

    # Check if the estimate is correct.
    if (nElem*nPoly+1) != nPoints:
        sys.exit("Could not estimate the number of high-order elements.")

    # Return the number of elements.
    return nElem



# Function that converts the grid format from Plot3D to AS3.
def ConvertGridFromPlot3DToAS3(data, marker_p3d, nPoly, file):

    # Extract the data variables, explicitly.
    x_p3d = data[0]
    y_p3d = data[1]
    n_p3d = data[3]

    # Extract the number of points per dimension.
    nx = n_p3d[0]; ny = n_p3d[1]

    # Number of nodes per element in 1D and 2D.
    nNode1D = int(nPoly+1)
    nNode2D = nNode1D*nNode1D

    # Deduce number of elements.
    nxElem = DetermineNumberOfElements(nx, nPoly) 
    nyElem = DetermineNumberOfElements(ny, nPoly) 

    # Total number of elements.
    nElem  = nxElem*nyElem
    
    # Initialize the connectivity matrix.
    C = np.zeros( nNode2D, dtype=int )
    
    # For the connectivity matrix, function of nPoly.
    k = 0
    for j in range(nNode1D):
        for i in range(nNode1D):
            C[k] = i - j*nx 
            k += 1

    # Initialize indices of elements, based on AS3 format.
    D_p3d_to_as3 = np.zeros( (nElem, nNode2D), dtype=int )

    # Initialize coordinates of elements in AS3 format.
    x_as3 = np.zeros( (nElem, nNode2D), dtype=float )
    y_as3 = np.zeros( (nElem, nNode2D), dtype=float )
    
    s = 0
    for j in range(nyElem):
        # Deduce the next starting point in the j-directoin.
        I0 = int( (ny - j*nPoly)*nx - nx )
        for i in range(nxElem):
            for k in range(nNode2D):
                
                # Element indices.
                D_p3d_to_as3[s, k] = I0 + C[k]
                # Coordinates.
                x_as3[s, k] = x_p3d[ D_p3d_to_as3[s,k] ]
                y_as3[s, k] = y_p3d[ D_p3d_to_as3[s,k] ]

            # Increment element index.
            s += 1
            # Deduce the next starting point in the i-direction.
            I0 += nPoly
    
    # Determine the equivalent AS3 format for the Plot3D markers.
    marker_as3 = ConvertMarkerFromPlot3DToAS3(marker_p3d, D_p3d_to_as3, nxElem, nyElem, nPoly)

    # Return the grid data in AS3 format.
    return x_as3, y_as3, marker_as3, nxElem, nyElem



# Function that converts the Plot3D marker into an AS3 marker, based on elements.
def ConvertMarkerFromPlot3DToAS3(marker_p3d, elements, nxElem, nyElem, nPoly):

    # Number of markers.
    nMarker = len(marker_p3d)

    # Number of nodes in 1D over an element.
    nNode   = int(nPoly+1)

    # Initialize the AS3 marker information.
    marker_as3 = []

    # Loop over the markers and identify their elements.
    for i in range(nMarker):
      
        # Abbreviation for the current marker name tag.
        name  = marker_p3d[i][0]

        # Abbreviation for current marker indices.
        m_ps3 = marker_p3d[i][1]

        # Determine number of points on this marker.
        npts = len(m_ps3)

        # Deduce the equivalent number of faces on this marker.
        nFace = DetermineNumberOfElements(npts, nPoly) 

        # Allocate the AS3 face marker information.
        face_as3 = np.zeros( (nFace, 2), dtype=int )

        # Loop over every face and correlate its element.
        for j in range(nFace):

            # Starting index of current face marker.
            I0 = j*nPoly

            # Explicitly form the element face marker indices.
            v  = np.array( m_ps3[I0:I0+nNode] )

            # Check if this tag belongs to face: IMIN.
            imin = CheckMarkerElementIMIN( elements, nxElem, nyElem, nPoly, v ) 
            if imin:
                # Assign face marker value.
                face_as3[j] = imin
                # Skip remaining iterations in this loop.
                continue 
            
            # Check if this belongs to face: IMAX.
            imax = CheckMarkerElementIMAX( elements, nxElem, nyElem, nPoly, v ) 
            if imax:
                # Assign face marker value.
                face_as3[j] = imax
                # Skip remaining iterations in this loop.
                continue 

            # Check if this belongs to face: JMIN.
            jmin = CheckMarkerElementJMIN( elements, nxElem, nyElem, nPoly, v ) 
            if jmin:
                # Assign face marker value.
                face_as3[j] = jmin
                # Skip remaining iterations in this loop.
                continue 

            # Check if this belonds to face: JMAX.
            jmax = CheckMarkerElementJMAX( elements, nxElem, nyElem, nPoly, v ) 
            if jmax:
                # Assign face marker value.
                face_as3[j] = jmax
                # Skip remaining iterations in this loop.
                continue 

            # If the code reaches this far, it means something is wrong: issue and error.
            sys.exit("Marker could not be converted from Plot3D to AS3.")

        # Append the AS3 marker information for this face.
        marker_as3.append( [name, face_as3] )

    # Return the marker indices, using AS3 format.
    return marker_as3 


# Function that processes whether a marker belongs to a boundary: JMIN. 
def CheckMarkerElementJMIN(elements, nxElem, nyElem, nPoly, m):

    # Face tag.
    tag = JMIN

    # Start and stop element indices. NOTE, start is inclusive, end is exclusive.
    I0 = int(0)
    I1 = int(nxElem)

    # Form the element indices.
    elem_idx = np.arange(I0, I1, dtype=int)

    # Start and stop nodal indices. NOTE, start is inclusive, end is exclusive.
    I0 = int(nPoly)
    I1 = int(-1)

    # Form the clockwise local nodal indices.
    node_idx = np.arange(I0, I1, -1, dtype=int )

    # Number of nodes in 1D.
    nNode = int(nPoly+1)

    # Search for the indices, if they can be found.
    info = FindElementMarker(elements, elem_idx, node_idx, m, tag)

    # Return the information if found, otherwise its an empty list. 
    return info
               

# Function that processes whether a marker belongs to a boundary: JMAX. 
def CheckMarkerElementJMAX(elements, nxElem, nyElem, nPoly, m):

    # Face tag.
    tag = JMAX

    # Start and stop element indices. NOTE, start is inclusive, end is exclusive.
    I0 = int(nxElem*nyElem-nxElem )
    I1 = int(nxElem*nyElem)

    # Form the element indices.
    elem_idx = np.arange(I0, I1, dtype=int)

    # Number of nodes in 1D and 2D.
    nNode1D = int(nPoly+1)
    nNode2D = nNode1D*nNode1D
    
    # Start and end nodal indices. NOTE, start is inclusive, end is exclusive.
    I0 = int(nNode2D-nNode1D)
    I1 = int(nNode2D)

    # Form the clockwise local nodal indices.
    node_idx = np.arange(I0, I1, dtype=int )

    # Search for the indices, if they can be found.
    info = FindElementMarker(elements, elem_idx, node_idx, m, tag)

    # Return the information if found, otherwise its an empty list. 
    return info


# Function that processes whether a marker belongs to a boundary: IMAX. 
def CheckMarkerElementIMAX(elements, nxElem, nyElem, nPoly, m):

    # Face tag.
    tag = IMAX

    # Start and stop element indices. NOTE, start is inclusive, end is exclusive.
    I0 = int(nxElem-1)
    I1 = int(nxElem*nyElem)

    # Form the element indices.
    elem_idx = np.arange(I0, I1, nxElem, dtype=int)

    # Number of nodes in 1D and 2D.
    nNode1D = int(nPoly+1)
    nNode2D = nNode1D*nNode1D
    
    # Start and stop nodal indices. NOTE, start is inclusive, end is exclusive.
    I0 = int(nNode2D-1)
    I1 = int(nPoly-1)

    # Form the clockwise local nodal indices.
    node_idx = np.arange(I0, I1, -nNode1D, dtype=int )

    # Search for the indices, if they can be found.
    info = FindElementMarker(elements, elem_idx, node_idx, m, tag)

    # Return the information if found, otherwise its an empty list. 
    return info
   

# Function that processes whether a marker belongs to a boundary: IMIN. 
def CheckMarkerElementIMIN(elements, nxElem, nyElem, nPoly, m):
    
    # Face tag.
    tag = IMIN

    # Start and stop element indices. NOTE, start is inclusive, end is exclusive.
    I0 = int(0)
    I1 = int(nxElem*nyElem-nxElem+1)

    # Form the element indices.
    elem_idx = np.arange(I0, I1, nxElem, dtype=int)

    # Number of nodes in 1D and 2D.
    nNode1D = int(nPoly+1)
    nNode2D = nNode1D*nNode1D
    
    # Start and end nodal indices. NOTE, start is inclusive, end is exclusive.
    I0 = int(0)
    I1 = int(nNode2D-nNode1D+1)

    # Form the clockwise local nodal indices.
    node_idx = np.arange(I0, I1, nNode1D, dtype=int )

    # Search for the indices, if they can be found.
    info = FindElementMarker(elements, elem_idx, node_idx, m, tag)

    # Return the information if found, otherwise its an empty list. 
    return info
 

# Function that returns the info of the element belonging to a marker, if found.
def FindElementMarker(elements, elem_idx, node_idx, m, tag):

    # Loop over all element indices and check if input marker is on input side.
    for i in elem_idx:
        if elements[i][node_idx[0]] == m[0]:
            if np.array_equal( elements[i][node_idx], m ):
                return [i,tag] 
            else:
                sys.exit("Nodal indices are incorrect, check clockwise convention.")

    # Marker does not belong to the current boundary, return an emtpy list.
    return []



