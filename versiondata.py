import time

def verData(versionNum, file):
    output = []
    output.append("2-D Diffusion Solver")
    output.append("Version Number " + versionNum)
    output.append("Author: Robinson Kuo")
    output.append("Computation Started at " + time.ctime())
    for line in output:
        print line
        file.write(line + "\n")
    print "\n"
    file.write("\n")
    return