def inputecho(inputDataInfo, writeTo):
    
    writeTo.write("Size of unit cells:\n")
    writeTo.write("x-length [cm]: " + str(inputDataInfo.xdim) + "\ny-length [cm]: " + str(inputDataInfo.ydim) + "\n")
    writeTo.write("Uniform neutron source [n/cm^3s]: " + str(inputDataInfo.source) + "\n")
    
    writeTo.write("Materials Used: index (diffusion coefficient [cm], cross section [cm^-1]):\n")
    i = 0
    for material in inputDataInfo.materials:
        writeTo.write(str(i) + " " + str(material) + "\n")
        i += 1
    writeTo.write("\n")
    writeTo.write("Relative error tolerance: " + str(inputDataInfo.getRelError()) + '\n\n')
    writeTo.write("Geometry of the system with material index used in each cell\n")
    for y in xrange(inputDataInfo.y, 0, -1):
        for x in xrange(1, inputDataInfo.x+1):
            spaces = 4
            writeTo.write(str(inputDataInfo.xycells[x][y]))
            spaces -= len(str(inputDataInfo.xycells[x][y]))
            while spaces > 0:
                writeTo.write(" ")
                spaces -= 1
        writeTo.write("\n")
    