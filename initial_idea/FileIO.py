# Imported libraries/functions.
import sys
import numpy as np
import Util



# Function that reads a Plot3D grid file.
def ImportGridPlot3D(file):

    # Open file to start extracting the data.
    with open(file, 'r') as grid:

        # First integer is the number of blocks.
        nBlock = grid.readline().split() 

        # Ensure number of blocks is a single value.
        if( len(nBlock) != 1 ):
            sys.exit( "Wront nBlock detected." )
        
        # Convert it to an integer type.
        nBlock = int( nBlock[0] )

        # Create a numpy of type int for the number of points per block.
        nPoint = np.zeros( (nBlock, 3), dtype = int )

        # Read the next nBlocks with their number of points in x,y,z.
        for i in range(nBlock):

            # Extract line, with end character.
            info = grid.readline()

            # Check if end of file is reached.
            if len(info) == 0:
                sys.exit( "Error, end of file reached unexpectedly." )

            # Extract information, by skipping white spaces and end line characters.
            info = info.split()

            # Check number of arguments is three.
            if( len(info) != 3):
                sys.exit( "Number of points per block must be 3." );

            # Extract number of points per block.
            nPoint[i][0] = int( info[0] )
            nPoint[i][1] = int( info[1] )
            nPoint[i][2] = int( info[2] )


        # Deduce size of 1D array of all information per dimension.
        IDX = Util.Indices1DArrayFrom3D(nPoint)

        # Allocate memory for the coordinates in all the blocks.
        x = np.zeros( IDX[-1], dtype=float )
        y = np.zeros( IDX[-1], dtype=float )
        z = np.zeros( IDX[-1], dtype=float )
 
        tmp = []
        for b in range(nBlock):

            # Explicitly write the number of points.
            nx = nPoint[b][0]
            ny = nPoint[b][1]
            nz = nPoint[b][2]

            # Total number of points.
            n = nx*ny*nz 
            
            # Allocate memory for the coordinates in this block.
            xyz = np.zeros( (3, n) )


            # Starting index for the x-coordinates.
            s = IDX[b]


            # Read in the coordinates, from x to z.
            for k in range(nz):
                for j in range(ny):
                   
                    # Read line.
                    buffer = grid.readline().split()
                    
                    if( len(buffer) != nx ):
                        sys.exit( "Wrong number of points in the i-direction detected." )
                        
                    for i in range(nx):
                        x[s] = float( buffer[i] )
                        s += 1

            # Check index is correct for the y-coordinates. Then, reset it.
            if( s != n+IDX[b] ):
                sys.exit( "Starting index for the y-coordinates is wrong" )
            else:
                s = IDX[b]

            # Read in the coordinates, from x to z.
            for k in range(nz):
                for j in range(ny):
                    
                    # Read line.
                    buffer = grid.readline().split()
                    
                    if( len(buffer) != nx ):
                        sys.exit( "Wrong number of points in the j-direction detected." )
                        
                    for i in range(nx):
                        y[s] = float( buffer[i] )
                        s += 1
            
            # Check index is correct for the z-coordinates. Then, reset it.
            if( s != n+IDX[b] ):
                sys.exit( "Starting index for the z-coordinates is wrong" )
            else:
                s = IDX[b]

            # Read in the coordinates, from x to z.
            for k in range(nz):
                for j in range(ny):
                    
                    # Read line.
                    buffer = grid.readline().split()
                    
                    if( len(buffer) != nx ):
                        sys.exit( "Wrong number of points in the k-direction detected." )
                        
                    for i in range(nx):
                        z[s] = float( buffer[i] )
                        s += 1
            
        # Return values with array size indices.
        return x, y, z, IDX, nPoint


