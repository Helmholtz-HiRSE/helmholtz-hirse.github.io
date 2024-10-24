---
layout: code
title: FLEUR
Topics: All-electron Density Functional Theory, Materials Science, Solid State Physics
Link: https://www.flapw.de
Project Head: Stefan Blügel, Daniel Wortmann
Members: Gregor Michalicek, Thomas Bornhake, Wejdan Beida
toc: true
---

- TOC
{:toc}

# FLEUR

FLEUR is an all-electron density functional theory suite of codes based on the full-potential linearized augmented plane wave (FLAPW) method. The key component of FLEUR is a versatile DFT code for the ground-state properties of multicomponent one-, two- and three-dimensional solids. A special focus of the development lies on non-collinear magnetism, the determination of exchange parameters, spin-orbit related properties (topological and Chern insulators, Rashba and Dresselhaus effect, magnetic anisotropies, Dzyaloshinskii-Moriya interaction) and magnon and phonon dispersion. A link to WANNIER90 enables the calculation of intrinsic and extrinsic transverse transport properties (anomalous-, spin- and inverse spin Hall effect, spin-orbit torque, anomalous Nernst effect, or topological transport properties such as the quantum spin-Hall effect etc.) in linear response theory using the Kubo formula. FLEUR includes LDA+U as well as hybrid-functionals for the accurate description of e.g. oxide materials and by linking against the libxc library, many more functionals are accessible.

FLEUR is one of the lighthouse codes of the MaX-Centre of Excellence.

## Goals

The main goals within HIRSE are dealing with the extension and consolidation of our development process:
- Extension of the CI testing to performance testing.
- Clearer developed path to integrate large scale developments without breaking the code base.
- Modularization and refactoring of OpenACC and OpenMP implementations.
- Development of calculation setup parameter profiles to minimize manual setup needs for HPC and HTC projects.

## Activities

- Generation of a set of performance tests suitable for automatic execution.
- Creation, integration and comissioning of the infrastructure for continuous benchmarking, based on the software Bencher.


