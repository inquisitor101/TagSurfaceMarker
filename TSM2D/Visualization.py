# Imported libraries/functions.
import sys
import math
import numpy as np
import GeometryUtility as geo
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor
from matplotlib.widgets import TextBox



# Function that enables visual interaction with data to tag boundary markers.
def InteractiveMarker(data, nMarker, file, nPoly):

    # Extract the data variables, explicitly.
    x = data[0]
    y = data[1]
    z = data[2]
    n = data[3]

    # Extract the number of points per dimension. Ensure the z-dimension is trivial.
    nx = n[0]; ny = n[1]; nz = n[2]
    if nz != 1:
        sys.exit("Grid must be two-dimensional, only a single point in the z-coordinates is expected.")


    # All surface indices of this grid.
    surf = geo.SurfaceIndicesClockwise(nx, ny)

    # Initialize the marker data.
    marker = [] 

    # Starting index of each face selection. Will get overriden, dont worry.
    I0 = int(0) 
    
    # Counter for the number of points selected.
    nPointPressed = 0   

    # The actual implementation.
    def onpick(event):
        nonlocal I0, nPointPressed
    
        # Get the index of the points chosen.
        ind = event.ind
    
        # Points selected must be one.
        if len(ind) != 1:
            return
       
        # Show selected point.
        ax.plot(x[ind], y[ind], 'o', markerfacecolor='none', color='red', linewidth=2, markersize=5)
        plt.draw() 
    
        # Increment the number of points pressed.
        nPointPressed += 1
        
        # Distinguish between starting/ending indices.
        if nPointPressed % 2 == 0:
           
            # Extract the indices of the points on this marker.
            ij = geo.FindIndicesLineClockwise(I0, ind, nx, ny, surf)
    
            # Plot the connecting line between the two indices.
            ax.plot(x[ij], y[ij], color='green')
            
            # Ask the user for an explicit marker tag name.
            name = []
            def submit(expression):
                nonlocal name
                name = expression
            
            # Visual submit detection.
            text_box.on_submit(submit)
          
            # Check for user input.
            while len(name) == 0:
                plt.pause(0.1)
    
            # Book-keep marker information.
            marker.append( [name, ij] )

            # Extract the plots from the figure and remove the starting and ending points.
            pts = ax.get_lines()
            pts[-3].remove() # start point
            pts[-2].remove() # end   point
    
            # Change the color of the most recent connecting line.
            pts[-1].set_color("gray")
            
        else:
            # Save the starting index.
            I0 = ind
       
        # Expected marker information is complete, close the figure.
        if len(marker) == nMarker:
            plt.close()
 
    # End of the interaction implementation.


    # Plot grid.
    fig, ax = plt.subplots()
    ax.plot(x, y, '^', picker=True)
   
    # Show the elements, for convenience.
    ShowElementsGrid(x,y,nx,ny,nPoly)

    # Title of figure.
    ax.set_title( "Marker tag selector for grid file: " + str(file) )
    
    # Pick event, for user interaction with data.
    fig.canvas.mpl_connect("pick_event", onpick)

    # Make the figure full screen, for convenience.
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    
    # For convenience in point selection, mouse cursor.
    cursor = Cursor(ax, useblit=True, color='gray', linewidth=2, ls=':')
    
    # Text box for user input marker name tags.
    axbox    = fig.add_axes([0.2125, 0.025, 0.6, 0.05])
    text_box = TextBox(axbox, "Marker name: ", textalignment="center",initial="Unknown") 

    # Update the plot.
    plt.show()

    # Ensure the markers are as expected.
    if len(marker) != nMarker:
        sys.exit("Could not assign the expected number of markers.")

    # Ensure the entire boundary is included in the markers, i.e. no missing points.
    if geo.MarkersContainEntireBoundary(marker, nx, ny) != True:
        sys.exit("Some boundary points are not included in the markers.")

    # Return the marker data.
    return marker


# Function that shows the elements separately, on the figure.
def ShowElementsGrid(x,y,nx,ny,nPoly):

    # Number of nodes per element in 1D.
    nNode = int(nPoly+1)

    # Ensure the elements are indeed of the specified order.
    nxElem = math.ceil( ( math.ceil(nx/nNode) + nx )/nNode )
    nyElem = math.ceil( ( math.ceil(ny/nNode) + ny )/nNode )

    # Consistency check.
    if (nxElem*nPoly+1) != nx:
        sys.exit("Could not estimate the number of high-order elements in x.")
    if (nyElem*nPoly+1) != ny:
        sys.exit("Could not estimate the number of high-order elements in y.")

    # Deduce the number of nodes, based on nPoly=1 elements.
    nxP1 = nxElem + 1
    nyP1 = nyElem + 1

    # Initialize coordinates of the P1 nodes.
    xP1 = np.zeros( (nxP1,nyP1), dtype=float )
    yP1 = np.zeros( (nxP1,nyP1), dtype=float )

    # Extract the coordinates of the P1 nodes.
    for j in range(nyP1):
        ij = j*nPoly*nx 
        for i in range(nxP1):
            xP1[i,j] = x[ij]
            yP1[i,j] = y[ij] 
            ij += nPoly
    
    # Plot the elements.
    for i in range(nxP1):
        plt.plot(xP1[i,:], yP1[i,:], 'k:')
    for j in range(nyP1):
        plt.plot(xP1[:,j], yP1[:,j], 'k:')

