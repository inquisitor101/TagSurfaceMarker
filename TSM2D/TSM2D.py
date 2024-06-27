# Imported libraries/functions.
import os
import sys
import numpy as np
import FileInput as fi
import FileOutput as fo
import Visualization as vis


# Main function.
def main():

    # Check if the program is called correctly. 
    if len( sys.argv ) != 4:
        sys.exit( "Usage: <grid file> <polynomial order> <number of boundary markers>" ) 

    # Get input grid file.
    file = sys.argv[1]

    # Get the polynomial order of the grid.
    nPoly = int( sys.argv[2] )

    # Get number of markers specified.
    nMarker = int( sys.argv[3] )

    # Import a zone.
    data = fi.ImportSingZoneBinaryPlot3D(file)

    # Visualize the data and apply the boundary markers.
    marker = vis.InteractiveMarker(data, nMarker, file, nPoly)

    # Write the marker data to an ASCII file.
    fo.ExportMarkerASCII(marker, nPoly, file)



# Main function that drives the program.
if __name__ == '__main__':
    main()
