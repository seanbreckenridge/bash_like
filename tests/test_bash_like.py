import sys
import os
import tempfile
from typing import Any

import pytest

from bash_like import SO, S

this_dir = os.path.abspath(os.path.dirname(__file__))
input_file = os.path.join(this_dir, "input.txt")


def test_read_file() -> None:
    assert "1\n\n2\n3\n4\n5\n" == (SO < input_file)


def test_iterate_read_file() -> None:
    assert ["1", "2", "3", "4", "5"] == list(SO << input_file)


def test_environ_or_exit_succeeds() -> None:
    os.environ["SOME_ARG"] = "5"
    val = SO | ("SOME_ARG", "couldnt find SOME_ARG as an environment variable")
    assert val == "5"


def test_environ_or_exit_fails(capsys: Any) -> None:
    if "SOME_ARG" in os.environ:
        del os.environ["SOME_ARG"]
    with pytest.raises(SystemExit):
        SO | ("SOME_ARG", "couldnt find SOME_ARG as an environment variable")
    captured = capsys.readouterr()
    captured_err = captured.err.splitlines()
    assert len(captured_err) == 1
    assert captured_err[0] == "couldnt find SOME_ARG as an environment variable"


def test_sys_argv_succeeds() -> None:
    sys.argv = ["main.py", "5", "2"]
    val = SO | (1, "No argument")
    assert val == "5"


def test_sys_argv_fails(capsys: Any) -> None:
    sys.argv = []
    with pytest.raises(SystemExit):
        SO | (1, "Provide the number of things to do as the first CLI argument!")
    captured = capsys.readouterr()
    captured_err = captured.err.splitlines()
    assert len(captured_err) == 1
    assert (
        captured_err[0]
        == "Provide the number of things to do as the first CLI argument!"
    )


def test_default_sys_uses_default() -> None:
    sys.argv = ["main.py", "5", "2"]
    val = SO - (5, "100")
    assert val == "100"


def test_default_environ_uses_default() -> None:
    if "SOME_ARG" in os.environ:
        del os.environ["SOME_ARG"]
    val = SO - ("SOME_ARG", "120")
    assert val == "120"


def test_default_sys_uses_item() -> None:
    sys.argv = ["main.py", "5"]
    val = SO - (1, "110")
    assert val == "5"


def test_default_environ_uses_item() -> None:
    os.environ["SOME_ARG"] = "5"
    val = SO - ("SOME_ARG", "130")
    assert val == "5"


def test_write_to_fd(capsys: Any) -> None:
    S("data") > 1
    S("otherdata") > 2
    captured = capsys.readouterr()
    captured_out = captured.out.splitlines()
    assert len(captured_out) == 1
    assert "data" == captured_out[0]
    captured_err = captured.err.splitlines()
    assert len(captured_err) == 1
    assert "otherdata" == captured_err[0]


def test_write_to_file() -> None:
    data = [1, 2, 3, 4, 5]
    f = tempfile.NamedTemporaryFile()
    S("\n".join(map(str, data)) + "\n") > f.name
    with open(f.name) as x:
        assert x.read() == "1\n2\n3\n4\n5\n"
    S("other") >> f.name
    lns = list(SO << f.name)
    assert len(lns) == 6
    list(lns)[-1] == "other"
