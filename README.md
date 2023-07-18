# SymmetryDetectionForQuantumSim
copyright  “Copyright (c) 2023 Alliance for Sustainable Energy, LLC”
# Code for *Automated detection of symmetry-protected subspaces in quantum simulations*
This is the repository which hosts all code for the manuscript [here](https://arxiv.org/abs/2302.08586). The repository is organized as follows:

+ `Tutorial.ipynb`: an overview of how to use our implementation of the algorithms in the manuscript. Demonstrates automated symmetry discovery and post-selection for dynamics in the Heisenberg-XXX model.
+ `QuantumEmulationGenerateData.ipynb`: a notebook to emulate ideal and noisy data from a quantum computer, for the exemplary models in the manuscript.
+ `GatherData.ipynb`: a notebook to analyze quantum data and create the figures used in the manuscript. Also creates additional figures, like population plots, which were not included in the manuscript.
+ `sps_detection.py`: a Python module which hosts our implementation of the manuscript's algorithms.
+ `circuits_warehouse.py`: a box of Python functions which create Cirq circuits to implement our quantum simulations in the gate model.

We do not guarantee any continued support or reliability with this repository; this repository is solely for educational purposes. The exact data used in our manuscript's simulations is hosted elsewhere.