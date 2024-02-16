from .error import *
from .token import *
from .node import *
from .utils.string_generation import expected_symbols


class ParseResult:

    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

    def __repr__(self) -> str:
        return f"<ParseResult:({self.node}, {self.error})>"


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok: Token
        self.advance()

    def advance(self) -> Token:
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()

        if not res.error and self.current_tok.type != TokenType.EOF:
            expected_symbols_list = [
                TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.POWER, TokenType.DIVREST,
                TokenType.EE, TokenType.NE, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE,
                Keyword.AND, Keyword.OR
            ]

            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start,
                                   self.current_tok.pos_end,
                                   expected_symbols(expected_symbols_list)))
            
        return res

    ###################################

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None
        
        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.IF):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected_symbols([Keyword.IF])
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.THEN):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected_symbols([Keyword.THEN])
            ))

        res.register_advancement()
        self.advance()

        expr = res.register(self.expr())
        if res.error:
            return res
        cases.append((condition, expr))

        while self.current_tok.matches(TokenType.KEYWORD, Keyword.ELIF):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error:
                return res

            if not self.current_tok.matches(TokenType.KEYWORD, Keyword.THEN):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected_symbols([Keyword.THEN])
                ))

            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res
            cases.append((condition, expr))

        if self.current_tok.matches(TokenType.KEYWORD, Keyword.ELSE):
            res.register_advancement()
            self.advance()

            else_case = res.register(self.expr())
            if res.error:
                return res

        return res.success(IfNode(cases, else_case))

    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.FOR):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected_symbols([Keyword.FOR])
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TokenType.IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected_symbols([TokenType.IDENTIFIER])
            ))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TokenType.EQUALS:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected_symbols([TokenType.EQUALS])
            ))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.TO):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected_symbols([Keyword.TO])
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error:
            return res

        if self.current_tok.matches(TokenType.KEYWORD, Keyword.STEP):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error:
                return res
        else:
            step_value = None

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.THEN):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected_symbols([Keyword.THEN])
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error:
            return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body))

    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.WHILE):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected_symbols([Keyword.WHILE])
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.THEN):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected_symbols([Keyword.THEN])
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error:
            return res

        return res.success(WhileNode(condition, body))

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TokenType.INT, TokenType.FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TokenType.IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TokenType.LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TokenType.RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start,
                                       self.current_tok.pos_end,
                                       expected_symbols([TokenType.RPAREN])))

        elif tok.matches(TokenType.KEYWORD, Keyword.IF):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)

        elif tok.matches(TokenType.KEYWORD, Keyword.FOR):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)

        elif tok.matches(TokenType.KEYWORD, Keyword.WHILE):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)

        return res.failure(
            InvalidSyntaxError(
                tok.pos_start, tok.pos_end,
                expected_symbols([
                    TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER, 
                    TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN
                    ])
                )
        )

    def power(self):
        return self.bin_op(self.atom, (TokenType.POWER, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TokenType.PLUS, TokenType.MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TokenType.MUL, TokenType.DIV))

    def arith_expr(self):
        return self.bin_op(self.term, (TokenType.PLUS, TokenType.MINUS))

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TokenType.KEYWORD, Keyword.NOT):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))

        tok_types = (TokenType.EE, TokenType.NE, TokenType.LT,
                     TokenType.GT, TokenType.LTE, TokenType.GTE)
        node = res.register(self.bin_op(self.arith_expr, tok_types))

        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected_symbols([
                        TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER, 
                        TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN,
                        Keyword.NOT
                        ])
                    )
            )

        return res.success(node)

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TokenType.KEYWORD, Keyword.SETVAR):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TokenType.IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start,
                                       self.current_tok.pos_end,
                                       expected_symbols([TokenType.IDENTIFIER])))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TokenType.EQUALS:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start,
                                       self.current_tok.pos_end,
                                       expected_symbols([TokenType.EQUALS])))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(
            self.bin_op(self.comp_expr, ((TokenType.KEYWORD,
                        Keyword.AND), (TokenType.KEYWORD, Keyword.OR)))
        )

        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected_symbols([
                        Keyword.SETVAR,
                        TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER, 
                        TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN,
                        Keyword.NOT
                        ])
                    )
                )

        return res.success(node)

    ###################################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
