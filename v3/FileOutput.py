# Imported libraries/functions.
import os
import sys
import struct
import numpy as np
from pathlib import Path
from ElementUtility import IMIN, IMAX, JMIN, JMAX

# Function that writes the markers (of a single zone) as an ASCII file.
def ExportMarkerASCII(marker, nPoly, gridfile):

    # Name of output directory of the markers.
    dirMarker = "/marker/"

    # Get current working directory.
    cwd = os.getcwd()

    # Absolute path to marker folder.
    folder = cwd + dirMarker

    # Extract name of grid file exclusively, without the directory.
    bn = os.path.basename(gridfile)
   
    # Remove the extension of the file.
    fn = bn.split('.')[0]

    # Add the complete file name, with extension and directory.
    fn = cwd + dirMarker + "marker_" + fn + ".txt"

    # Create output directory, if it doesn't exist. Also, initialize its current file.
    file = Path(fn)
    file.parent.mkdir(parents=True, exist_ok=True)

    # Number of markers.
    nMarker = len(marker)
    
    # Open file for writing.
    with file.open('w') as f:
        # Number of markers in total.
        f.write(f"NMARK = {nMarker}\n")

        # Loop over the markers and write them separately.
        for i in range(nMarker):
            # Extract marker tag name.
            tag = marker[i][0]
            # Extract marker indices.
            ind = marker[i][1]

            # Number of nodes in 1D over an element.
            npts = int(nPoly+1)
            # Total number of nodes on this marker.
            ntot = len(ind)

            # Deduce number of elements on this marker.
            nElem = int( (ntot-1)/nPoly )

            # Consistency check.
            if (nElem*nPoly+1) != ntot:
                sys.exit("Inconsistent number of elements on a marker is detected.")

            # Write the name of the current marker tag.
            f.write(f"MARKER_TAG = {tag}\n")

            # Write total number of elements on this marker.
            # Note, in reality, these are the number of faces, not elements. This is 
            # because on corners, 2 faces belong to the same element. So, it is more
            # appropriate to call them faces.
            f.write(f"NFACE = {nElem}\n")

            # Loop over the nodes on the surface elements and write their indices.
            s = 0
            for j in range(nElem):
                for k in range(nPoly):
                    f.write(f"{ind[s+k]},")
                # Last entry is written here, such that there is not comma and a new line is added.
                f.write(f"{ind[s+nPoly]}\n")
                # Offset counter, since the solution is multiply defined at the internal faces.
                s += nPoly


# Function that writes an AS3 grid in binary format. The byte order uses little-endian.
def WriteAS3GridBinaryFormat(grid_as3, file_p3d):

    # Name of output directory for the AS3 grid.
    dirAS3 = "/grid_AS3/"

    # Get current working directory.
    cwd = os.getcwd()

    # Absolute path to the AS3 grid folder.
    folder = cwd + dirAS3

    # Extract name of grid file exclusively, without the directory.
    bn = os.path.basename(file_p3d)
   
    # Remove the extension of the file.
    fn = bn.split('.')[0]

    # Add the complete file name, with extension and directory.
    fn = cwd + dirAS3 + fn + ".as3"

    # Create output directory, if it doesn't exist. Also, initialize its current file.
    file = Path(fn)
    file.parent.mkdir(parents=True, exist_ok=True)


    # Ensure the grid arguments are the correct size.
    if len(grid_as3) != 5:
        sys.exit("Parameters of AS3 grid is wrong size.")

    # Get the data explicity in the grid.
    xx = grid_as3[0]
    yy = grid_as3[1]
    mm = grid_as3[2]
    nx = grid_as3[3]
    ny = grid_as3[4]

    # Length of strings used, using the CGNS convention.
    CGNS_STRING_SIZE = 33

    # AS3 file magic number.
    AS3_MAGIC_NUMBER = int( 3735929054 )

    # Dimension of the grid: 2D or 3D.
    dimgrid = int(2)

    # Number of total markers.
    nMarker = len(mm)

    # Total number of nodes in an element.
    nNode2D = xx.shape[1]

    # Consistency checks.
    if nNode2D != yy.shape[1]:
        sys.exit("Coordinates do not have the same polynomial order.")
    if nx*ny != xx.shape[0] or nx*ny != yy.shape[0]:
        sys.exit("Grid elements and coordinates are not of equal size.")


    # Open file for writing binary data using little endian (i.e. ">").
    with file.open('wb') as f:
       
        # Write the AS3 magic number.
        f.write( struct.pack( "<I", AS3_MAGIC_NUMBER ) )

        # Write the dimension of the grid: 2 for 2D, 3 for 3D.
        f.write( struct.pack( "<I", dimgrid ) )

        # Write the grid number of elements: nxElem, nyElem.
        f.write( struct.pack( "<2I", nx, ny ) )

        # Write the number of nodes in 2D for an element.
        f.write( struct.pack( "<I", nNode2D ) );

        # Write the x-coordinates.
        for i in range(len(xx)):
            f.write( struct.pack( "<{0}d".format(nNode2D), *xx[i,:] ) )

        # Write the y-coordinates.
        for i in range(len(yy)):
            f.write( struct.pack( "<{0}d".format(nNode2D), *yy[i,:] ) )

        # Write the local element indicial face convention for the markers.
        f.write( struct.pack( "<4I", IMIN, IMAX, JMIN, JMAX ) )

        # Write the number of markers available.
        f.write( struct.pack( "<I", nMarker ) )
        
        # Loop over each marker and write its information.
        for i in range(nMarker):

            # Marker tag name. Ensure its size is not greater than the max value.
            name = mm[i][0] 
            if len(name) > CGNS_STRING_SIZE:
                sys.exit( "Marker name is larger than " + str(CGNS_STRING_SIZE) + " characters." )

            # Write its name tag.
            f.write( struct.pack( "<{0}s".format(CGNS_STRING_SIZE), name.encode('utf-8') ) )

            # Extract the number of faces on this marker.
            nFace = len( mm[i][1] )

            # Write the number of faces on this marker.
            f.write( struct.pack( "<I", nFace ) )

            # Loop over its faces and write its information (iElem,iBoundary).
            for j in range(nFace):
                f.write( struct.pack( "<2I", mm[i][1][j][0], mm[i][1][j][1] ) )








