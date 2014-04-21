import numpy as np

""" Assuming vacuum boundary conditions in bottom/left faces and reflecting in top/right faces"""

def diffSolver(inputDataInfo):
    xyCells = inputDataInfo.xycells
    
    np.mat