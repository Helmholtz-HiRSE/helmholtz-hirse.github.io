---
layout: code
title: FLEUR
Topics: All-electron Density Functional Theory, Materials Science, Solid State Physics
link: https://www.flapw.de
Project Head: Stefan Blügel, Daniel Wortmann
Members: Gregor Michalicek, Uliana Alekseeva, Christian-R. Gerhorst
toc: true
---

- TOC
{:toc}

# FLEUR
FLEUR is an all-electron density functional theory suite of codes based on the full-potential linearized augmented plane wave (FLAPW) method. The key component of FLEUR is a versatile DFT code for the ground-state properties of multicomponent one-, two- and three-dimensional solids. A special focus of the development lies on non-collinear magnetism, the determination of exchange parameters, spin-orbit related properties (topological and Chern insulators, Rashba and Dresselhaus effect, magnetic anisotropies, Dzyaloshinskii-Moriya interaction) and magnon dispersion. A link to WANNIER90 enables the calculation of intrinsic and extrinsic transverse transport properties (anomalous-, spin- and inverse spin Hall effect, spin-orbit torque, anomalous Nernst effect, or topological transport properties such as the quantum spin-Hall effect etc.) in linear response theory using the Kubo formula. FLEUR includes LDA+U as well as hybrid-functionals for the accurate description of e.g. oxide materials and by linking against the libxc library, many more functionals are accessible.

FLEUR is one of the flagship codes of the MaX-Centre of Excellence.
## Goals
The main goals within HIRSE_PS are dealing with the extension and consolidation of our development process:
- Extension of the CI testing to performance testing.
- Clearer developed path to integrate large scale developments without breaking the code base.
- Modularization and refactoring of OpenACC and OpenMPI implementations.


## Acitivties

Generation of a set of performance tests suitable for automatic execution.

