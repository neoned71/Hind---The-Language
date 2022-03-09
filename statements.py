
from typing import List
from abstract_syntax_tree import Expression
# from interpreter import Interpreter
from tokens import TokenTypes,Token

class Statement:
    # expression=None
    def __init__(self) -> None:
        pass
        # print("expression created")

    #for getting overriden by derived classes
    def accept(self,interpreter=None):
        print("[!Error:Base Class]")

class ExpressionStatement(Statement):
    def __init__(self,expr:Expression) -> None:
        self.expression= expr
        

    def accept(self,interpreter=None):
        if(interpreter is not None):
            # interpretor.
            return interpreter.expression_statement(self)
        # print("Accepting Binary")
        # return self.parenthesize(self.operator.lexeme,[self.left,self.right])


class PrintStatement(Statement):
    def __init__(self,expr:Expression) -> None:
        # print(expr)
        self.expression= expr

    def accept(self,interpreter=None):
        if(interpreter is not None):
            # print(self.expression)
            return interpreter.print_statement(self)

class VariableStatement(Statement):
    def __init__(self,name:Token,expr:Expression) -> None:
        self.initializer_expression=expr
        self.name=name
        

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.variable_statement(self)


class BlockStatement(Statement):
    statements=[]
    def __init__(self,statements) -> None:
        self.statements = statements
        

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.block_statement(self)

class IfStatement(Statement):
    def __init__(self,condition:Expression,true_branch:Statement,false_branch:Statement) -> None:
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
        

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.if_statement(self)



class WhileStatement(Statement):
    def __init__(self,condition:Expression,body:Statement) -> None:
        self.condition = condition
        self.body = body
        

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.while_statement(self)



class FunctionStatement(Statement):
    def __init__(self,name:str,params:List[Token],body:List[Statement]) -> None:
        self.name=name
        self.params = params
        self.body = body
        

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.function_statement(self)

class ReturnStatement(Statement):
    def __init__(self,value:object) -> None:
        self.value=value
        

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.return_statement(self)





