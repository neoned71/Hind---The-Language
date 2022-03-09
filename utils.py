import time
from environment import *
from tokens import *

from statements import FunctionStatement
had_error = False

keywords = {}
# keywords["and"]    = TokenTypes.AND
# keywords["class"]  = TokenTypes.CLASS
# keywords["else"]   = TokenTypes.ELSE
# keywords["false"]  = TokenTypes.FALSE
# keywords["for"]    = TokenTypes.FOR
# keywords["fun"]    = TokenTypes.FUN
# keywords["if"]     = TokenTypes.IF
# keywords["nil"]    = TokenTypes.NIL
# keywords["or"]     = TokenTypes.OR
# keywords["print"]  = TokenTypes.PRINT
# keywords["return"] = TokenTypes.RETURN
# keywords["super"]  = TokenTypes.SUPER
# keywords["this"]   = TokenTypes.THIS
# keywords["true"]   = TokenTypes.TRUE
# keywords["var"]    = TokenTypes.VAR
# keywords["while"]  = TokenTypes.WHILE
keywords["aur"]    = TokenTypes.AND
keywords["class"]  = TokenTypes.CLASS
keywords["athwa"]   = TokenTypes.ELSE
keywords["galat"]  = TokenTypes.FALSE
keywords["for"]    = TokenTypes.FOR
keywords["mantra"]    = TokenTypes.FUN
keywords["yadi"]     = TokenTypes.IF
keywords["nil"]    = TokenTypes.NIL
keywords["ya"]     = TokenTypes.OR
keywords["chapo"]  = TokenTypes.PRINT
keywords["return"] = TokenTypes.RETURN
keywords["super"]  = TokenTypes.SUPER
keywords["this"]   = TokenTypes.THIS
keywords["sahi"]   = TokenTypes.TRUE
keywords["dabba"]    = TokenTypes.VAR
keywords["jabtak"]  = TokenTypes.WHILE

def error(line_number,message):
    report(line_number,"",message)


def report(line_number,position,message):
    had_error = True
    print(line_number,message)


class Callable:
    # def __init__(self,arity,call_function) -> None:
    #     self.arity=arity
    #     self.call = call_function

    def call(self,interpreter=None,arguments=None):
        pass

    def arity(self):
        pass

    def string(self):
        pass

class Clock(Callable):
    def call(self,interpreter,arguments):
        # super().call(interpreter, arguments)
        return float(time.time()/1000.0)

    def arity(self):
        return 0

    def string(self):
        return "native function: Clock"

class FunctionCallable(Callable):
    def __init__(self,function_statement:FunctionStatement) -> None:
        self.declaration = function_statement

    def call(self,interpreter,arguments):
        env = Environment(interpreter.environment)
        if len(arguments) != len(self.declaration.params):
            error(interpreter.seek(),"Arguments count dont match")
        
        for i,arg in enumerate(arguments):
            env.define(self.declaration.params[i].lexeme,arg)

        return interpreter.execute_block(self.declaration.body,env)
        
            

    def arity(self):
        return len(self.declaration.params)

    def string(self):
        return "function: "+self.declaration.name
