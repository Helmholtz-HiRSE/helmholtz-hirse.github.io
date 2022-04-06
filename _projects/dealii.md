---
layout: project
title: deal.II - an open source finite element library
Project_Head: Peter Munch (Hereon) is one of the principal developers mostly involved in the HPC and linear algebra aspects of the library
Members: World-wide team of developers
Link: https://www.dealii.org/
toc: true
---

- TOC
{:toc}

# deal.II

deal.II is a C++ software library supporting the creation of finite element codes for a broad 
variety of PDEs, from laptops to supercomputers (e.g, 300k processes on SuperMUC-NG). It is 
used in a large variaty of application 
fields, ranging from traditional fluid/solid mechanics to plasma physics. Features
comprise: matrix-free implementations, parallelization (MPI, threading via TBB, SIMD, GPU support), 
discontinuous Galerkin methods, AMR via p4est, particles, wrappers for PETSc and Trilinos,
particles, hp-adaptivity, simplex and mixed meshes. The library is
freely available under LGPL 2.1 license.

## Goals

With the support of HiRSE_PS, we plan to improve the performance testing infrastructure of the library.
The goal is to find unintentional performance degradations at an early stage so that they can be 
fixed before the yearly release. Challenges are 1) that many performance issues only become critical 
at large scale and 2) to make data accessible and easy to understand to users who are not familiar 
with computer science.

## Activities

None so far.
