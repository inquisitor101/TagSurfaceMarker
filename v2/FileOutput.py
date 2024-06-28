# Imported libraries/functions.
import os
import sys
import numpy as np
from pathlib import Path


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







