from mpi4py import MPI
from lammps_mpi4py import LammpsMPI


def main(lmp: LammpsMPI):
    # Now you can write code in a serial manner
    print(f"Lammps version: {lmp.version()}")


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    lmp = LammpsMPI(comm, 0)

    rank = comm.Get_rank()
    size = comm.Get_size()
    print(f"rank {rank} of {size}")
    if rank == 0:
        main(lmp)
        lmp.close()
    else:
        lmp.listen()
