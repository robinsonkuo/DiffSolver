import numpy as np
import copy
import time

""" Assuming vacuum boundary conditions in bottom/left faces and reflecting in top/right faces"""

def diffSolver(IDI):
    materials = IDI.materials
    source = IDI.getSource()
    xdim = IDI.xdim
    ydim = IDI.ydim
    xnum = IDI.x
    ynum = IDI.y
    rel_error = IDI.getRelError()
    # Create uniform source vector.
    Svector = [source for x in xrange((xnum+1)*(ynum+1))]
    
    print "Building the matrix..."
    # Create the Amatrix, set everything to 0 first. Indexed by rows then columns
    Amatrix = [[0 for b in xrange((xnum+1)*(ynum+1))] for a in xrange((xnum+1)*(ynum+1))]
    """ 
    Amatrix is indexed such that the row that influences cell x,y is row x+y*x 
    Within a row for cell x,y, the influence of cell i,j on cell x,y is column i+i*j
    So the effect of flux by cell i,j on cell x,y is in the Amatrix entry [x+y*x][i+i*j]
    """
    # First  consider the non-boundary cases
    for x in xrange(1,xnum):
        for y in xrange(1,ynum):
            Lx = x-1
            Rx = x+1
            Dy = y-1
            Uy = y+1
            mat00 = IDI.getCellMaterialData(x,y)
            mat10 = IDI.getCellMaterialData(x+1,y)
            mat01 = IDI.getCellMaterialData(x,y+1)
            mat11 = IDI.getCellMaterialData(x+1,y+1)
            a_L = -(mat00[0]+mat01[0])*ydim/(2*xdim)
            a_R = -(mat10[0]+mat11[0])*ydim/(2*xdim)
            a_B = -(mat00[0]+mat10[0])*xdim/(2*ydim)
            a_T = -(mat01[0]+mat11[0])*xdim/(2*ydim)
            sigma = xdim*ydim*(mat00[1]+mat10[1]+mat01[1]+mat11[1])/4
            a_C = sigma - (a_L + a_R + a_B + a_T)
            setMatrix(Amatrix, x, y, Lx, y, a_L, xnum)
            setMatrix(Amatrix, x, y, Rx, y, a_R, xnum)
            setMatrix(Amatrix, x, y, x, Dy, a_B, xnum)
            setMatrix(Amatrix, x, y, x, Uy, a_T, xnum)
            setMatrix(Amatrix, x, y, x, y, a_C, xnum)
    # Now left boundary condition (vacuum), modifying Svector as needed
    x = 0
    for y in xrange(1, ynum):
        Rx = x+1
        Dy = y-1
        Uy = y+1
        mat00 = IDI.getCellMaterialData(1,y)
        mat01 = IDI.getCellMaterialData(1,y+1)
        a_L = -(mat00[0]+mat01[0])*ydim/(2*xdim)
        a_R = a_L
        a_B = -mat00[0]*xdim/(2*ydim)
        a_T = -mat01[0]*xdim/(2*ydim)
        sigma = xdim*ydim*(mat00[1]+mat01[1])/4
        Svector[x+y*(xnum + 1)] = source/2
        a_C = sigma - (a_L + a_R + a_B + a_T)
        setMatrix(Amatrix, x, y, Rx, y, a_R, xnum)
        setMatrix(Amatrix, x, y, x, Dy, a_B, xnum)
        setMatrix(Amatrix, x, y, x, Uy, a_T, xnum)
        setMatrix(Amatrix, x, y, x, y, a_C, xnum)
    # Now right boundary condition (reflecting)
    x = xnum
    for y in xrange(1, ynum):
        Lx = x-1
        Dy = y-1
        Uy = y+1
        mat00 = IDI.getCellMaterialData(x,y)
        mat01 = IDI.getCellMaterialData(x,y+1)
        a_L = -(mat00[0]+mat01[0])*ydim/(2*xdim)
        a_B = -mat00[0]*xdim/(2*ydim)
        a_T = -mat01[0]*xdim/(2*ydim)
        sigma = xdim*ydim*(mat00[1]+mat01[1])/4
        Svector[x+y*(xnum + 1)] = source/2
        a_C = sigma - (a_L + a_B + a_T)        
        setMatrix(Amatrix, x, y, Lx, y, a_L, xnum)
        setMatrix(Amatrix, x, y, x, Dy, a_B, xnum)
        setMatrix(Amatrix, x, y, x, Uy, a_T, xnum)
        setMatrix(Amatrix, x, y, x, y, a_C, xnum)
    # Bottom boundary conditions (vacuum)
    y = 0
    for x in xrange(1, xnum):
        Lx = x-1
        Rx = x+1
        Uy = y+1
        mat00 = IDI.getCellMaterialData(x,1)
        mat10 = IDI.getCellMaterialData(x+1,1)
        a_L = -(mat00[0])*ydim/(2*xdim)
        a_R = -(mat10[0])*ydim/(2*xdim)
        a_B = -(mat00[0]+mat10[0])*xdim/(2*ydim)
        a_T = a_B
        sigma = xdim*ydim*(mat00[1]+mat10[1])/4
        Svector[x+y*(xnum + 1)] = source/2
        a_C = sigma - (a_L + a_R + a_B + a_T)
        setMatrix(Amatrix, x, y, Lx, y, a_L, xnum)
        setMatrix(Amatrix, x, y, Rx, y, a_R, xnum)
        setMatrix(Amatrix, x, y, x, Uy, a_T, xnum)
        setMatrix(Amatrix, x, y, x, y, a_C, xnum)
    # Top boundary condition (reflecting)
    y = ynum
    for x in xrange(1, xnum):
        Lx = x-1
        Rx = x+1
        Dy = y-1
        mat00 = IDI.getCellMaterialData(x,y)
        mat10 = IDI.getCellMaterialData(x+1,y)
        a_L = -(mat00[0])*ydim/(2*xdim)
        a_R = -(mat10[0])*ydim/(2*xdim)
        a_B = -(mat00[0]+mat10[0])*xdim/(2*ydim)
        sigma = xdim*ydim*(mat00[1]+mat10[1])/4
        Svector[x+y*(xnum + 1)] = source/2
        a_C = sigma - (a_L + a_R + a_B)
        setMatrix(Amatrix, x, y, Lx, y, a_L, xnum)
        setMatrix(Amatrix, x, y, Rx, y, a_R, xnum)
        setMatrix(Amatrix, x, y, x, Dy, a_B, xnum)
        setMatrix(Amatrix, x, y, x, y, a_C, xnum)
    # Finally corner cases
    # Bottom left (both vacuum)
    x = 0
    y = 0
    Rx = x+1
    Uy = y+1
    mat00 = IDI.getCellMaterialData(1,1)
    a_L = -(mat00[0])*ydim/(2*xdim)
    a_R = -(mat00[0])*ydim/(2*xdim)
    a_B = -(mat00[0])*xdim/(2*ydim)
    a_T = -(mat00[0])*xdim/(2*ydim)
    sigma = xdim*ydim*(mat00[1])/4
    Svector[x+y*(xnum + 1)] = source/4
    a_C = sigma - (a_L + a_R + a_B + a_T)
    setMatrix(Amatrix, x, y, Rx, y, a_R, xnum)
    setMatrix(Amatrix, x, y, x, Uy, a_T, xnum)
    setMatrix(Amatrix, x, y, x, y, a_C, xnum) 
    # Top left (vacuum left, reflecting top)
    x = 0
    y = ynum
    Rx = x+1
    Dy = y-1
    mat00 = IDI.getCellMaterialData(1,y)
    a_L = -(mat00[0])*ydim/(2*xdim)
    a_R = a_L
    a_B = -(mat00[0])*xdim/(2*ydim)
    sigma = xdim*ydim*(mat00[1])/4
    Svector[x+y*(xnum + 1)] = source/4
    a_C = sigma - (a_L + a_R + a_B)
    setMatrix(Amatrix, x, y, Rx, y, a_R, xnum)
    setMatrix(Amatrix, x, y, x, Dy, a_B, xnum)
    setMatrix(Amatrix, x, y, x, y, a_C, xnum)
    # Top right (both reflecting)
    x = xnum
    y = ynum
    Lx = x-1
    Dy = y-1
    mat00 = IDI.getCellMaterialData(x,y)
    a_L = -(mat00[0])*ydim/(2*xdim)
    a_B = -(mat00[0])*xdim/(2*ydim)
    sigma = xdim*ydim*(mat00[1])/4
    Svector[x+y*(xnum + 1)] = source/4
    a_C = sigma - (a_L + a_B)
    setMatrix(Amatrix, x, y, Lx, y, a_L, xnum)
    setMatrix(Amatrix, x, y, x, Dy, a_B, xnum)
    setMatrix(Amatrix, x, y, x, y, a_C, xnum)
    # Bottom right (vacuum bottom, reflecting right)
    x = xnum
    y = 0
    Lx = x-1
    Uy = y+1
    mat00 = IDI.getCellMaterialData(x,y)
    a_L = -(mat00[0])*ydim/(2*xdim)
    a_B = -(mat00[0])*xdim/(2*ydim)
    a_T = -(mat00[0])*xdim/(2*ydim)
    sigma = xdim*ydim*(mat00[1])/4
    Svector[x+y*(xnum + 1)] = source/4
    a_C = sigma - (a_L + a_B + a_T)
    setMatrix(Amatrix, x, y, Lx, y, a_L, xnum)
    setMatrix(Amatrix, x, y, x, Uy, a_T, xnum)
    setMatrix(Amatrix, x, y, x, y, a_C, xnum)
    # This should be it for matrix construction
    

    print "Matrix is complete..."
    print "Beginning Gauss-Seidel iterations..."
    solutions, error, iterations = GaussSeidel(Amatrix, Svector, Svector, rel_error, xnum)
    print "Computation complete..."
    return solutions, error, iterations

