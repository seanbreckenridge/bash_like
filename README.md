# bash_like

[![PyPi version](https://img.shields.io/pypi/v/bash_like.svg)](https://pypi.python.org/pypi/bash_like) [![Python 3.6|3.7|3.8|3.9](https://img.shields.io/pypi/pyversions/bash_like.svg)](https://pypi.python.org/pypi/bash_like) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

A small utility library to handle arguments and read/write text to files using bash-like syntax

## Installation

Requires `python3.6+`

To install with pip, run:

    pip install bash_like

---

This creates small helper function/symbols to handle some common patterns when creating python scripts

To use, include the following imports at the top:

```python
from bash_like import S, SO  # (Shell, ShellOperations)
```

| Description                                                           | Bash                                                                                             | bash_like (python)                                                                                               |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| Write a string to a file                                              | `echo hello > file.txt`                                                                          | `S("hello\n") > "file.txt"`                                                                                        |
| Append to file                                                        | `echo hello >> file.txt`                                                                         | `S("hello\n") >> "file.txt"`                                                                                       |
| Print to STDERR (2)                                                   | `echo error 1>&2`                                                                                | `S("error\n") > 2`                                                                                                 |
| Print to STDOUT (1)                                                   | `echo hello`                                                                                     | `S("hello\n") > 1`                                                                                                 |
| Read text from a file                                                 | `<input.txt`                                                                                     | `SO < "input.txt"`                                                                                               |
| Read lines from a file (strips, and ignores empty lines)              | `while read line; do echo line; done <input.txt`                                                 | `SO << "input.txt"`                                                                                              |
| Get Environment or CLI argument, If not present, print error and exit | `FILE="${1:?Provide file as first CLI arg}" ;VAL="${CONFIG_VAR:?Error - CONFIG_VAR is not set}"` | `file = SO \| (1, "Provide file as first CLI arg"); val = SO \| ("CONFIG_VAR", "Error - CONFIG_VAR is not set")` |
| Get Environment or CLI argument, If not present, use default          | `FILE="${1:-output.txt}"; VAL="${DIFFERENCE:-5}"`                                                | `file = SO - (1, "output.txt"); val = SO - ("DIFFERENCE", 5)`                                                    |

Of course, you don't have to use `hello` for the strings, wrapping any python string in `S` allows you to quickly redirect it to a file, without having to do the `with` block:

As a more complete example, this takes a file as input, and writes the contents of that file in lower case to `${APP_DATA:-$HOME/.local/share}/....`. It:

- uses the first CLI argument as the input file, else prints an error and exits
- uses the second CLI argument as basename, else defaults to `output.txt`
- uses `APP_DATA` (some environment variable for your application) if present, else defaults to `~/.local/share`

`APP_DATA=~/.local/appdata python3 main.py input.txt fout.txt` would write to `~/.local/appdata/fout.txt`

```python3
from os import path, environ
from time import time

from bash_like import S, SO

# the 1 and 2 correspond to sys.argv[1] and sys.argv[2], if they're present
inp = SO | (1, "Error: no input file provided as first argument")
out = SO - (2, "output.txt")
app_data = SO - ("APP_DATA", path.join(environ["HOME"], ".local", "share"))

# read file, casefold (lowercase), and write to file
S((SO < inp).casefold()) > path.join(app_data, out)
# append current time to a temporary logfile
S(f"{time()}\n") >> "/tmp/time.log"
```
