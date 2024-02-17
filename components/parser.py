from typing import Callable

from .error import Error, InvalidSyntaxError
from .token import Token, TokenType, Keyword
from .node import Node, NumberNode, StringNode, BinOpNode, UnaryOpNode, VarAccessNode, VarAssignNode, CallNode, ForNode, FuncDefNode, IfNode, WhileNode, ListNode
from .utils.expected import expected


class ParseResult:

    def __init__(self):
        self.error: Error = None
        self.node: Node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res) -> Node:
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node: Node):
        self.node = node
        return self

    def failure(self, error: Error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

    def __repr__(self) -> str:
        return f"<ParseResult:({self.node}, {self.error})>"


class Parser:

    def __init__(self, tokens):
        self.tokens: tuple[Token] = tokens
        self.tok_idx = -1
        self.current_tok: Token
        self.advance()

    def advance(self) -> Token:
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self) -> ParseResult:
        res = self.expr()

        if not res.error and self.current_tok.type != TokenType.EOF:
            expected_symbols_list = [
                TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.POWER, TokenType.DIVREST,
                TokenType.EE, TokenType.NE, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE,
                Keyword.AND, Keyword.OR
            ]

            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(*expected_symbols_list))
                )
            
        return res

	###################################

    def expr(self) -> ParseResult:
        res = ParseResult()

        if self.current_tok.matches(TokenType.KEYWORD, Keyword.SETVAR):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TokenType.IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.IDENTIFIER)
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TokenType.EQUALS:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.EQUALS)
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((TokenType.KEYWORD, Keyword.AND), (TokenType.KEYWORD, Keyword.OR))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(Keyword.SETVAR, Keyword.IF, Keyword.FOR, Keyword.WHILE, Keyword.SETFUNCTION,
                         TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER,
                         TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN, TokenType.LSQUARE, Keyword.NOT)
            ))

        return res.success(node)

    def comp_expr(self) -> ParseResult:
        res = ParseResult()

        if self.current_tok.matches(TokenType.KEYWORD, Keyword.NOT):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))
        
        node = res.register(self.bin_op(self.arith_expr, (TokenType.EE, TokenType.NE, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE)))
        
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER,
                         TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN, TokenType.LSQUARE, Keyword.NOT)
            ))

        return res.success(node)

    def arith_expr(self) -> ParseResult:
        return self.bin_op(self.term, (TokenType.PLUS, TokenType.MINUS))

    def term(self) -> ParseResult:
        return self.bin_op(self.factor, (TokenType.MUL, TokenType.DIV))

    def factor(self) -> ParseResult:
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TokenType.PLUS, TokenType.MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def power(self) -> ParseResult:
        return self.bin_op(self.call, (TokenType.POWER, TokenType.DIVREST), self.factor)

    def call(self) -> ParseResult:
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res

        if self.current_tok.type == TokenType.LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_tok.type == TokenType.RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        expected(TokenType.RPAREN, Keyword.SETVAR, Keyword.IF, Keyword.FOR, Keyword.WHILE, Keyword.SETFUNCTION,
                                 TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER,
                                 TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN,  Keyword.NOT)
                    ))

                while self.current_tok.type == TokenType.COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.current_tok.type != TokenType.RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        expected(TokenType.COMMA, TokenType.RPAREN)
                    ))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self) -> ParseResult:
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TokenType.INT, TokenType.FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TokenType.STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == TokenType.IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TokenType.LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TokenType.RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.RPAREN)
                ))
        
        elif tok.type == TokenType.LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)
        
        elif tok.matches(TokenType.KEYWORD, Keyword.IF):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif tok.matches(TokenType.KEYWORD, Keyword.FOR):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)

        elif tok.matches(TokenType.KEYWORD, Keyword.WHILE):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(TokenType.KEYWORD, Keyword.SETFUNCTION):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            expected(TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER,
                     TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN, TokenType.LSQUARE,
                     Keyword.IF, Keyword.FOR, Keyword.WHILE, Keyword.SETFUNCTION)
        ))
        
    def list_expr(self) -> ParseResult:
        res = ParseResult()
        element_nodes: list[Node] = []
        pos_start = self.current_tok.pos_start.copy()
        
        if self.current_tok.type != TokenType.LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.LSQUARE)
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TokenType.RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.RSQUARE, Keyword.SETVAR, Keyword.FOR, Keyword.WHILE, Keyword.SETFUNCTION,
                             TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER,
                             TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN, TokenType.LSQUARE, Keyword.NOT)
                ))

            while self.current_tok.type == TokenType.COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error: return res

            if self.current_tok.type != TokenType.RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.COMMA, TokenType.RSQUARE)
                ))

            res.register_advancement()
            self.advance()
        
        return res.success(ListNode(
            element_nodes, 
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def if_expr(self) -> ParseResult:
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.IF):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(Keyword.IF)
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.THEN):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(Keyword.THEN)
            ))

        res.register_advancement()
        self.advance()

        expr = res.register(self.expr())
        if res.error: return res
        cases.append((condition, expr))

        while self.current_tok.matches(TokenType.KEYWORD, Keyword.ELIF):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error: return res

            if not self.current_tok.matches(TokenType.KEYWORD, Keyword.THEN):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(Keyword.THEN)
                ))

            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error: return res
            cases.append((condition, expr))

        if self.current_tok.matches(TokenType.KEYWORD, Keyword.ELSE):
            res.register_advancement()
            self.advance()

            else_case = res.register(self.expr())
            if res.error: return res

        return res.success(IfNode(cases, else_case))

    def for_expr(self) -> ParseResult:
        res = ParseResult()

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.FOR):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(Keyword.FOR)
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TokenType.IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.IDENTIFIER)
            ))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TokenType.EQUALS:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.EQUALS)
            ))
        
        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.TO):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(Keyword.TO)
            ))
        
        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error: return res

        if self.current_tok.matches(TokenType.KEYWORD, Keyword.STEP):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error: return res
        else:
            step_value = None

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.THEN):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(Keyword.THEN)
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body))

    def while_expr(self) -> ParseResult:
        res = ParseResult()

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.WHILE):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(Keyword.WHILE)
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.THEN):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(Keyword.THEN)
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error: return res

        return res.success(WhileNode(condition, body))

    def func_def(self) -> ParseResult:
        res = ParseResult()

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.SETFUNCTION):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(Keyword.SETFUNCTION)
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TokenType.IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TokenType.LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.LPAREN)
                ))
        else:
            var_name_tok = None
            if self.current_tok.type != TokenType.LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.IDENTIFIER, TokenType.LPAREN)
                ))
        
        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == TokenType.IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()
            
            while self.current_tok.type == TokenType.COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TokenType.IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        expected(TokenType.IDENTIFIER)
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()
            
            if self.current_tok.type != TokenType.RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.COMMA, TokenType.LPAREN)
                ))
        else:
            if self.current_tok.type != TokenType.RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.IDENTIFIER, TokenType.RPAREN)
                ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TokenType.ARROW:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.ARROW)
            ))

        res.register_advancement()
        self.advance()
        node_to_return = res.register(self.expr())
        if res.error: return res

        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            node_to_return
        ))

    ###################################


    def bin_op(self, func_a: Callable, ops: list[TokenType]|tuple[TokenType], func_b: Callable = None) -> ParseResult:
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
