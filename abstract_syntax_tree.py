
from tokens import TokenTypes,Token
from typing import List

class Expression:
    def __init__(self) -> None:
        pass
        # print("expression created")

    #for getting overriden by derived classes
    def accept(self,interpreter=None):
        print("[!Error:Base Class]")

    def parenthesize(self,name:str,expressions):
        ret="("+name
        for exp in expressions:
            ret+=" "
            ret+=str(exp.accept())
        ret+=")"
        return ret

class Binary(Expression):
    def __init__(self,left:Expression,operator:Token,right:Expression) -> None:
        # super().__init__()
        self.left= left
        self.right= right
        self.operator = operator

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.binary_expression(self)
        return self.parenthesize(self.operator.lexeme,[self.left,self.right])



class Grouping(Expression):
    def __init__(self,expr:Expression) -> None:
        super().__init__()
        self.expression=expr

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.grouping_expression(self)
        # print("Accepting Grouping")
        return self.parenthesize("Group",[self.expression])

class Literal(Expression):
    def __init__(self,value:object) -> None:
        super().__init__()
        self.value= value

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.literal_expression(self)
        # print("Accepting Literal")
        if (self.value is None): return "nil"
        return str(self.value)

class Unary(Expression):
    def __init__(self,operator:Token,right:Expression) -> None:
        super().__init__()
        self.right= right
        self.operator = operator

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.unary_expression(self)
            
        # print("Accepting Unary")
        return self.parenthesize(self.operator.lexeme, [self.right])


class VariableAccess(Expression):
    name=None
    def __init__(self,name:Token) -> None:
        self.name=name.lexeme
        

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.variable_access_expression(self)


class Assignment(Expression):
    def __init__(self,name:Token,value:Expression) -> None:
        self.name=name
        self.value = value
        

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.variable_assign_statement(self)

class Logical(Expression):
    def __init__(self,left:Expression,operator:Token,right:Expression) -> None:
        # super().__init__()
        self.left= left
        self.right= right
        self.operator = operator

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.logical_expression(self)
        return self.parenthesize(self.operator.lexeme,[self.left,self.right])

class FunctionCall(Expression):
    def __init__(self,callee:Expression, parenthesis:Token, arguments:List[Expression]) -> None:
        # super().__init__()
        self.callee = callee
        self.parenthesis = parenthesis
        self.arguments = arguments

    def accept(self,interpretor=None):
        if(interpretor is not None):
            return interpretor.call_expression(self)



