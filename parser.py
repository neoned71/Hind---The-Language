from typing import List

from more_itertools import consume
from sympy import Expr
from tokens import TokenTypes
from abstract_syntax_tree import *
from statements import *
from utils import error


class Parser:
    tokens=[]
    current = 0 
    def __init__(self,tokens) -> None:
        self.tokens = tokens
        # print(tokens)

    def parse(self)->List[Statement]:#returns list of statements
        statements = []
        # while (not self.is_at_end()): 
        #     statements.append(self.declaration())
        
        # return statements
        try:
            while (not self.is_at_end()): 
                statements.append(self.declaration())
        
            return statements
        except Exception as exp:
            print(exp.args[0])
            return None

    def declaration(self) -> Statement:
        if(self.match([TokenTypes.FUN])): return self.function_declaration()
        if(self.match([TokenTypes.VAR])): return self.variable_declaration()
        return self.statement()
        # try:
            # if(self.match([TokenTypes.VAR])): return self.variable_declaration()
            # return self.statement()
        # except Exception as exp:
        #     self.synchronize()
        #     print(exp.args)
        
    def statement(self):
        if (self.match([TokenTypes.PRINT])): return self.print_statement()
        if (self.match([TokenTypes.IF])): return  self.if_statement()
        if (self.match([TokenTypes.WHILE])): return  self.while_statement()
        if (self.match([TokenTypes.RETURN])): return  self.return_statement()
        if (self.match([TokenTypes.LEFT_BRACE])): return  BlockStatement(self.create_block())
        return self.expression_statement()


    def expression_statement(self):
        value = self.expression()
        self.consume(TokenTypes.SEMICOLON,"Expected ';' after each statement!")
        return ExpressionStatement(value)

    def create_block(self):
        statements = []
        
        while(not self.check(TokenTypes.RIGHT_BRACE) and not self.is_at_end()):
            statements.append(self.declaration())

        self.consume(TokenTypes.RIGHT_BRACE,"Expected '}' after block")
        return statements

    def if_statement(self):
        self.consume(TokenTypes.LEFT_PAREN,"Expected '(' after 'if'")
        condition = self.expression()
        self.consume(TokenTypes.RIGHT_PAREN,"Expected ')' after if condition")

        true_branch = self.statement()
        false_branch = None

        if(self.match([TokenTypes.ELSE])):
            false_branch = self.statement()

        return IfStatement(condition,true_branch,false_branch)

    def while_statement(self):
        self.consume(TokenTypes.LEFT_PAREN,"Expected '(' after 'while'")
        condition = self.expression()
        self.consume(TokenTypes.RIGHT_PAREN,"Expected ')' after if condition")

        body = self.statement()

        return WhileStatement(condition,body)

    def print_statement(self):
        value = self.expression()
        # print("sada")
        self.consume(TokenTypes.SEMICOLON,"Expected ';' after each statement!")
        return PrintStatement(value) 

    def return_statement(self):
        value = self.expression()
        # print("sada")
        self.consume(TokenTypes.SEMICOLON,"Expected ';' after each statement!")
        return ReturnStatement(value)

    def variable_declaration(self):
        name = self.consume(TokenTypes.IDENTIFIER,"Expected Variable name!") 
        initializer = None
        if(self.match([TokenTypes.EQUAL])):
            initializer = self.expression()

        self.consume(TokenTypes.SEMICOLON,"Expected ';' after variable declaration!")
        return VariableStatement(name,initializer)

    def function_declaration(self):
        name = self.consume(TokenTypes.IDENTIFIER,"Expected function name.") 
        arguments = self.arguments()
        self.consume(TokenTypes.LEFT_BRACE,"Expected '{' for function body!")
        body= self.create_block()
        return FunctionStatement(name.lexeme,arguments,body)

    def arguments(self):
        self.consume(TokenTypes.LEFT_PAREN,"Expected '(' for arguments!")
        args=[]
        if not self.check(TokenTypes.RIGHT_PAREN):
            args.append(self.consume(TokenTypes.IDENTIFIER,"Expected parameter name."))
            while(self.match([TokenTypes.COMMA])):
                if len(args)>255: error(self.peek(),"Cannot have more than 255 arguments.")
                args.append(self.consume(TokenTypes.IDENTIFIER,"Expected parameter name."))

        self.consume(TokenTypes.RIGHT_PAREN,"Expected ')' after arguments.")

        return args

    def expression(self)->Expression:
        v =self.assignment()
        # print(v)
        return v

    def assignment(self):
        # print("yes")
        expr = self.OR()

        if(self.match([TokenTypes.EQUAL])):
            equals = self.previous()
            value = self.assignment()
            # print("yess")
            if(isinstance(expr,VariableAccess)):
                name=expr.name
                return Assignment(name,value)
            error(equals.line,"Invalid Assignment Statement")
        return expr

    def OR(self):
        expr = self.AND()

        while(self.match([TokenTypes.OR])):
            operator = self.previous()
            right= self.AND()
            expr = Logical(expr,operator,right)

        return expr

    def AND(self):
        expr = self.equality()

        while(self.match([TokenTypes.AND])):
            operator = self.previous()
            right= self.equality()
            expr = Logical(expr,operator,right)

        return expr

    def equality(self):
        # print("inside equality")
        # equality → comparison ( ( "!=" | "==" ) comparison )* ;
        expr=self.comparison()

        while(self.match([TokenTypes.EQUAL_EQUAL,TokenTypes.BANG_EQUAL])):
            operator = self.previous()
            right=self.comparison()
            expr= Binary(expr,operator,right)

        # print(expr.accept())
        # print(expr.value)
        return expr

    def comparison(self):
        # comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
        expr = self.term()

        while(self.match([TokenTypes.GREATER,TokenTypes.GREATER_EQUAL,TokenTypes.LESS,TokenTypes.LESS_EQUAL])):
            operator = self.previous()
            right= self.term()
            expr = Binary(expr,operator,right)
        
        return expr

    def term(self):
        # term → factor ( ( "-" | "+" ) factor )* ;
        expr = self.factor()

        while(self.match([TokenTypes.MINUS,TokenTypes.PLUS])):
            operator = self.previous()
            right= self.factor()
            expr = Binary(expr,operator,right)
        
        # print(expr.value)
        return expr

    def factor(self):
        #factor → unary ( ( "/" | "*" ) unary )* ;
        expr = self.unary()
        # print(expr.value)
        while(self.match([TokenTypes.SLASH,TokenTypes.STAR])):
            operator = self.previous()
            right= self.unary()
            expr = Binary(expr,operator,right)
        
        # print(expr)
        return expr


    def unary(self):
        # unary  → ( "!" | "-" ) unary | call ;
        if(self.match([TokenTypes.BANG,TokenTypes.MINUS])):
            operator = self.previous()
            right= self.unary()
            u=Unary(operator,right)
            return u

        # print("hello")

        return self.call()

    def call(self):
        # call           → primary ( "(" arguments? ")" )* ;
        expr = self.primary()
        while(True):
            if(self.match([TokenTypes.LEFT_PAREN])):
                expr = self.finish_call(expr)
            else:
                break

        return expr

    def finish_call(self,expr:Expression):
        arguments = []
        if(not self.check(TokenTypes.RIGHT_PAREN)):
            arguments.append(self.expression())
            while(self.match([TokenTypes.COMMA])):
                if(len(arguments)>255):
                    error(self.peek(),"Cannot have more than 255 characters")
                arguments.append(self.expression())

        token = self.consume(TokenTypes.RIGHT_PAREN,"Expected ')' after arguments")
        return FunctionCall(expr,token,arguments)

    def primary(self):
        # primary → IDENTIFIER | NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
        
        if(self.match([TokenTypes.FALSE])): return Literal(False)
        if(self.match([TokenTypes.TRUE])): return Literal(True)
        if(self.match([TokenTypes.NIL])): return Literal(None)

        if(self.match([TokenTypes.IDENTIFIER])):
            return VariableAccess(self.previous())
        
        if(self.match([TokenTypes.NUMBER,TokenTypes.STRING])):
            # print(self.previous())
            l=Literal(self.previous().literal)
            # print(l.value)
            return l

        if(self.match([TokenTypes.LEFT_PAREN])):
            expr = self.expression()
            self.consume(TokenTypes.RIGHT_PAREN,"Missing )")
            return Grouping(expr)

        raise Exception( "Expected primary: "+ str(self.peek()))

#### Helping functions ###
    def match(self,tokens):
        for t in tokens:
            if(self.check(t)):
                self.advance()
                return True
            
        return False


    def check(self,token_type:TokenTypes):
        if(self.is_at_end()): return False
        # print(token_type)
        return self.peek().token_type == token_type

    def advance(self):
        if(not self.is_at_end()): self.current+=1
        return self.previous()

    def is_at_end(self):
        return self.peek().token_type==TokenTypes.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self)->Token:
        return self.tokens[self.current - 1]

### ### Exception handling ### ###
    def parse_error(self,token:Token):
        error(token.line,"parsing error")

    def consume(self,token_type:TokenTypes,message:str):
        if(self.check(token_type)): return self.advance()
        raise Exception("Expected:"+ str(token_type)+", but instead, got this:"+str(self.peek()))

    def synchronize(self):
        self.advance()
        while( not self.is_at_end() ):
            if self.previous().token_type == TokenTypes.SEMICOLON: return

            match(self.peek().token_type):
                case TokenTypes.CLASS |TokenTypes.FUN |TokenTypes.VAR | TokenTypes.FOR | TokenTypes.IF | TokenTypes.WHILE | TokenTypes.PRINT:
                    return

            self.advance()
        