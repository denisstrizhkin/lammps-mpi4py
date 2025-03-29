import lammps_mpi4py


def main(lmp: lammps_mpi4py.LammpsMPI):
    # Now you can write code in a serial manner
    print(f"Lammps version: {lmp.version()}")


if __name__ == "__main__":
    lammps_mpi4py.run(main)