def setMatrix(matrix, x1, y1, x2, y2, value, xnum):
    if matrix[x1+y1*(xnum+1)][x2+y2*(xnum+1)] != 0:
        raise Exception(str(x1+y1*(xnum+1)) + "," + str(x2+y2*(xnum+1)) + " is already set.")
    else:
        matrix[x1+y1*(xnum+1)][x2+y2*(xnum+1)] = value

def GaussSeidel(A, b, x_0, tol, xnum, absolute=False):

    # Define the size of our system
    n = len(x_0)
    
    # We've got an initial guess, x_0 that we will store in x_old.
    # x_new will be for the new iterates, for now set to zero.
    x_new = np.zeros(n)
    x_old = x_0
    
    # Check if b is all zeros, if so, then just return all 0s
    
    if all(b) == 0:
        print "ALL ZERO"
        return x_new, 0, 0
    
    # We also need to initialize the error and track the iteration count
    error = 1.0
    itr = 0
    max_itr = 1e5 # Don't do more than this many iterations
    
    # Keep iterating until we get a 2-norm error under the tolerance
    # or we reach the max iteration count.
    
    while ((error > tol) and (itr < max_itr)):
        
        # increment the iteration counter.
        itr = itr+1
        print time.ctime() + ': Iteration ' + str(itr) + ', relative error: ' + str(error)
        for i in range(0, n):

            # Initialize the summation terms to zero on each iteration
            sum_1 = 0.0
            sum_2 = 0.0
            
            # Speeding up the calculation by ignoring zeros
            if i-(xnum+1) >= 0:
                sum_1 += A[i][i-(xnum+1)]*x_new[i-(xnum+1)]
            if i-1 >= 0:
                sum_1 += A[i][i-1]*x_new[i-1]
            if i+(xnum+1) < len(A):
                sum_2 += A[i][i+(xnum+1)]*x_old[i+(xnum+1)]
            if i+1 < len(A):
                sum_2 += A[i][i+1]*x_old[i+1]
            
            """# the k+1 term from 0 to i-1 
            for j in range(i):

                sum_1 = sum_1 + A[i][j] * x_new[j]

            # the k term from i+1 to n-1
            for j in range(i+1, n):

                sum_2 = sum_2 + A[i][j] * x_old[j]
            """
            x_new[i] = 1.0/A[i][i] * (b[i] - sum_1 - sum_2)
            
        # compute the absolute error or the relative error
        if (absolute == True):
            error = np.linalg.norm(np.abs(x_new - x_old),2) 
        else:
            error = np.linalg.norm(np.abs(x_new - x_old),2) / np.linalg.norm(x_new,2)

        # update the iterate
        x_old = copy.deepcopy(x_new)

    # return the solution and the error
    return x_new, error, itr
    
    