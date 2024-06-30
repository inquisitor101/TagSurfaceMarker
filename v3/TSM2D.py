# Imported libraries/functions.
import os
import sys
import numpy as np
import FileInput as fi
import FileOutput as fo
import Visualization as vis
import ElementUtility as dgfem


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

    # Obtain all grid files and index of input file.
    zoneFiles = fi.DetermineGridFiles(file)

    # Determine number of grid zones detected.
    nZone = len(zoneFiles[0])

    # Import all the zones, one at a time.
    data = []
    for i in range(nZone):
        data.append( fi.ImportSingleZoneBinaryPlot3D(zoneFiles[0][i]) )


    # Visualize the data and apply the boundary markers.
    marker_p3d = vis.InteractiveMarker( data, nMarker, file, nPoly, zoneFiles[1] )

    # Write the marker data to an ASCII file.
    fo.ExportMarkerASCII( marker_p3d, nPoly, file )

    # Convert input grid from Plot3D to AS3 format, inclusive of markers.
    grid_as3 = dgfem.ConvertGridFromPlot3DToAS3( data[zoneFiles[1]], marker_p3d, nPoly, file )

    # Write the AS3 grid file in binary format, including its markers.
    fo.WriteAS3GridBinaryFormat( grid_as3, file )


# Main function that drives the program.
if __name__ == '__main__':
    main()
