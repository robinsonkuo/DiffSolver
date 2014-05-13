DiffSolver
==========
These files compose the 2-D Neutron Diffusion Equation Solver implemented by Robinson Kuo.

How to Execute:
In order to run the code, one must first install the NumPy and PyLab packages. These both come as part of the SciPy suite,
which is probably the easiest way to install the necessary software.
Once the required software packages are installed, the code can be executed by having a properly formatted input file, 
named "INPUT.txt", in the same directory as all the python files and executing main.py. Once completed, there will be two
output files in a subdirectory named results: "OUTPUT.txt", which contains information from the input files and the results
of running the solver (number of iterations required, error, flux values for each cell), and "OUTPUT.m", which is the
Matlab file containing the solved flux vector and (assuming the size of the problem is not too large) the matrix used to
solve the problem and the source vector
