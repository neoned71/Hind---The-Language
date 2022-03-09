#packages
import argparse
from os import access
import sys

#homemade
from scanner import *
from tokens import TokenTypes,Token 
from utils import *
from abstract_syntax_tree import *
from parser import *
from interpreter import Interpreter


##########END IMPORTS##############

# as scanner
argparser = argparse.ArgumentParser(description='Neoned71 Homemade Language ')
argparser.add_argument('-f','--file',default="-",help="Source file")

args = argparser.parse_args()
# print(args.file)


#Local Global variables
# had_error = False

def main():
    # print("starting the game")
    if(args.file == "-"):
        runPrompt()
    else:
        #get the code from the file!!
        code = open(args.file,'r').read()
        run(code)

        # expr = Binary(
        #     Unary(Token(TokenTypes.MINUS,"-",None,1),Literal(23.0)),#1
        #     Token(TokenTypes.STAR,"*",None,1),
        #     Grouping(Literal(45.03)))#2

        # print(expr.accept())
            # Unary(Token(TokenTypes.MINUS,"-",None,1),Literal(23.0)))
    

    #scan the code for the tokens
    # scanner.Scanner(code)



def runPrompt():
    while(True):
        print(">>",end="")
        try:
            line = input()
            # print(ord(line))
            if not line: break
            run(line)
        except:
            print("see you later")
            break
    print("bbye...")

def run(source):
    scanner = Scanner(source)
    if(had_error): exit(10)
    tokens = scanner.scan()
    # for i in tokens:
    #     print(i)

    parser = Parser(tokens)
    # ast = parser.parse()
    statements = parser.parse()
    interpreter = Interpreter()

    if statements is not None and len(statements)>0:
        # for i in ast:
        # print(ast.accept())
        # print("Tree Evaluation:",end="")
        interpreter.interpret(statements)
        
    else:
        print("parsing failed")
    

if(__name__ == "__main__"):
    main()


###Error handling
