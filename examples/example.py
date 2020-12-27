from os import path, environ, makedirs
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
