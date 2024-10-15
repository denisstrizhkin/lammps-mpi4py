# lammps-mpi4py

## Example

```python
from lammps import lammps                                               
from mpi4py import MPI                                                                         
from lammps_mpi4py import LammpsMPI


def main(lmp):
    # Now you can write code in a serial manner
    print(f"Lammps version: {lmp.version()}")


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    lmp = lammps()
    lmpmpi = LammpsMPI(lmp, comm, 0)

    rank = comm.Get_rank()
    size = comm.Get_size()
    print(f"rank {rank} of {size}")
    if rank == 0:
        main(lmpmpi)
        lmpmpi.close()
    else:
        lmpmpi.listen()
```

run

```console
> mpirun -n 4 python example.py
LAMMPS (29 Aug 2024)
WARNING: Using I/O redirection is unreliable with parallel runs. Better to use the -in switch to read input files. (src/lammps.cpp:571)
OMP_NUM_THREADS environment is not set. Defaulting to 1 thread. (src/comm.cpp:98)
  using 1 OpenMP thread(s) per MPI task
Total wall time: 0:00:00
rank 0 of 4
Lammps version: 20240829
rank 1 of 4
rank 2 of 4
rank 3 of 4
```
