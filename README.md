DiffSolver
==========
These files compose the 2-D Neutron Diffusion Equation Solver implemented by Robinson Kuo. The solver utilizes the Gauss-Seidel iterative method on a Finite Volume discretization of a two-dimensional surface. The only implemented boundary conditions are vacuum on the bottom and left surfaces and reflecting on the top and right surfaces.

How to Execute
--------
In order to run the code, one must first install the NumPy and PyLab packages. These both come as part of the SciPy suite,
which is probably the easiest way to install the necessary software.
Once the required software packages are installed, the code can be executed by having a properly formatted input file, 
named "INPUT.txt", in the same directory as all the python files and executing main.py. Once completed, there will be two
output files in a subdirectory named results: "OUTPUT.txt", which contains information from the input files and the results
of running the solver (number of iterations required, error, flux values for each cell), and "OUTPUT.m", which is the
Matlab file containing the solved flux vector and (assuming the size of the problem is not too large) the matrix used to
solve the problem and the source vector.

STATUS
--------
Code is operational and appears to solve problems correctly. Let me know if any bugs appear!

PURPOSE
--------
The purpose of the code is to solve the two-dimensional neutron diffusion equation using the Gauss-Seidel iterative method. While it is technically possible to solve these problems analytically using matrix inversion and other direct calculation methods, these methods are often resource-intensive and slow for sufficiently large systems (which requires solving a large matrix problem of the form Ax = b). Iterative methods, while not always exact, can provide a good approximation for the expected positional neutorn flux.

INPUT
--------
The following is a sample input that is properly formatted:

X Cells: 50

Y Cells: 60

X-dimension [cm]: 1

Y-dimension [cm]: 2.3

Number of materials (Material #, D [cm], Sigma [cm-1]): 2

0 1000 10.0

1 100 100

Default material: 0

Number of geometries: 1

20 20 25 25 1

Default source [n/cm3s]: 100.6

Number of unique sources: 2

50 50 50 50 500

23 25 24 30 50.1

Relative error tolerance: 1.0E-6


Note that all character strings that don't describe numbers must appear exactly as shown.

Going line by line:

X Cells: 50 % Specifies the number of cells in the x-direction for the problem (must be positive integer)

Y Cells: 60 % Specifies the number of cells in the y-direction for the problem (must be positive integer)

X-dimension [cm]: 1 % Specifies the length in the x-direction for a single unit cell (must be positive real number)

Y-dimension [cm]: 2.3 % Specifies the length in the y-direction for a single unit cell (must be positive real number)

Number of materials (Material #, D [cm], Sigma [cm-1]): 2 % Specifies the number of different materials used (positive 
integer) % NOTE: The number of materials in the number of materials line must match exactly the number of materials specified below. Additionally, the materials must be numbered sequentially starting from 0, and incrementing by 1.

0 1000 10.0 % Material indexed 0, with D = 1000 and Sigma = 10.0 (both D and Sigma must be non-negative real numbers)

1 100 100 % Material indexed 1, with D = 100, Sigma = 100 (both D and Sigma must be non-negative real numbers)

Default material: 0 % Specifies the index of the material that fills the surface if not otherwise specified

Number of geometries: 1 % Number of rectangles filled with a single material that are to be placed on the surface; 
overwrites the default material for the specified cells (non-negative integer; NOTE: If this is 0, then there should be no geometry lines and the next line should be the Default source line).

20 20 25 25 1 % Specifies the lower x, lower y, upper x and upper y cells (inclusive) of the rectangle to be filled with material index (1 in this case). All cell values must be non-negative integers and the material index must have been specified under materials. NOTE: If rectangles overlap, the last entry specified will fill the overlapping area. 

Default source [n/cm3s]: 100.6 % Specifies the source value that fills all cells not otherwise specified (Non-negative real number)

Number of unique sources: 2 % Number of rectangles filled with a single source value that are to be placed on the surface; overwrites the default source for the specified cells (non-negative integer; NOTE: If this is 0, then there should be no unique source lines and the next line should be the Relative error tolerance line).

50 50 50 50 500 % Specifies the lower x, lower y, upper x and upper y cells (inclusive) of the rectangle to be filled with the source value (500 in this case). All cell values must be positive integers, and the source value must be a non-negative real number. NOTE: If rectangles overlap, the last entry specified will fill the overlapping area. 

23 25 24 30 50.1

Relative error tolerance: 1.0E-6 % The acceptable tolerance between the final two Gauss-Seidel iterations. This is defined by norm(flux(k+1)-flux(k))/norm(flux(k+1)), where k is the number of the iteration. NOTE: By default, the code will terminate after 10E6 iterations if the tolerance has not yet been reached.

OUTPUT
-------
The OUTPUT.txt file will consist a repetition of the input file, as well as an ASCII display of the specified materials and sources. For materials and sources, the material/source listed for a given x,y coordinate applies to the cell whose top-right corner is those coordinates.
Additionally, the number of Gauss-Seidel iterations and the final relative error between iterations is listed. The computed flux is displayed in a similar format to the specified materials and sources with one caveat. Since flux is edge-centered, the values of flux are the values at the intersection of those x-y coordinates. For example, if the bottom axis is 1cm and the left axis is 5 cm, then the value for the intersection is the flux centered at x = 1cm and y = 5cm.
The OUTPUT.m file will always at least contain the computed flux vector, called 'phi'. The flux is organized first by ascending x-coordinate then by ascending y-coordinate. So all values where y = 0 cm will be listed before values where y = 1 cm are listed.
If the size of the problem is not too large (the size can be specified by changing the SOLUTION_LIMIT value in the main.py file), then the A matrix (used to solve A*flux = source) and the source vector are also given, as well as a few short equations to compute the error between the iterative solution and the direct solution by inversion of A.

Limitations and Restrictions
------
The biggest limitation is probably the lack of variable boundary conditions. Right now, all problems must assume a left and bottom vacuum boundary condition and a top and right reflecting boundary condition. The current capabilities for inputting geometries of materials and sources is also rather constraining, though it is possible to construct virtually any 2D geometry with the current tools.
