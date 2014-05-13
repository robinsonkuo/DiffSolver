import time, sys
from versiondata import verData
from inputdata import process
from inputecho import inputecho
from solver import diffSolver
import pylab as pl
import numpy as np

version = "0.10"
SOLUTION_LIMIT = 500 # Adjust this to be greater if one desires the A_matrix and Source vector to be included in the matlab output


def main():
    inputF = open('INPUT.txt', 'rb')
    output = open('results/OUTPUT.txt', 'wb')
    matlab = open('results/OUTPUT.m', 'wb')
    startTime = time.clock()
    verData(version, output)
    print "Scanning input data..."
    data = process(inputF)
    print "Input data verified..."
    xlen = data.getXdim()
    ylen = data.getYdim()
    xedges = data.getXcells()+1
    yedges = data.getYcells()+1
    inputF.close()
    inputF = open('INPUT.txt', 'rb')
    inputecho(data, output, inputF)
    solutions, error, iterations = diffSolver(data, matlab, SOLUTION_LIMIT)
    #print solutions
    fluxmap =[]
    for y in xrange(yedges):
        fluxmap.append(solutions[xedges*y:xedges*(y+1)])
    writeOutput(output, fluxmap, error, iterations, xedges, yedges, xlen, ylen, matlab, solutions)
    fluxmap = np.array(fluxmap)
    if iterations > 0:
        pl.pcolor(fluxmap)
        pl.colorbar()
        pl.ylim([0,yedges])
        pl.xlim([0,xedges])
        pl.draw()


    endTime = time.clock()
    executionTime = endTime-startTime
    
    print "Time to Execute: " + str(executionTime) + " seconds"
    inputF.close()
    output.close()
    matlab.close()
    if iterations > 0:
        pl.show()
    return

def writeOutput(writeTo, fluxes, error, iterations, xedges, yedges, xlen, ylen, matlab, solutions):
    writeTo.write('\nIterations to reach convergence: ' + str(iterations) + '\n')
    error_string = "%.5g" % error
    writeTo.write('Relative error between last iterations: ' + error_string + '\n\n')
    
    writeTo.write("Flux values [n/cm^2s]\n\n")
    for y in xrange(len(fluxes)-1, -1, -1):
        y_value = y*ylen
        y_str = "|%.4g cm|" % y_value
        writeTo.write(y_str)
        spaces = 15 - len(y_str)
        while spaces > 0:
            writeTo.write(" ")
            spaces -= 1
        for x in xrange(len(fluxes[y])):
            # total string length of flux value and subsequent spacing should be 14 spaces
            flux = "%.4g" % fluxes[y][x]
            writeTo.write(flux)
            spaces = 14 - len(flux)
            while spaces > 0:
                writeTo.write(" ")
                spaces -= 1
        writeTo.write('\n')
    spaces = 15
    while spaces > 0:
        writeTo.write(" ")
        spaces -= 1
    for x in xrange(len(fluxes[0])):
        x_value = x*xlen
        x_str = "|%.4g cm|" % x_value
        writeTo.write(x_str)
        spaces = 14 - len(x_str)
        while spaces > 0:
            writeTo.write(" ")
            spaces -= 1
            
    # Writing the result vector to matlab
    matlab.write("phi = [")
    matlab.write(str(solutions[0]))
    for s in solutions[1:]:
        matlab.write("; " + str(s))
    matlab.write("];\n")
    if len(solutions) < SOLUTION_LIMIT:
        matlab.write("phi_direct = inv(A)*source;\n")
        matlab.write("error_vector = phi_direct-phi;\n")
        matlab.write("error = norm(phi_direct-phi, 2)/(norm(phi_direct, 2));")
    return
    
if (__name__ == "__main__"):
    main()
    

