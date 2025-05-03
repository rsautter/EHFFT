# Entangled Hexagonal Fast Fourier Transform

This repository provides an implementation of the Fast Fourier Transform (FFT) adapted for a hexagonal grid. It's important to note that this approach, utilizing an entangled hexagonal grid represented by a 3-directional 2D system (vertical and two diagonals), does not inherently guarantee orthonormality as in a standard 2D FFT. 

An example of diagonal in a hexagonal lattice is given by:

![](https://raw.githubusercontent.com/rsautter/EHFFT/refs/heads/main/EHFFT/hexDiag.png)

This lattice is stored as the following matrix:

![](https://raw.githubusercontent.com/rsautter/EHFFT/refs/heads/main/EHFFT/matHexDiag.png)
