---
layout: code
title: NEST Simulator – spiking neural network simulations
Topics: neuroscience, simulation, spiking neural networks, learning, brain function
Link: https://nest-simulator.org
Project Head: https://nest-initiative.org
Contact: users@nest-simulator.org
Members: https://github.com/orgs/nest/people and https://nest-initiative.org
Research Field: Helmholtz Information
Scientific Community: Biology, Medicine, AI
Funding: See https://github.com/nest/nest-simulator/blob/master/ACKNOWLEDGMENTS.md
Repository: https://github.com/nest/nest-simulator
Programming Languages: C++, Python
License: GPL-2.0-or-later
Cite:  <a href="https://doi.org/10.5281/zenodo.8344932" alt="NEST 3.6"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.8344932.svg" alt="DOI"></a>
toc: true
---

- TOC
{:toc}

# NEST Simulator

<a href="https://doi.org/10.5281/zenodo.8344932" alt="NEST 3.6"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.8344932.svg" alt="DOI"></a>

<!-- what is nest? what is it for? -->
NEST is a simulator for spiking neuronal networks. It is used mostly in computational neuroscience to model and study <!-- phenomenons in the functional --> behaviour of large networks of neurons. The models describe single neuron and synapse behaviour and their connections. Different mechanisms of plasticity can be used to investigate artificial learning and help to shed light on the fundamental principles of how the brain works.

<!-- how could I try? -->
NEST is a well tested and efficient tool that works on your laptop and also on the world's largest supercomputers. It is fast and memory efficient, making best use of your multi-core computer or compute cluster. Whether you want to work on a small laptop or the largest supercomputers, NEST can seamlessly scale to your needs.

<!-- what can I do with NEST? -->
A NEST simulation works like a physiological experiment but inside a computer. Perform your own experiments using assemblies of virutal neurons and different  stimulating and recording devices. <!-- 
.
what are the building blocks I can play with? -->
It comes loaded with numerous state-of-the art neuron models. Textbook standards like integrate-and-fire and Hodgkin-Huxley type models are available alongside high quality implementations of models published by the neuroscience community. NESTML provides a framework to create models without the need for detailed programming knowledge, and makes creating your own neuron and synapse models a breeze! Visit [NESTML](https://nestml.readthedocs.io/en/latest/) to find out more.

<!-- How can I build stuff? -->
NEST offers convenient and efficient commands to define and connect large networks, ranging from algorithmically determined connections to data-driven connectivity. Create connections between neurons using numerous synapse models from STDP to gap junctions.

<!-- background, community and friends -->
The simulator is developed and continuously improved by the NEST community around the globe to stay up-to-date and fit for the latest research questions. NEST developers are using continuous-integration based workflows in order to maintain high code quality standards for correct and reproducible simulations.

<!-- Community building -->
NEST has fostered a large community of experienced developers and amazing users, who actively contribute to the project. Our community extends to related projects, like the teaching tool [NEST Desktop](https://nest-desktop.readthedocs.io/en/latest/), cross-simulator languages like [PyNN](https://neuralensemble.org/docs/PyNN/) and neural activity analysis tools like [Elephant](https://elephant.readthedocs.io/en/latest/).

With the combination of AI and neuromorphic computing, both sides can advance from findings from both worlds. Connect your NEST simulation to [neurorobotics](https://neurorobotics.net/) and add the "eyes" and "muscles" to complete the sensor-motor loop and tackle the problem of embodiment.


## Activities

* Participated in continuous benchmarking hackathon
* Presented documentation related talk to HiRSE Seminar Series
* Improved CI chain with new RSE best practice tools
