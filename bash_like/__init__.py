import sys
import os
from typing import Any, Union, Iterator, Tuple, Set


class ShellOperations:
    def __lt__(self, filename: Union[str, bytes, int]) -> str:
        """
        Emulates <filename; Read from filename, return the contents as a string
        """
        with open(filename, "r") as f:
            return f.read()

    def __lshift__(self, filename: Union[str, bytes, int]) -> Iterator[str]:
        """
        Emulates a while-read loop; Read lines from filename, yields an iterator of lines
        Strips whitespace and newlines from the ends of lines, removes empty lines
        """
        with open(filename, "r") as f:
            for line in f:
                ln: str = line.strip()
                if ln:
                    yield ln

    def __or__(self, err: Tuple[Union[str, int], str]) -> str:
        """
        Emulates ${VAR:?Err Msg}
        Given an environment variable (or CLI arg) and a error message,
        returns CLI argument if given, else prints message to stderr and exits
        """
        arg, errmsg = err
        try:
            if isinstance(arg, int):
                return sys.argv[arg]
            else:
                return os.environ[arg]
        except (IndexError, KeyError):
            print(errmsg, file=sys.stderr)
            sys.exit(1)

    def __sub__(
        self,
        info: Tuple[Union[str, int], Any],
    ) -> Any:
        """
        Emulates ${VAR:-default}
        Given an environment variable (or CLI arg), uses that value
        if it exists in the environment, else uses default value
        """
        arg, default = info
        try:
            if isinstance(arg, int):
                return sys.argv[arg]
            else:
                return os.environ.get(arg, default)
        except IndexError:
            return default


SO = ShellOperations()


class Shell:
    allowed_fds: Set[int] = set([1, 2])

    def __init__(self, data: Any):
        if isinstance(data, str):
            self.data: str = data
        else:
            self.data = str(data)

    def __gt__(self, target: Union[int, str], mode: str = "w") -> "Shell":
        """
        If target is Integer (1 or 2), writes to STDOUT and STDERR
        If target is a string, writes to that file
        """
        if isinstance(target, int):
            if target not in self.__class__.allowed_fds:
                raise ValueError(
                    "If integer, target filename must be 1 (for STDOUT) or 2 (for STDERR). Received {}".format(
                        target
                    )
                )
            if target == 1:
                print(self.data, file=sys.stdout, end="")
            if target == 2:
                print(self.data, file=sys.stderr, end="")
        else:
            with open(target, mode) as f:
                f.write(self.data)
        return self

    def __rshift__(self, target: Union[int, str]) -> "Shell":
        """
        Appends string data to the given target
        """
        return self.__gt__(target, mode="a")  # type: ignore[call-arg]


S = Shell
