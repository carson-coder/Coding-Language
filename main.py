import io
import re

Error = False
ErrorMsg = "You shouldn't see this"

class Buffer():
    buffer = []
    def add(self, cmd):
        self.buffer.append(cmd)
    def remove(self, cmd):
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
        