import sys, numpy

properFormat = []
properFormat.append("X Cells: ")
properFormat.append("Y Cells: ")
properFormat.append("X-dimension [cm]: ")
properFormat.append("Y-dimension [cm]: ")
properFormat.append("Number of materials: ")
properFormat.append("Source Term: ")




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
        for i in xrange(self.x):
            self.xycells.append(self.y*[[]])
        

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
        
        if self.xdim < 1 or self.ydim < 1:
            raise Exception("Dimension lengths should not be negative")
        
        # Number of materials
        numMatLine = inputFile.readline()
        if numMatLine.startswith("Number of materials: "):
            self.numMat = int(numMatLine[len("Number of materials: "):])
        else:
            raise Exception("Number of materials should be ... Number of materials: #")
        if self.numMat < 1:
            raise Exception("Must have positive number of materials")
        self.materials = [[]]*self.numMat
        
        for i in xrange(self.numMat):
            matLine = inputFile.readline()
            if matLine.startswith(str(i) + " "):
                matLine = matLine[len(str(i) + " "):]
                matData = matLine.split(" ")
                self.materials[i] = [float(j) for j in matData[:2]] #Stops at 2 to exclude the \n character
            else:
                raise Exception("Material " + i + " has an invalid diffusivity/cross section formatting")
        
        sourceLine = inputFile.readline()
        if sourceLine.startswith("Source term: "):
            self.source = float(sourceLine[len("Source term: "):])
        else:
            raise Exception("Source term should be ... Source term: #")
        
        defmatLine = inputFile.readline()
        if defmatLine.startswith("Default material: "):
            self.defmat = int(defmatLine[len("Default material: ")])
            if self.defmat >= self.numMat:
                raise Exception("Default material number must be less than the number of materials")
            for x in xrange(self.x):
                for y in xrange(self.y):
                    self.xycells[x][y] = self.defmat
        else:
            raise Exception("Default material should ... Default material: #")
        
        numGeoLine = inputFile.readline()
        if numGeoLine.startswith("Number of geometries: "):
            self.numGeo = int(numGeoLine[len("Number of geometries: "):])
        else:
            raise Exception("Number of geometries should be ... Number of geometries: #")
        
        for i in xrange(self.numGeo):
            geoLine = inputFile.readline()
            rectLine = geoLine.split(" ")
            rectData = [int(j) for j in rectLine[:4]]
            material = int(rectLine[4])
            for x in xrange(rectData[0], rectData[2]+1):
                for y in xrange(rectData[1], rectData[3]+1):
                    self.xycells[x][y] = material
            
        
                
        
        
        
        




def process(inputFile):
    return inputDataInfo(inputFile)
