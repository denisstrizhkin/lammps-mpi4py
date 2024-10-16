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
        self.lmp = lammps(name=name, cmdargs=cmdargs, comm=comm)
        self.comm = comm
        self.master = master

    def listen(self) -> None:
        if self.comm.Get_rank() == self.master:
            raise LammpsMPIException("Shouldn't call listen() for master rank")
        while True:
            data = self.comm.recv(source=self.master, tag=0)
            method = getattr(self.lmp, data["method"])
            method(*data["args"], **data["kwargs"])
            if data["method"] == "close":
                break

    @staticmethod
    def _lmp_command[
        C: LammpsMPI, **P, R
    ](fn: Callable[Concatenate[C, P], R]) -> Callable[Concatenate[C, P], R]:
        method = fn.__name__

        @functools.wraps(fn)
        def wrapped(self, *args: P.args, **kwargs: P.kwargs) -> R:
            if self.comm.Get_rank() != self.master:
                raise LammpsMPIException("Shouldn't send commands from slave ranks")
            for rank in range(self.comm.Get_size()):
                if rank != self.master:
                    self.comm.send(
                        {"method": method, "args": args, "kwargs": kwargs},
                        dest=rank,
                        tag=0,
                    )
            return getattr(self.lmp, method)(*args, **kwargs)

        return wrapped

    @_lmp_command
    def command(self, cmd: str) -> None:
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
    def version(self) -> int:
        return int()

    @_lmp_command
    def close(self) -> None:
        return
