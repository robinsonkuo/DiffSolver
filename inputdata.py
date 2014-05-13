import sys, numpy


class inputDataInfo:
    
    
    def __init__(self, inputFile):
        
        # First process X and Y cells
        xline = inputFile.readline()
        if xline.startswith("X Cells: "):
            xline = xline[9:]
            self.x = int(xline)
        else:
            raise Exception("x number cells improperly formatted!")
            
        yline = inputFile.readline()
        if yline.startswith("Y Cells: "):
            yline = yline[9:]
            self.y = int(yline)
        else:
            raise Exception("y number cells improperly formatted!")
        
        if self.x < 1 or self.y < 1:
            raise Exception("Number of cells must be positive")
        
        self.xycells = []
        for i in xrange(self.x+1):
            self.xycells.append((self.y+1)*[[]])
        

        # Next find cell size dimensions, assume uniform
        xdim = inputFile.readline()
        if xdim.startswith("X-dimension [cm]: "):
            self.xdim = float(xdim[len("X-dimension [cm]: "):])
        else:
            raise Exception("X-dimension of cells improperly formatted!")
        
        ydim = inputFile.readline()
        if ydim.startswith("Y-dimension [cm]: "):
            self.ydim = float(ydim[len("Y-dimension [cm]: "):])
        else:
            raise Exception("Y-dimension of cells improperly formatted!")
        
        if self.xdim <= 0 or self.ydim <= 0:
            raise Exception("Dimension lengths must be positive")
        
        # Number of materials
        numMatLine = inputFile.readline()
        if numMatLine.startswith("Number of materials (Material #, D [cm], Sigma [cm-1]): "):
            self.numMat = int(numMatLine[len("Number of materials (Material #, D [cm], Sigma [cm-1]): "):])
        else:
            raise Exception("Number of materials should be ... Number of materials (Material #, D [cm], Sigma [cm-1]): #")
        if self.numMat < 1:
            raise Exception("Must have positive number of materials")
        self.materials = [[]]*self.numMat
        
        # Materials are entered with Diffusion Coefficient then cross section
        for i in xrange(self.numMat):
            try: 
                matLine = inputFile.readline()
                if matLine.startswith(str(i) + " "):
                    matLine = matLine[len(str(i) + " "):]
                    matData = matLine.split(" ")
                    self.materials[i] = [float(j) for j in matData[:2]] #Stops at 2 to exclude the \n character
                    if self.materials[i][0] < 0:
                        raise Exception("Material " + str(i) + " cannot have a negative diffusion coefficient")
                    if self.materials[i][1] < 0:
                        raise Exception("Material " + str(i) + " cannot have a negative cross section")
                else:
                    raise Exception("Material " + str(i) + " has an invalid diffusion coefficient/cross section formatting")
            except:
                raise Exception("Materials not properly formatted")

        
        defmatLine = inputFile.readline()
        if defmatLine.startswith("Default material: "):
            self.defmat = int(defmatLine[len("Default material: ")])
            if self.defmat >= self.numMat:
                raise Exception("Default material number must be less than the number of materials")
            for x in xrange(self.x+1):
                for y in xrange(self.y+1):
                    self.xycells[x][y] = self.defmat
        else:
            raise Exception("Default material should ... Default material: #")
        
        numGeoLine = inputFile.readline()
        if numGeoLine.startswith("Number of geometries: "):
            self.numGeo = int(numGeoLine[len("Number of geometries: "):])
        else:
            raise Exception("Number of geometries should be ... Number of geometries: #")
        
        for i in xrange(self.numGeo):
            try:
                geoLine = inputFile.readline()
                rectLine = geoLine.split(" ")
                rectData = [int(j) for j in rectLine[:4]]
                material = int(rectLine[4])
                if material < 0:
                    raise Exception("Materials in geometries must be non-negative numbers")
                for x in xrange(rectData[0]-1, rectData[2]):
                    for y in xrange(rectData[1]-1, rectData[3]):
                        self.xycells[x][y] = material
            except:
                raise Exception("Geometries improperly formatted")
                    
        sourceLine = inputFile.readline()
        if sourceLine.startswith("Default source [n/cm3s]: "):
            self.source = float(sourceLine[len("Default source [n/cm3s]: "):])
            if self.source < 0:
                raise Exception("Source term cannot be negative")
        else:
            raise Exception("Source term should be ... Default source [n/cm3s]: #")
        
        numSourceLine = inputFile.readline()
        if numSourceLine.startswith("Number of unique sources: "):
            self.numSources = int(numSourceLine[len("Number of unique sources: "):])
            if self.numSources < 0:
                raise Exception("Number of unique sources must be at least 0")
        else:
            raise Exception("Number of unique sources should be ... Number of unique sources: #")
        
        self.sources = []
        for i in xrange(self.x+1):
            self.sources.append((self.y+1)*[self.source])
        for i in xrange(self.numSources):
            try:
                sgeoLine = inputFile.readline()
                srectLine = sgeoLine.split(" ")
                srectData = [int(j) for j in srectLine[:4]]
                source_val = float(srectLine[4])
                if source_val < 0:
                    raise Exception("Source values must be non-negative")
                for x1 in xrange(srectData[0]-1, srectData[2]):
                    for y1 in xrange(srectData[1]-1, srectData[3]):
                        self.sources[x1][y1] = source_val
            except:
                raise Exception("Unique sources improperly formatted")
        
        errorLine = inputFile.readline()
        if errorLine.startswith("Relative error tolerance: "):
            self.rel_error = float(errorLine[len("Relative error tolerance: "):])
            if self.rel_error <= 0:
                raise Exception("Relative error tolerance must be positive!")
        else:
            print errorLine
            raise Exception("Relative error tolerance should be formatted... \"Relative error tolerance: number \" where number is written as a decimal or in scientific notation, i.e. 0.011 or 1.1E-2")
        
        
    def getSources(self):
        return self.sources
    
    def getCellMaterialData(self, x, y):
        return self.materials[self.xycells[x][y]]
    
    def getXdim(self):
        return self.xdim
    
    def getYdim(self):
        return self.ydim
    
    def getXcells(self):
        return self.x
    
    def getYcells(self):
        return self.y
    
    def getFluxVectorLength(self):
        return (self.getXcells()+1)*(self.getYcells()+1)
    
    def getRelError(self):
        return self.rel_error
    
                
        
        
        
        




def process(inputFile):
    return inputDataInfo(inputFile)
