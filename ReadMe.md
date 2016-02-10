A corner in an image I is a pixel p where two edges from different directions intersect. Corners
can be characterized by high curvature of intensity values.

-----------
1. Hessian
-----------
Implements corner detection algorithm based on Hessian matrix (H) computation. Note that Hessian
matrix is defined for a given image I at a pixel p as

H1(p) = |Ixx(p) Ixy(p)|
		|Ixy(p) Iyy(p)|

such that eigen-decomposition (spectral decomposition) of this matrix yields two eigenvalues as: Lambda1 and Lambda2. If both Lambda1, Lambda2 are large, we are at a corner.

---------
2.Harris
---------
Implements Harris Corner Detection algorithm for the same input images you previously.
Rather than considering the Hessian of the original image I (i.e. second-order derivatives), we use the first-order derivatives of the smoothed version L(p; sigma) for some Gaussian filter with standard deviation sigma > 0.
We then calculate the cornerness using two different functions and then compare their efficiency.


