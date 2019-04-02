# Lampy

Numpy for Open-Lambda.

![image-20190402012347530](/Users/mike/Library/Application Support/typora-user-images/image-20190402012347530.png)

[TOC]

## What should people care about `Lampy`

### Parallelism 

`Lampy` should be a cheap, scalable solution for parallel computing. Conversely, it means that `Lampy` should not target on any problem that is not parallelizable. The optimization of these problems should totally depend on users.

Maybe `Lampy` should be clever —  It should find opportunity to parallelize computation without user to specify. Maybe `Lampy` should be stupid — it only allow some manual hints (like numpy -  `@elemwise`, `@reduce`, `@sum`) to start parallel computation. In that case, we should treat `Lampy` similar to a parallel region in CUDA/OpenMP, or an MPI-connected system.

One thing that could be different from CUDA/OpenMP is that we don't necessarily need to follow the host-device model (or master-slave model) of computation. The host can resign the ability to orchestrate computation to some chosen lambda funciton, and the orchestration power can change depending on the life of a lambda function, data locality, and other factors.



### Throughput 







## Dev Aspects

### Semester Goal: Fisher Semi-Linear Discriminant

- Scheduling: 
  - Generate computation dependency graph
  - Parallelism 
- Data I/O: 
  - 
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
  - [ ] Use compiled data dependency graph to <u>request lambda resource (**scheduler team**)</u>
  - [ ] 
- [ ] Data I/O
  - [x] Fetch Data from remote device
  - [ ] Create a `lampy-server` class for remote access



### Operation & Computation

#### Create simple DAG 



#### Load/Dump Data Dependency Graph



####  (Pseudo) Estimate Computation Time







### Data I/O

#### Fetch Data from remote device

**Goal**

- Issue a **lambda-call** to request the file from a remote lambda repo
- Request **piece** of data — a slice of data, instead of the whole data.



**Current Stage**: `v0.0.2` - load remote matrix file

```python
import lampy as np
# Load Data from local/remote file
base_dir = os.getcwd()
matrix_path = os.path.join(base_dir, '../dump/a.np')
a = LamObject(matrix_path)
b = LamObject(matrix_path)
d = LamObject([4])

c = a + b + d
c.run()
print(c) # [6, 8, 10]
```



##### `v0.0.2`: load remote matrix file

##### `v0.0.3`: Dispatch a lambda call to issue the request of data



## References

- [Tensorflow: A System for Large-Scale Machine Learning](https://www.tensorflow.org/about/bib)
- [Tensorflow: Large-Scale Machine Learning on Heterogeneous Distributed Systems](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45166.pdf)
- [Thrust](https://github.com/thrust/thrust/wiki)
- [Numpy](https://arxiv.org/pdf/1102.1523.pdf)





