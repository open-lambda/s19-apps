# Lampy

Numpy for Open-Lambda.

[TOC]

## What people care

- **Parallelism.** Open-Lambda should not solve problem that is not parallelizable.





## Dev Aspects

### Semester Goal: Fisher Semi-Linear Discriminant

- Scheduling: 
  - Generate computation dependency graph
  - Parallelism 
- Data I/O: 
- Operation: 
  - Support common math operations
  - Test on Fisher Semi-Linear Discriminant Methods



## Components



- [ ] Operation & Computation
  - [x] Create simple DAG 
  - [ ] Load/Dump Data Dependency Graph (visualization and scheduling)
  - [ ] Estimate Computation Time (based on matrix size and operations)
  - [ ] Extend the DAG idea to a directed graph (for loops etc.) 
- [ ] Scheduling
  - [ ] 
- [ ] Data I/O
  - [x] Fetch Data from remote device
  - [ ] Create a `lampy-server` class for remote access
    - [ ] Request like a URL



### Operation & Computation

#### Create simple DAG 



#### Load/Dump Data Dependency Graph



####  (Pseudo) Estimate Computation Time







### Data I/O

#### Fetch Data from remote device

This step is to 

```python
import lampy as np
# Load Data from local/remote file
matrix_a = ""
matrix_b = ""
a = np.array()
b = np.array()
c = a + b
c.run()
```



##### `v0.0.2`: load remote matrix file

##### `v0.0.3`: Dispatch a lambda call to issue the request of data



## References

- [Tensorflow: A System for Large-Scale Machine Learning](https://www.tensorflow.org/about/bib)
- [Tensorflow: Large-Scale Machine Learning on Heterogeneous Distributed Systems](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45166.pdf)
- [Thrust](https://github.com/thrust/thrust/wiki)
- [Numpy](https://arxiv.org/pdf/1102.1523.pdf)
