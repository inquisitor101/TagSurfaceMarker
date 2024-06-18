# Imported libraries/functions.
import os
import sys
import numpy as np
import FileIO
import Visualization


# Main function.
def main():

    # Check if the program is called correctly. 
    if len( sys.argv ) != 3:
        sys.exit( "Must input grid file as first argument, followed by number of boundary markers." )

    # Get input grid file.
    file = sys.argv[1]

    # Get number of markers specified.
    nMarker = int( sys.argv[2] )

    # Get current directory.
    cwd = os.getcwd()

    # Import the grid.
    x, y, z, I0, n = FileIO.ImportGridPlot3D(file)

    # Extract a single zone data.
    iZone = 0
    xx = x[ I0[iZone]:I0[iZone+1] ]
    yy = y[ I0[iZone]:I0[iZone+1] ] 
    nn = n[iZone]

    
    

    # Visualize data.
    marker = Visualization.DataInteraction(xx, yy, nn, nMarker)

    print("final marker tags: ", marker)

# Main function that drives the program.
if __name__ == '__main__':
    main()
