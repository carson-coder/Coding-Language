import io
import re
import sys


# Args:
# -debug: run in debug mode. Lets you define breakpoints. See var values.

# -dev: debug compiler. dont put in docs

global DEBUG
global Error
global ErrorMsg
global DEV
Error = False
ErrorMsg = "You shouldn't see this"
DEBUG = False
DEV = False
EXIT_ON_ERR = True
PRINT_ERR = True

class Code_Not_Loaded(Exception):
    pass

if "-debug" in sys.argv:
    DEBUG = True
if "-dev" in sys.argv:
    DEV = True

class Buffer():
    buffer = []
    def add(self, cmd):
        self.buffer.append(cmd)
    def remove(self, cmd):
        global Error
        global ErrorMsg
        try:
            self.buffer.remove(cmd)
        except ValueError:
            Error = True
            ErrorMsg = "Error on line: {Line}. Buffer doesn't contain value %s" % (cmd,)

class Compiler():
    def load_code(self, code: str|io.TextIOWrapper):
        """Load code. Supports files, files locations, and raw code.

        Args:
            code (str | io.TextIOWrapper): The code to load. Will close the file automaticly
        """
        
        # File
        if type(code) == io.TextIOWrapper:
            self.code = code.read()
            code.close()
            return
        # File Path
        elif re.search("^[a-zA-Z](:/)", code):
            with open(code) as codes:
                self.code = codes.read()
                codes.close()
        #Code
        else:
            self.code = code
        self.code_loaded = True
    def init(self):
        global EXIT_ON_ERR
        global PRINT_ERR
        if self.code_loaded != True:
            raise Code_Not_Loaded("Run load_code() before init()")
        self.parsed_code = self.code.split("\n")
        try:
            if self.parsed_code.index("EXIT_ON_ERR is false") < 2:
                EXIT_ON_ERR = False
                if self.parsed_code.index("PRINT_ERR is false") < 2:
                    PRINT_ERR = False
        except ValueError:
            pass
        self.ready = True

if DEV:
    a = Compiler()
    a.load_code("EXIT_ON_ERR is false")
    a.init()

    print(EXIT_ON_ERR, PRINT_ERR, DEBUG, a.code, a.parsed_code, a.ready, a.code_loaded)