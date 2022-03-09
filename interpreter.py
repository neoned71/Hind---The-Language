

# from ast import operator
# from turtle import right
from ast import keyword
from sympy import fu
from environment import Environment
from abstract_syntax_tree import Expression, FunctionCall,Grouping,Literal, Logical, Unary,Binary, VariableAccess,Assignment
from statements import BlockStatement, FunctionStatement, ReturnStatement,WhileStatement, ExpressionStatement, IfStatement, PrintStatement, Statement,VariableStatement
from tokens import TokenTypes,Token
from typing import List

from utils import Clock, FunctionCallable


class Interpreter:
    tree=None
    globals:Environment = None

    def __init__(self) -> None:
        self.globals = Environment()
        self.globals.define("clock",Clock())
        self.environment = Environment(self.globals)


    #API function
    def interpret(self,statements:List[Statement])->None:
        try:
           for statement in statements:
               self.execute(statement)
        except Exception as exp:
            print(exp.args)

    def expression_statement(self,statement:ExpressionStatement):
        self.evaluate(statement.expression)
        return None

    def print_statement(self,statement:PrintStatement):
        #print(statement)
        value=self.evaluate(statement.expression)
        #print(value)
        # match(value):
        #     case True:
        #         value=""
        print(str(value))
        return None

    def variable_statement(self,statement:VariableStatement):
        value=None
        if(statement.initializer_expression != None):
            value = self.evaluate(statement.initializer_expression)
        self.environment.define(statement.name.lexeme,value)
        return None

    def variable_assign_statement(self,expr:Assignment):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name,value)
        return value

    def if_statement(self,statement:IfStatement):
        if(self.is_truthlike(self.evaluate(statement.condition))):
            self.execute(statement.true_branch)
        else:
            self.execute(statement.false_branch)
        return None

    def while_statement(self,statement:WhileStatement):
        while(self.is_truthlike(self.evaluate(statement.condition))):
            self.execute(statement.body)
        return None
        # value=None
        # if(statement.nitializer_expression != None):
        #     value = self.evaluate(statement.initializer_expression)
        # self.environment.define(statement.name.lexeme,value)
        # return None

    def block_statement(self,block:BlockStatement):
        return self.execute_block(block.statements,Environment(enclosing=self.environment))

    def function_statement(self,function:FunctionStatement):
        #call to define the function here!
        callable = FunctionCallable(function)
        # print("function name")
        # print(function.name)
        self.environment.define(function.name,callable)
        pass


    # def return_statement():
    #     pass


    def variable_access_expression(self,expr:VariableAccess):
        # print("accessing variable")
        return self.environment.get(expr.name)

    

    def literal_expression(self,expr:Literal) -> object:
        return expr.value

    def logical_expression(self,expr:Logical):
        left = self.evaluate(expr.left)
        # print(expr.operator.token_type)
        if(expr.operator.token_type == TokenTypes.OR):
            if(self.is_truthlike(left)): return left
        else:
            if(not self.is_truthlike(left)): return left

        return self.evaluate(expr.right)

    def grouping_expression(self,expr:Grouping) -> object:
        return self.evaluate(expr.expression)

    def unary_expression(self,expr:Unary) -> object:
        right = self.evaluate(expr.right)
        
        match(expr.operator.token_type):
            case TokenTypes.BANG:
                return (not self.is_truthlike(right))
            case TokenTypes.MINUS:
                self.checkNumberOperand(expr.operator, right)
                return -float(right)
            case _:
                return None


    def binary_expression(self,expr:Binary)-> object:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match(expr.operator.token_type):
            case TokenTypes.GREATER:
                return float(left) > float(right)
            case TokenTypes.GREATER_EQUAL:
                return float(left) >= float(right)
            case TokenTypes.LESS:
                return float(left) < float(right)
            case TokenTypes.LESS_EQUAL:
                return float(left) <= float(right)
            case TokenTypes.BANG_EQUAL: return not self.is_equal(left, right)
            case TokenTypes.EQUAL_EQUAL: return self.is_equal(left, right)


            case TokenTypes.MINUS:
                self.check_numeric_oprands(expr.operator, left, right)
                return float(left) - float(right)

            case TokenTypes.SLASH:
                self.check_numeric_oprands(expr.operator, left, right)
                return float(left) / float(right)

            case TokenTypes.STAR:
                self.check_numeric_oprands(expr.operator, left, right)
                return float(left) * float(right)
            
            case TokenTypes.MOD:
                self.check_numeric_oprands(expr.operator, left, right)
                return float(left) % float(right)

            case TokenTypes.PLUS:
                self.check_numeric_oprands(expr.operator, left, right)
                if isinstance(left,str) and isinstance(right,str):
                    return str(left) + str(right)

                if isinstance(left,float) and isinstance(right,float):
                    return float(left) + float(right)

                raise Exception("Need either 2 strings or 2 numbers to be added!")

            case _:
                return None

    def call_expression(self,function:FunctionCall):
        
        call_object=self.environment.get(function.callee.name)
        
        if(call_object.call is None):
            raise Exception("Can only call functions and classes")
        if(len(function.arguments) != call_object.arity()):
            raise Exception("Number of arguments are not matched!")

        arguments=[]
        for arg in function.arguments:
            arguments.append(self.evaluate(arg))

        return call_object.call(interpreter=self,arguments=arguments)

    ###### HELPING FUNCTIONS #########
    def execute(self,statement:Statement):
        # print(statement)
        statement.accept(self)

    def evaluate(self,expr:Expression)->object:
        # print(expr)
        return expr.accept(self)

    def is_truthlike(self,obj:object):
        # print(obj)
        if obj is None: return False
        if isinstance(obj,bool): return bool(obj)
        if isinstance(obj,int): return obj>0
        return True

    def is_equal(self,a:object,b:object):
        if a is None and b is None: return True
        if a is None: return False
        return a==b

    def check_numeric_oprand(self,op:Token,obj:object):
        if isinstance(obj,float): return True
        print("error has occured")
        raise Exception("Value of the operands is not numeric: "+op.lineno)
    
    def check_numeric_oprands(self,op:Token,left:object,right):
        if isinstance(left,float) and isinstance(right,float): return True
        print("error has occured")
        raise Exception("Value of the operands is not numeric: "+op.lineno)

    def execute_block(self,statements, environment):
        previous_environment = self.environment
        ret_value=None
        try:
            self.environment = environment
            # print()


            for statement in statements:
                if isinstance(statement, ReturnStatement):
                    ret_value = self.evaluate(statement.value)
                    break
                self.execute(statement)

        except Exception as exp:
            print(exp)
        finally:
            # print("switching back")
            self.environment = previous_environment
            return ret_value
            # print(id(self.environment))

