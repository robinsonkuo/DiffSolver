import time, sys
from versiondata import verData
from inputdata import process
from inputecho import inputecho
from solver import diffSolver
import pylab as pl
import numpy as np

version = "0.06"

def main():
    input = open('results/INPUT.txt', 'r')
    output = open('results/OUTPUT.txt', 'w')
    startTime = time.clock()
    verData(version, output)
    print "Scanning input data..."
    data = process(input)
    print "Input data verified..."
    xlen = data.getXdim()
    ylen = data.getYdim()
    xedges = data.getXcells()+1
    yedges = data.getYcells()+1
    inputecho(data, output)
    solutions, error, iterations = diffSolver(data)
    #print solutions
    fluxmap =[]
    for y in xrange(yedges):
        fluxmap.append(solutions[xedges*y:xedges*(y+1)])
    writeOutput(output, fluxmap, error, iterations, xedges, yedges, xlen, ylen)
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
    input.close()
    output.close()
    if iterations > 0:
        pl.show()
    return

def writeOutput(writeTo, fluxes, error, iterations, xedges, yedges, xlen, ylen):
    writeTo.write('\nIterations to reach convergence: ' + str(iterations) + '\n')
    error_string = "%.5g" % error
    writeTo.write('Relative error between last iterations: ' + error_string + '\n\n')
    
    writeTo.write("Flux values [n/cm^2s]\n\n")
    for y in xrange(len(fluxes)-1, -1, -1):
        y_value = y*ylen
        y_str = "|%.6g cm|" % y_value
        writeTo.write(y_str)
        spaces = 15 - len(y_str)
        while spaces > 0:
            writeTo.write(" ")
            spaces -= 1
        for x in xrange(len(fluxes[y])):
            # total string length of flux value and subsequent spacing should be 14 spaces
            flux = "%.6g" % fluxes[y][x]
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
        x_str = "|%.6g cm|" % x_value
        writeTo.write(x_str)
        spaces = 14 - len(x_str)
        while spaces > 0:
            writeTo.write(" ")
            spaces -= 1
        
    return
    
if (__name__ == "__main__"):
    main()
    

