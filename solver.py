import numpy as np

""" Assuming vacuum boundary conditions in bottom/left faces and reflecting in top/right faces"""

def diffSolver(inputDataInfo):
    xyCells = inputDataInfo.xycells
    materials = inputDataInfo.materials
    xdim = inputDataInfo.xdim
    ydim = inputDataInfo.ydim
    xnum = inputDataInfo.x
    ynum = inputDataInfo.y
    print("Will solve here")