import sys

class inputDataInfo:
    
    
    def __init__(self, inputFile):
        
        # First process X and Y cells
        xline = inputFile.readline()
        if xline.startswith("X Cells: "):
            xline = xline[9:]
            self.x = int(xline)
        else:
            raise Exception("Number of x cells improperly formatted!")
            
        yline = inputFile.readline()
        if yline.startswith("Y Cells: "):
            yline = yline[9:]
            self.y = int(yline)
        else:
            raise Exception("Number of x cells improperly formatted!")
        
        if self.x < 1 or self.y < 1:
            raise Exception("Dimensions of x and y must be positive")
        
        
        
        
        
        




def process(inputFile):
    return inputDataInfo(inputFile)
