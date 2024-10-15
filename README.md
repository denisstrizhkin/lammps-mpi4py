# lammps-mpi4py

## Example

```python
from lammps import lammps                                               
from mpi4py import MPI                                                                         
from lammps_mpi4py import LammpsMPI


def main(lmp):
    print(f"Lammps version: {lmp.version()}"


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    lmp = lammps()
    lmpmpi = LammpsMPI(lmp, comm, 0)

    rank = comm.Get_rank()
    if rank == 0:
        main(lmpmpi)
        lmpmpi.close()
    else:
        lmpmpi.listen()
```
