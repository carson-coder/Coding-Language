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
Error = 0
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
            Error = 1
            ErrorMsg = "Error on line: {Line}. Buffer doesn't contain value %s" % (cmd,)

def get_type(txt):
    global ErrorMsg
    global Error
    """Get type of string

    Args:
        txt (str): the text to get type of
    """
    if txt.count("\"") == 2:
        return(str)
    elif txt.isdigit():
        return(int)
    else:
        Error = 1
        ErrorMsg = f"{txt} is not a str or int"
        return(None)

def err_check(self):
    global ErrorMsg
    global Error
    """Checks if a error has been raised
    """
    ErrorMsg = ErrorMsg.replace("{Line}", str(self.line))
    if Error == 0:
        return
    elif Error == 1:
        if PRINT_ERR:
            print(f"Error: {ErrorMsg}")
        if EXIT_ON_ERR:
            exit()
        else:
            error = 0
    else:
        print(f"Critical Error: {ErrorMsg}")
        exit()
class Compiler():
    line = 0
    code_loaded = False
    ready = False
    vars = {}
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
        self.parsed_code = self.code.replace("\n", " ").split(" ")
        while "" in self.parsed_code:
            self.parsed_code.remove("")
        try:
            if self.code.split("\n").index("EXIT_ON_ERR is false") < 2:
                EXIT_ON_ERR = False
                if self.code.split("\n").index("PRINT_ERR is false") < 2:
                    PRINT_ERR = False
        except ValueError:
            pass
        self.ready = True
        print("[--------------Compiler has been initalized--------------]")
    def run(self):
        global Error
        global ErrorMsg
        if not(self.ready and self.code_loaded):
            raise Code_Not_Loaded("Code has not been initalized. run init() to initialize code after loading")

        # Run Code
        
        # Parse More
        
        strtxt = ""
        string = False
        out_code = []
        func = False
        func_code = []
        
        for i in self.parsed_code:
            if "{" in i:
                func_code.append(out_code[len(out_code) - 1])
                out_code.remove(out_code[len(out_code) - 1])
                func = True
            elif "}" in i:
                func = False
                out_code.append(func_code.copy())
                func_code = []
            add_list = func_code if func else out_code
            if i.count("\"") == 1:
                string = not string
                if not string:
                    add_list.append(strtxt)
                    strtxt = ""
            if string:
                strtxt += i
            elif i.count("\"") == 2:
                    strtxt = i[i.index("\""):i.find("\"", i.index("\""))]
                    add_list.append(strtxt)
                    strtxt = ""
            else:
                add_list.append(i.replace("{", ""))
        self.good_code = out_code
        
        # Make sure there is a start
        start = False
        for i in self.good_code:
            if i[0].lower() == "start":
                if start: ErrorMsg, Error = "Too many start positions", 2
                start = True
        if not start: ErrorMsg, Error = "Start not found", 2
        
        err_check(self)
        
        # self.line = self.parsed_code.index("start {") + 1
        # while self.line < len(self.parsed_code):
        #     i = self.parsed_code[self.line]
        #     err_check(self)
        #     parts = i.split(" ")
        #     while "" in parts:
        #         parts.remove("")
                
        #     # Check for varible definition
        #     if "is" in parts and "if" not in parts:
        #         if len(parts) != 3 or get_type(parts[2]) == None:
        #             Error = 2
        #             ErrorMsg = "Var Definition on line {Line} has more or less then 3 words (%s)" % (len(parts),)
        #             err_check(self)
        #         else:
        #             a = get_type(parts[2])
        #             self.vars[parts[0]] = a(parts[2])
            
            
        #     self.line += 1
        
        
if DEV:
    a = Compiler()
    a.load_code("EXIT_ON_ERR is false\nstart {\nA = \"A\"\nB =    10\n}")
    a.init()
    a.run()

    #print(EXIT_ON_ERR, PRINT_ERR, DEBUG, a.code, a.parsed_code, a.ready, a.code_loaded, a.good_code)
    