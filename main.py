import time, sys
from versiondata import verData
from inputdata import process
from inputecho import inputecho
from solver import diffSolver

version = "0.02"

def main():
    input = open('results/INPUT.txt', 'r')
    output = open('results/OUTPUT.txt', 'w')
    startTime = time.clock()
    verData(version, output)
    data = process(input)
    inputecho(data, output)
    diffSolver(data)






    endTime = time.clock()
    executionTime = endTime-startTime
    print "Time to Execute: " + str(executionTime) + " seconds"
    input.close()
    output.close()
    return

    
if (__name__ == "__main__"):
    main()
    

