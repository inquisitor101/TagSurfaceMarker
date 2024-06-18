# Imported libraries/functions.
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor
from matplotlib.widgets import TextBox




# Function that plots and interacts with data.
def DataInteraction(x, y, n, nMarker):

    # Extract number of points in x and y.
    nx = n[0]
    ny = n[1]

    # Deduce the boundary indices, based on clockwise conveniton.
    surfaceIndices = SurfaceIndicesClockwise( nx, ny )

    # Initialize the marker data.
    marker = [] 

    # Starting index of each face selection. Will get overriden, dont worry.
    I0 = int(0) 
    
    # Counter for the number of points selected.
    nPointPressed = 0   

    def onpick(event):
        # Non-local and global variables.
        nonlocal nPointPressed
        nonlocal I0

        # Get the index of the points chosen.
        ind = event.ind

        # Points selected must be one.
        if len(ind) != 1:
            return
        
        #print("number of points pressed: ", nPointPressed)
        #print("event.ind: ", ind, ", with coordinates: ", x[ind], y[ind])
        ax.plot(x[ind], y[ind], 'o', markerfacecolor='none', color='red', linewidth=2, markersize=5)
        plt.draw() 

        # Increment the number of points pressed.
        nPointPressed += 1
        
        # Distinguish between starting/ending indices.
        if nPointPressed % 2 == 0:
           
            # Extract the indices of the points on this marker.
            ij = FindIndicesLineClockwise(I0, ind, nx, ny, surfaceIndices)

            # Plot the connecting line between the two indices.
            plt.plot(x[ij],y[ij], color='green')
            
            # Ask the user for an explicit marker tag name.
            #name = input("Enter Marker name tag: ")
            
            # TESTING
            name = []
            waiting = True
            def submit(expression):
                nonlocal name
                name = expression
                print("waiting in submit...")
                
            def on_press_waiting(button):
                nonlocal waiting
                print("button.key: ", button.key)
                if button.key == 'x':
                    waiting = False
                    return


            fig.canvas.mpl_connect('key_press_event', on_press_waiting)

            if waiting == False:
                axbox = fig.add_axes([0.1, 0.05, 0.8, 0.075])
                text_box = TextBox(axbox, "Marker name: ", textalignment="center")
                text_box.on_submit(submit)
                text_box.set_val("Unknown")  # Trigger `submit` with the initial string.
                print("completed.")
            # TESTING

            # Book-keep marker information.
            marker.append([name, I0, ind])

            print("markers: ", marker)

            # Remove last entry point.
            #pts.remove()
            #pts.pop(0).remove()

            # Extract the plots from the figure and remove the starting and ending points.
            pts = ax.get_lines()
            pts[-3].remove() # start point
            pts[-2].remove() # end   point


            # Change the color of the most recent connecting line.
            pts[-1].set_color("gray")
            
            #fig,ax = plt.gca()
            #ax.set_title("asd")
            #print( len(plots) )

        else:
            # Save the starting index.
            I0 = ind

       
        # Expected marker information is complete, close the figure.
        if len(marker) == nMarker:
            plt.close()
            print("markers should be complete.")
            

        #print( "len(ind): ", len(ind) )

        #if len(ind) > 1:
        #    datax,datay = event.artist.get_data()
        #    datax,datay = [datax[i] for i in ind],[datay[i] for i in ind]
        #    msx, msy = event.mouseevent.xdata, event.mouseevent.ydata
        #    dist = np.sqrt((np.array(datax)-msx)**2+(np.array(datay)-msy)**2)
        #    ind = [ind[np.argmin(dist)]]
        #s = event.artist.get_gid()
        #print( s, ind )
    
    fig, ax = plt.subplots()
    ax.plot(x, y, '^', picker=True)
    
    fig.canvas.mpl_connect("pick_event", onpick)

    # Make the figure full screen, for convenience.
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    
    cursor = Cursor(ax, useblit=True, color='gray', linewidth=2, ls=':')
           
    plt.show()
    
    return marker



# Function that returns the indices on all surfaces, based on a clockwise convention.
def SurfaceIndicesClockwise(nx, ny):

    # Total number of indices on a boundary.
    ns = 2*nx + 2*ny - 4;

    # Create the indices for all boundaries first.
    boundary = np.zeros( ns, dtype=int )

    # Counter for boundary indices.
    s = 0


    # The following is based on the convention of a Plot3D file.
    # The indices are using clockwise format.
    
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


# Function that determines the indices for the line from I0 to I1, 
# based on the clockwise direction.
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






