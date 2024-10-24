---
layout: code
title: Heat - The Helmholtz Analytics Toolkit
Topics: High-performance Computing, Data Analysis, Data Science, Machine Learning, Distributed Tensors, Python, MPI, GPU, CUDA, ROCm
Link: https://github.com/helmholtz-analytics/heat/
Project Head: Markus Götz
Members: KIT-SCC, FZJ-JSC, DLR-SC
toc: true
---

- TOC
{:toc}

# Heat

Heat builds on [PyTorch](https://pytorch.org/) and [mpi4py](https://mpi4py.readthedocs.io) to provide high-performance computing infrastructure for memory-intensive applications within the NumPy/SciPy ecosystem.


With Heat you can:
- port existing NumPy/SciPy code from single-CPU to multi-node clusters with minimal coding effort;
- exploit the entire, cumulative RAM of your many nodes for memory-intensive operations and algorithms;
- run your NumPy/SciPy code on GPUs (CUDA, ROCm, coming up: Apple MPS).

## Goals

Within HiRSE we would like to achieve at least the following objectives:

* Continuous Benchmarking ( ✅ )
* Portation to IPUs and XPUs (CUDA, ROCm: ✅)
* Optimized Communication and Distribution Semantics

## Activities

* Continuous Benchmarking via the [perun](https://pypi.org/project/perun/) tool including measurement of energy consumption for MPI applications.
* v1.3.1 supports PyTorch 2.0
* Usage on HPC systems simplified via spack and Docker containers (upcoming: Easybuild)
* New features include support for memory distributed truncated SVD.
* Upcoming in v1.4: distributed FFTS, optimized QR decomposition, batch-parallel clustering, fully distributed advanced indexing, and more.

