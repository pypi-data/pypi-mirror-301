# Datamate

Datamate is a lightweight data and configuration management framework for structuring data in machine learning projects on a hierarchical filesystem.

Datamate provides a simple framework to work with heterogenous data by automating
input and output of arrays and configurations to disk.
It provides an interface to the system's filesystem through pointers to files
and representations of the hierarchical structure.

Typical usecases are:

- automating pathing and orchestrating data
- seamless input and output operations to a hierarchical filesystem
- keep track of configurations, e.g. for preprocessing, experiments, analyses
- structured preprocessing with minimal overhead code---cause configuration-based, preprocessed data can automatically be computed only once and then referenced to
- for instance to skip slow computations when restarting the kernel in your `everything_in_here.ipynb` notebook
- interactive prototyping in data-heterogenous applications: hierarchical file views in notebooks, pandas integration, configuration diffs, simultaneous write and read

# Examples

Datamate's `Directory` instances can point to (processed) data on the disk (relative to a root directory),
allowing seamless I/O.

E.g., to store a numpy array

```python
>>> import datamate
>>> datamate.set_root_dir("./data")
>>> directory = datamate.Directory("experiment_01")  # pointer to ./data/experiment_01
>>> directory.array = np.arange(5)  # creates parent directory and writes array to h5 file
>>> directory
experiment_01/ - Last modified: April 04, 2022 08:24:56
└── array.h5

displaying: 1 directory, 1 files
```

To retrieve the array:

```python
>>> import datamate
>>> datamate.set_root_dir("./data")
>>> directory = datamate.Directory("experiment_01")
>>> directory.array[:]
array([0, 1, 2, 3, 4])
```

More detailed examples in `examples/01. Introduction to Datamate.ipynb`.

# Installation

Using pip:

`pip install datamate`

# Related frameworks

Datamate is adapted from [artisan](https://github.com/MasonMcGill/artisan) to focus on flexibility in interactive jupyter notebooks with only optional configuration and type enforcement.

Because cloud-based and relational database solutions for ML-workflows can be little
beginner friendly or little flexible, Datamate is simply based on I/O of arrays and configurations on
disk with pythonic syntax, and it targets interactive and notebook-based workflows.

# Contribution

Contributions welcome!
