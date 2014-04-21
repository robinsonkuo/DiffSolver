def inputecho(inputDataInfo, writeTo):
    
    writeTo.write("Size of unit cells:\n")
    writeTo.write("x-length [cm]: " + str(inputDataInfo.xdim) + "\ny-length [cm]: " + str(inputDataInfo.ydim) + "\n")
    writeTo.write("Uniform neutron source: " + str(inputDataInfo.source) + "\n")
    
    writeTo.write("Materials Used: index [D, sigma]:\n")
    i = 0
    for material in inputDataInfo.materials:
        writeTo.write(str(i) + " " + str(material) + "\n")
        i += 1
    writeTo.write("\n")
    writeTo.write("Geometry of the system with material index used in each cell\n")
    for y in xrange(inputDataInfo.y-1, -1, -1):
        for x in xrange(inputDataInfo.x):
            writeTo.write(str(inputDataInfo.xycells[x][y]) + " ")
        writeTo.write("\n")
    