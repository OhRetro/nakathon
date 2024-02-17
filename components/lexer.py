from .error import *
from .token import *
from .position import *
from string import ascii_letters

DIGITS = "0123456789"
LETTERS = ascii_letters
SPECIAL_CHARACTERS = "&|"
LETTERS_DIGITS = LETTERS + DIGITS

class Lexer:
    def __init__(self, fn: str, text: str):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char: str = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def make_tokens(self):
        tokens = []
        basic_tokens = {
            TokenType.PLUS.value: TokenType.PLUS,
            TokenType.DIV.value: TokenType.DIV,
            TokenType.DIVREST.value: TokenType.DIVREST,
            TokenType.LPAREN.value: TokenType.LPAREN,
            TokenType.RPAREN.value: TokenType.RPAREN,
            TokenType.LSQUARE.value: TokenType.LSQUARE,
            TokenType.RSQUARE.value: TokenType.RSQUARE,
            TokenType.COMMA.value: TokenType.COMMA
        }
        
        advanced_tokens = {
            TokenType.MINUS.value: self.make_minus, # Also checks for '->'
            TokenType.MUL.value: self.make_multiplier, # Also checks for '**' 
            TokenType.EQUALS.value: self.make_equals, # Also checks for '=='
            TokenType.LT.value: self.make_less_than, # Also checks for '<='
            TokenType.GT.value: self.make_greater_than, # Also checks for '>='
            TokenType.STRING.value: self.make_string
        }
        
        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
                
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
                
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
                
            elif self.current_char in basic_tokens:
                tokens.append(Token(basic_tokens[self.current_char], pos_start=self.pos))
                self.advance()

            elif self.current_char in advanced_tokens:
                tokens.append(advanced_tokens[self.current_char]())
                
            elif self.current_char == TokenType.NE.value[0]:
                tok, error = self.make_not_equals()
                if error: return [], error
                tokens.append(tok)
                
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")

        tokens.append(Token(TokenType.EOF, pos_start=self.pos))
        return tokens, None

    def make_minus(self):
        tok_type = TokenType.MINUS
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == TokenType.ARROW.value[-1]:
            self.advance()
            tok_type = TokenType.ARROW
            
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    
    def make_multiplier(self):
        tok_type = TokenType.MUL
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == TokenType.MUL.value:
            self.advance()
            tok_type = TokenType.POWER
            
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    
    def make_number(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TokenType.INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TokenType.FLOAT, float(num_str), pos_start, self.pos)

    def make_string(self):
        string = ""
        pos_start = self.pos.copy()
        escape_char = False
        self.advance()

        escape_chars = {
            "n": "\n",
            "t": "\t"
        }

        while self.current_char != None and (self.current_char != TokenType.STRING.value or escape_char):
            if escape_char:
                string += escape_chars.get(self.current_char, self.current_char)
            else:
                if self.current_char == "\\":
                    escape_char = True
                else:
                    string += self.current_char
            self.advance()
            escape_char = False

        self.advance()
        return Token(TokenType.STRING, string, pos_start, self.pos)

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()
        
        reversed_keyword_dict = Keyword._value2member_map_
        
        while self.current_char != None and self.current_char in LETTERS_DIGITS + "_":
            id_str += self.current_char
            self.advance()
            
        tok_type = TokenType.KEYWORD if id_str in reversed_keyword_dict else TokenType.IDENTIFIER
        tok_value = reversed_keyword_dict[id_str] if id_str in reversed_keyword_dict else id_str
        
        return Token(tok_type, tok_value, pos_start=pos_start, pos_end=self.pos)

    def make_equals(self):
        tok_type = TokenType.EQUALS
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == TokenType.EQUALS.value:
            self.advance()
            tok_type = TokenType.EE
            
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
            
    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == TokenType.EQUALS.value:
            self.advance()
            return Token(TokenType.NE, pos_start=pos_start, pos_end=self.pos), None
        
        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")
    
    def make_less_than(self):
        tok_type = TokenType.LT
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == TokenType.EQUALS.value:
            self.advance()
            tok_type = TokenType.LTE
            
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        tok_type = TokenType.GT
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == TokenType.EQUALS.value:
            self.advance()
            tok_type = TokenType.GTE
            
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
            