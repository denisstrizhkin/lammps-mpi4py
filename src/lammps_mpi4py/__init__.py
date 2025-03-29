from lammps import lammps  # type: ignore
import functools
from mpi4py import MPI
from typing import Callable, Concatenate, Optional


class LammpsMPIException(Exception): ...


class LammpsMPI:
    def __init__(
        self,
        comm: MPI.Intracomm,
        master: int,
        name: str = "",
        cmdargs: Optional[list[str]] = None,
    ) -> None:
        self._lmp = lammps(name=name, cmdargs=cmdargs, comm=comm)
        self._comm = comm
        self._master = master

    def listen(self) -> None:
        if self._comm.Get_rank() == self._master:
            raise LammpsMPIException("Shouldn't call listen() for master rank")
        while True:
            data = self._comm.recv(source=self._master, tag=0)
            method = getattr(self._lmp, data["method"])
            try:
                method(*data["args"], **data["kwargs"])
            except Exception:
                break
            if data["method"] == "close":
                break

    @staticmethod
    def _lmp_command[C: LammpsMPI, **P, R](
        fn: Callable[Concatenate[C, P], R],
    ) -> Callable[Concatenate[C, P], R]:
        method = fn.__name__

        @functools.wraps(fn)
        def wrapped(self, *args: P.args, **kwargs: P.kwargs) -> R:
            if self._comm.Get_rank() != self._master:
                raise LammpsMPIException("Shouldn't send commands from slave ranks")
            for rank in range(self._comm.Get_size()):
                if rank != self._master:
                    self._comm.send(
                        {"method": method, "args": args, "kwargs": kwargs},
                        dest=rank,
                        tag=0,
                    )
            return getattr(self._lmp, method)(*args, **kwargs)

        return wrapped

    @_lmp_command
    def command(self, cmd: str) -> None:
        return

    @_lmp_command
    def commands_list(self, cmdlist: list[str]) -> None:
        return

    @_lmp_command
    def commands_string(self, multicmd: str) -> None:
        return

    @_lmp_command
    def extract_box(
        self,
    ) -> list:
        return list()

    @_lmp_command
    def file(self, path: str) -> None:
        return

    @_lmp_command
    def get_thermo(self, name: str) -> float | None:
        return float()

    @_lmp_command
    def set_internal_variable(self, name: str, value: float) -> int:
        return int()

    @_lmp_command
    def set_string_variable(self, name: str, value: str) -> int:
        return int()

    @_lmp_command
    def version(self) -> int:
        return int()

    @_lmp_command
    def close(self) -> None:
        return


def run(f: Callable[[LammpsMPI], None]) -> None:
    comm = MPI.COMM_WORLD
    lmp = LammpsMPI(comm, 0)
    if comm.Get_rank() == 0:
        f(lmp)
        lmp.close()
    else:
        lmp.listen()
