import time, sys
from versiondata import verData
from inputdata import process


version = "0.01"

def main():
    input = open('results/INPUT.txt', 'r')
    output = open('results/OUTPUT.txt', 'w')
    startTime = time.clock()
    verData(version, output)
    process(input)














    endTime = time.clock()
    executionTime = endTime-startTime
    print "Time to Execute: " + str(executionTime) + " seconds"
    input.close()
    output.close()
    

    
if (__name__ == "__main__"):
    main()

