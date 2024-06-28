# Imported libraries/functions.
import os
import sys
import struct
import numpy as np


# Function that reads a (single zone) Plot3D binary grid file.
def ImportSingleZoneBinaryPlot3D(filename):
    
    # Number of bytes of int and double, as per written convention.
    nByteInt = int(4); nByteDouble = int(8)

    # Open and read all the binary data.
    with open(filename, mode='rb') as file:
        buffer = file.read()

    # Assume the default is little endian.
    endian = "little"; sym = "<"

    # Read first integer and ensure it is has the size of 4, since 1 int = 4 bytes, by written convention.
    if int.from_bytes( buffer[0:4], endian ) != nByteInt:
        endian = "big"; sym = ">"
        if int.from_bytes( buffer[0:4], endian ) != nByteInt:
            sys.exit("Could not read the file, unknown first value.")

    # Extract the header information about the grid.
    j = nByteInt; v = []
    for i in range(8):
        v.append( int.from_bytes( buffer[j:j+nByteInt], endian ) )
        j += nByteInt

    # First record is the number of blocks, must be one.
    if v[0] != 1:
        sys.exit("Number of blocks must be set to one (for now).")

    # Extract the number of points in all three dimensions. Ensure the z-dimension is trivial.
    nx = v[3]; ny = v[4]; nz = v[5]
    if nz != 1:
        sys.exit("Grid must be two-dimensional, only one point in the z-direction is expected.")

    # Determine the precision of the data.
    precision = int( v[-1]/(3*nx*ny*nz) )

    # For now, force only double precision.
    if precision != nByteDouble:
        sys.exit("Only double precision is supported.")

    # Total number of grid points expected.
    nPoint = int( nx*ny*nz )

    # Byte-reading format for double-precision.
    sym += str(nPoint) + "d"

    # Extract the remaining data. Starting from the x-coordinates.
    I0 = int(j); I1 = int(I0 + nPoint*nByteDouble)
    x = np.array( struct.unpack( sym, buffer[I0:I1] ) )

    # Then, the y-coordinates.
    J0 = I1; J1 = int(J0 + nPoint*nByteDouble)
    y = np.array( struct.unpack( sym, buffer[J0:J1] ) )

    # Lastly, the z-coordinates.
    K0 = J1; K1 = int(K0 + nPoint*nByteDouble)
    z = np.array( struct.unpack( sym, buffer[K0:K1] ) )
    
    # Consistency check, based on the last integer entry within the writing convention.
    if int.from_bytes(buffer[-4:-1], endian) != v[-1]:
        sys.exit("Last entry in file should correspond to the total bytes of the data.")
    
    # Array containing the information of the grid.
    info = np.array( (nx, ny, nz) ) 

    
    # Return the data.
    return x,y,z,info


# Function that returns the path to all grid files and the index of the input file.
def DetermineGridFiles(file):

    # Get the name of the input grid file exclusively.
    bn = os.path.basename(file)

    # Current working directory.
    cwd = os.getcwd()

    # Folder containing the grid files.
    dirGrid = os.path.dirname(file)
    
    # Path to grid zones.
    path = cwd + "/" + dirGrid + "/"
    
    # List of all grid zone files.
    zones = os.listdir( path )

    # Total number of zones/files.
    nZone = len(zones)

    # Index of the input grid zone.
    IDX = []

    # Ensure all grid directory has no directories, only files.
    for i in range(nZone):

        # Check if the item is indeed a file.
        if os.path.isfile( path+zones[i] ) == False:
            sys.exit("Grid directory contains non-files.")
        
        # Filter out the remaining zones, by excluding the input zone.
        if zones[i] == bn: IDX = i       
        
        # Prepend the absolute path.
        zones[i] = path + zones[i]

    # Ensure the input grid is detected.
    if not IDX:
        sys.exit("Could not detect input grid file.")

    # Return the zone files and the index of the input grid.
    return zones, IDX

