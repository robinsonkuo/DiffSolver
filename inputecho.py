def inputecho(inputDataInfo, writeTo, inputF):
    
    """writeTo.write("Size of unit cells:\n")
    writeTo.write("x-length [cm]: " + str(inputDataInfo.xdim) + "\ny-length [cm]: " + str(inputDataInfo.ydim) + "\n")
    writeTo.write("Uniform neutron source [n/cm^3s]: " + str(inputDataInfo.source) + "\n")
    
    writeTo.write("Materials Used: index (diffusion coefficient [cm], cross section [cm^-1]):\n")
    i = 0
    for material in inputDataInfo.materials:
        writeTo.write(str(i) + " " + str(material) + "\n")
        i += 1
    writeTo.write("\n")
    writeTo.write("Relative error tolerance: " + str(inputDataInfo.getRelError()) + '\n\n')"""
    for line in inputF.readlines():
        writeTo.write(line)
    writeTo.write("\n\nGeometry of the system with material index used in each cell\n")
    for y in xrange(inputDataInfo.y, 0, -1):
        y_value = y*inputDataInfo.getYdim()
        y_str = "|%.6g cm|" % y_value
        writeTo.write(y_str)
        spaces = 12 - len(y_str)
        while spaces > 0:
            writeTo.write(" ")
            spaces -= 1
        for x in xrange(1, inputDataInfo.x+1):
            spaces = 10
            writeTo.write(str(inputDataInfo.xycells[x][y]))
            spaces -= len(str(inputDataInfo.xycells[x][y]))
            while spaces > 0:
                writeTo.write(" ")
                spaces -= 1
        writeTo.write("\n")
    spaces = 10
    while spaces > 0:
        writeTo.write(" ")
        spaces -= 1
    for x in xrange(1,inputDataInfo.x+1):
        x_value = x*inputDataInfo.getXdim()
        x_str = "|%.6g cm|" % x_value
        writeTo.write(x_str)
        spaces = 10 - len(x_str)
        while spaces > 0:
            writeTo.write(" ")
            spaces -= 1
    writeTo.write("\n\n")
    writeTo.write("Sources [n/cm^3s] in each cell\n")
    
    
    for y in xrange(inputDataInfo.y, 0, -1):
        y_value = y*inputDataInfo.getYdim()
        y_str = "|%.6g cm|" % y_value
        writeTo.write(y_str)
        spaces = 12 - len(y_str)
        while spaces > 0:
            writeTo.write(" ")
            spaces -= 1
        for x in xrange(1, inputDataInfo.x+1):
            spaces = 10
            source_str = "%.3g" % inputDataInfo.sources[x][y]
            spaces -= len(source_str)
            writeTo.write(source_str)
            while spaces > 0:
                writeTo.write(" ")
                spaces -= 1
        writeTo.write("\n")
    spaces = 12
    while spaces > 0:
        writeTo.write(" ")
        spaces -= 1
    for x in xrange(1,inputDataInfo.x+1):
        x_value = x*inputDataInfo.getXdim()
        x_str = "|%.6g cm|" % x_value
        writeTo.write(x_str)
        spaces = 10 - len(x_str)
        while spaces > 0:
            writeTo.write(" ")
            spaces -= 1
    writeTo.write("\n")
    return