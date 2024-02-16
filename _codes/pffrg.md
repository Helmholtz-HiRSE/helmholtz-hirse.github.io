---
layout: code
title: PFFRG for quantum magnetic systems
Topics: Condensed matter physics, quantum magnetism, functional renormalization group methods
Project Head: Johannes Reuther
Members: Nils Niggemann, Vincent Noculak, Matías Gonzalez, Michele Mesiti
toc: true
---

- TOC
{:toc}

# PFFRG

Simulating quantum magnetic systems such as frustrated spin models is a notoriously difficult problem, as it requires solving a complex quantum many-body problem. Despite a plethora of powerful existing approaches such as tensor network methods and extensive efforts to develop new techniques, each method also has its limitations such that, overall, there is still a significant lack of methods. The PFFRG is a complementary technique for simulating quantum magnetic systems which relies on a renormalization group ansatz. The key advantage over other methods lies in its enhanced flexibility as it allows one to treat systems with complex microscopic spin interactions and complicated lattice geometries, including three-dimensional networks. From a technical viewpoint, the approach amounts to solving large sets of coupled differential equations for spin correlation functions, whose numerical outcomes can be directly compared with experiments.

## Goals

Our activities in developing, implementing and applying the PFFRG code are relatively young and have mostly occurred within the past ten years. Particularly, with the recent development of the PMFRG, which is a variant of the PFFRG, a new promising future research direction is opened up. Among other advantages, the PMFRG is capable of simulating the effects of finite temperatures more accurately. Given this fast progress in fundamental method development there is now a need for focussing more on our research codes. Particularly, our future activities aim at optimizing the code performance and making it more user friendly. Another important task is a better code optimization for high performance computing via efficient parallelization.
As a quite new software project and with our main contributors being physicists with only secondary software development experience, our group benefits in particular from the counseling opportunities offered by HiRSE.

## Codes
`PMFRG.jl` (**P**seudo-**M**ajorana **F**unctional **R**enormalization **G**roup) is a package written in the [Julia language](https://julialang.org/). It is used to compute observables for spin- $1/2$ Heisenberg models of the form

```math
H = \sum_{ij} J_{ij} \vec{S}_i \cdot \vec{S}_j
```
### Installation
- First, a working installation of Julia is required. We recommend an installation via [juliaup](https://github.com/JuliaLang/juliaup).
Subsequently, `PMFRG.jl` and its dependencies are best installed via first installing the private registry "JuliaPMFRG". Type `]` in the shell to enter the package mode:
```
(@v1.10) pkg> registry add https://github.com/NilsNiggemann/JuliaPMFRGRegistry.git
```
This only needs to be done once on every machine. Then, `PMFRG.jl`, its dependencies and other helper packages for evaluation can be installed conveniently via
```
(v1.10) pkg> add PMFRG
```
For further usage instructions, see https://github.com/NilsNiggemann/PMFRG.jl.
## Activities
In the scope of HiRSE_PS, `PMFRG.jl`, formerly a private repository, has since become a public open-source software package.
In this context, the package now features
- Continuous integration
- Installation instructions
- Usage documentation.

In a very successful collaboration with Michele Mesiti, enabled by HiRSE_PS, a working implementation of a new hybrid parallelization scheme employing julia threads as well as MPI for inter-node communication was developed. 

## Relevant publications
The following is a list of selected publications, which outline the background and methodology of the PMFRG method.

- Benedikt Schneider, Johannes Reuther, Matías G. Gonzalez, Björn Sbierski, Nils Niggemann, Temperature flow in pseudo-Majorana functional renormalization for quantum spins, [arXiv:2312.14838 (2023)](https://arxiv.org/abs/2312.14838)

- Tobias Müller, Dominik Kiese, Nils Niggemann, Björn Sbierski, Johannes Reuther, Simon Trebst, Ronny Thomale, Yasir Iqbal, Pseudo-fermion functional renormalization group for spin models,  [Rep. Prog. Phys. 87 036501 (2024)](https://doi.org/10.1088/1361-6633/ad208c)

- Nils Niggemann, Björn Sbierski, and Johannes Reuther, Frustrated quantum spins at finite temperature: Pseudo-Majorana functional renormalization group approach, [Phys. Rev. B 103, 104431 (2021)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.103.104431)

- J. Reuther and P. Wölfle, J1-J2 frustrated two-dimensional Heisenberg model: Random phase approximation and functional renormalization group, [Phys. Rev. B 81, 144410 (2010).](http://journals.aps.org/prb/abstract/10.1103/PhysRevB.81.144410)
