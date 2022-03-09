from numpy import void
from utils import *
from email.policy import default
from tokens import TokenTypes,Token



class Scanner:
    start=0
    current=0
    line=1
    tokens=[]

    def __init__(self,source):
        self.source = source
        # print(source)


    def scan(self) :
        while(not self.is_at_end()):
            self.start = self.current
            self.get_tokens()

        self.tokens.append(Token(TokenTypes.EOF,"",None,self.line))
        return self.tokens

    def get_tokens(self):
        c=self.advance()
        match c:
            case '(': self.add_tokens(TokenTypes.LEFT_PAREN); return
            case ')': self.add_tokens(TokenTypes.RIGHT_PAREN); return
            case '{': self.add_tokens(TokenTypes.LEFT_BRACE); return
            case '}': self.add_tokens(TokenTypes.RIGHT_BRACE); return
            case ',': self.add_tokens(TokenTypes.COMMA); return
            case '.': self.add_tokens(TokenTypes.DOT); return
            case '-': self.add_tokens(TokenTypes.MINUS); return
            case '+': self.add_tokens(TokenTypes.PLUS); return
            case ';': self.add_tokens(TokenTypes.SEMICOLON); return
            case '*': self.add_tokens(TokenTypes.STAR); return
            case '/': self.add_tokens(TokenTypes.SLASH); return
            case '!': self.add_tokens(TokenTypes.BANG_EQUAL if self.match('=') else TokenTypes.BANG); return
            case '=': self.add_tokens(TokenTypes.EQUAL_EQUAL if self.match('=') else  TokenTypes.EQUAL);return
            case '<': self.add_tokens(TokenTypes.LESS_EQUAL if self.match('=') else TokenTypes.LESS);return
            case '>': self.add_tokens(TokenTypes.GREATER_EQUAL if self.match('=') else  TokenTypes.GREATER);return
            case '"': self.string(); return
            case '\t'|' '|'\r': pass
            case '\n': self.line+=1

            case _: 
                if(self.is_digit(c)):
                    self.number()
                elif(self.is_alpha(c)):
                    self.alpha()
                else:
                    error(self.line,"Unexpected Character")#default value if none matched

    def advance(self):
        #move one step ahead and return character at that position
        self.current+=1
        return self.source[self.current-1]

    def is_at_end(self):
        if(self.current >= len(self.source)):
            return True
        else:
            return False

    def add_tokens(self,token_type:TokenTypes,obj=None):
        #add tokens to the Scanner's tokens list!
        self.tokens.append(Token(token_type,self.source[self.start:self.current],obj,self.line))

    def match(self,expected):
        if(self.is_at_end() or self.source[self.current] != expected):
            return False
        else:
            self.current+=1
            return True

    def peek(self):#lookahead
        return '\0' if(self.is_at_end()) else self.source[self.current] 


    def peek_next(self):#lookahead
        return '\0' if((self.current+1) > len(self.source)) else self.source[self.current+1] 

    def string(self) -> void:
        #loop till the other  -->"<--  is found using peek
        while(self.peek()!='"' and not self.is_at_end()):
            if(self.peek()=='\n'):
                self.line+=1
            self.advance()
        
        if(self.is_at_end()):
            error(self.line,"Unterminated String")
            return
        
        self.advance()
        # print(type(self.start),type(self.current))
        value = self.source[(self.start+1):(self.current-1)]
        self.add_tokens(TokenTypes.STRING,obj=value)
        # print(value)
        return
        #advance one more step
        #return start+ to current-1 substring!


    def is_digit(self,c):
        return (c>='0' and c<='9')
    
    

    def number(self):
        while (self.is_digit(self.peek())): self.advance()
        
        if(self.peek()=='.' and self.is_digit(self.peek_next())):
            self.advance()
            while (self.is_digit(self.peek())): self.advance()

        self.add_tokens(TokenTypes.NUMBER, float(self.source[self.start:self.current]))

    
    def is_alpha(self,c):
        return (c>='a' and c<='z') or (c>='A' and c<='Z') or (c=='_')

    def is_alpha_numeric(self,c):
        return self.is_alpha(c) or self.is_digit(c)


    def alpha(self):
        while (self.is_alpha_numeric(self.peek())): self.advance()
        #get the full word
        #print(self.start,self.current)
        text = self.source[self.start:self.current]

        #then match is with something
        token_type = keywords.get(text)
        if token_type is None: token_type = TokenTypes.IDENTIFIER
        self.add_tokens(token_type)


    
