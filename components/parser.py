from typing import Callable
from .error import InvalidSyntaxError
from .token import Token, TokenType
from .keyword import Keyword
from .node import (NumberNode, StringNode, BinOpNode,
                   UnaryOpNode, VarAccessNode, VarAssignNode,
                   ImmutableVarAssignNode, TempVarAssignNode, ScopedVarAssignNode, VarReassignNode,
                   CallNode, ForNode, FuncDefNode, IfNode,
                   WhileNode, ListNode, ReturnNode, ContinueNode, BreakNode)
from .utils.strings_template import CANNOT_DECLARE_TYPE_AFTER_DECLARED_ERROR
from .utils.expected import expected

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self

    def __repr__(self) -> str:
        return f"<ParseResult:({self.node}, {self.error})>"


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != TokenType.EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Token cannot appear after previous tokens"
            ))
        return res

    ###################################

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type in (TokenType.NEWLINE, TokenType.SEMICOLON):
            res.register_advancement()
            self.advance()

        statement = res.register(self.statement())
        if res.error:
            return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            
            while self.current_tok.type in (TokenType.NEWLINE, TokenType.SEMICOLON):
                res.register_advancement()
                self.advance()
                newline_count += 1
                
            if newline_count == 0:
                more_statements = False

            if not more_statements:
                break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(
            statements,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()
        
        if self.current_tok.matches(TokenType.KEYWORD, Keyword.RETURN):
            res.register_advancement()
            self.advance()
            
            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TokenType.KEYWORD, Keyword.CONTINUE):
            res.register_advancement()
            self.advance()
            return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TokenType.KEYWORD, Keyword.BREAK):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(Keyword.RETURN, Keyword.CONTINUE, Keyword.BREAK,
                         Keyword.SETVAR, Keyword.SETIMMUTABLEVAR, Keyword.SETTEMPVAR, Keyword.SETSCOPEDVAR,
                         Keyword.IF, Keyword.FOR, Keyword.WHILE, Keyword.SETFUNCTION,
                         TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER,
                         TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN, TokenType.LSQUARE, TokenType.LBRACE, Keyword.NOT)
            ))
            
        return res.success(expr)

    def expr(self):
        res = ParseResult()

        if (self.current_tok.matches(TokenType.KEYWORD, Keyword.SETVAR) or
            self.current_tok.matches(TokenType.KEYWORD, Keyword.SETIMMUTABLEVAR) or
            self.current_tok.matches(TokenType.KEYWORD, Keyword.SETTEMPVAR) or
            self.current_tok.matches(TokenType.KEYWORD, Keyword.SETSCOPEDVAR)):
            
            var_keyword_tok = self.current_tok
            var_type_tok = None
            var_type_specified = False

            res.register_advancement()
            self.advance()

            if self.current_tok.type != TokenType.IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.IDENTIFIER)
                ))
                
            var_name_tok = self.current_tok
            
            res.register_advancement()
            self.advance()
        
            if self.current_tok.type == TokenType.COLON:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TokenType.IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        expected(TokenType.IDENTIFIER)
                    ))
                    
                var_type_tok = self.current_tok
                
                var_type_specified = True
                
                if var_keyword_tok.value == Keyword.SETTEMPVAR:
                    res.register_advancement()
                    self.advance()
            else:
                var_type_tok = Token(TokenType.IDENTIFIER, "Any")
            
            if var_keyword_tok.value == Keyword.SETTEMPVAR:
                if self.current_tok.type != TokenType.INT:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        expected(TokenType.INT)
                    ))

                temp_lifetime = self.current_tok

            if var_type_specified or var_keyword_tok.value == Keyword.SETTEMPVAR:
                res.register_advancement()
                self.advance()

            if self.current_tok.type not in (TokenType.EQUALS, TokenType.PLUSE, TokenType.MINUSE, TokenType.MULE, TokenType.DIVE, TokenType.POWERE, TokenType.DIVRESTE):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.EQUALS, TokenType.PLUSE, TokenType.MINUSE, TokenType.MULE, TokenType.DIVE, TokenType.POWERE, TokenType.DIVRESTE)
                ))
                
            var_assign_type_tok = self.current_tok

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res

            if var_keyword_tok.value == Keyword.SETVAR:
                node_ret = VarAssignNode(var_name_tok, expr, var_type_tok, var_assign_type_tok)
            elif var_keyword_tok.value == Keyword.SETIMMUTABLEVAR:
                node_ret = ImmutableVarAssignNode(var_name_tok, expr, var_type_tok, var_assign_type_tok)
            elif var_keyword_tok.value == Keyword.SETTEMPVAR:
                node_ret = TempVarAssignNode(var_name_tok, expr, var_type_tok, var_assign_type_tok, temp_lifetime)
            elif var_keyword_tok.value == Keyword.SETSCOPEDVAR:
                node_ret = ScopedVarAssignNode(var_name_tok, expr, var_type_tok, var_assign_type_tok)

            return res.success(node_ret)

        if self.current_tok.type == TokenType.IDENTIFIER:                
            var_name_tok = self.current_tok
            
            res.register_advancement()
            self.advance()

            if self.current_tok.type in (TokenType.EQUALS, TokenType.PLUSE, TokenType.MINUSE, TokenType.MULE, TokenType.DIVE, TokenType.POWERE, TokenType.DIVRESTE):
                var_assign_type_tok = self.current_tok

                res.register_advancement()
                self.advance()
                
                expr = res.register(self.expr())
                if res.error:
                    return res

                return res.success(VarReassignNode(var_name_tok, expr, var_assign_type_tok))
            
            elif self.current_tok.type == TokenType.COLON:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    CANNOT_DECLARE_TYPE_AFTER_DECLARED_ERROR
                ))
            
            else:
                self.reverse()
        
        node = res.register(self.bin_op(
            self.comp_expr, ((TokenType.KEYWORD, Keyword.AND), (TokenType.KEYWORD, Keyword.OR))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(Keyword.SETVAR, Keyword.SETIMMUTABLEVAR, Keyword.SETTEMPVAR, Keyword.SETSCOPEDVAR,
                         Keyword.IF, Keyword.FOR, Keyword.WHILE, Keyword.SETFUNCTION,
                         TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER,
                         TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN, TokenType.LSQUARE, TokenType.LBRACE, Keyword.NOT)
            ))

        return res.success(node)

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

        node = res.register(self.bin_op(
            self.arith_expr, (TokenType.EE, TokenType.NE, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER,
                         TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN, TokenType.LSQUARE, Keyword.NOT)
            ))

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TokenType.PLUS, TokenType.MINUS))

    def term(self):
        return self.bin_op(self.factor, (TokenType.MUL, TokenType.DIV, TokenType.DIVREST))

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

    def power(self):
        return self.bin_op(self.call, (TokenType.POWER, ), self.factor)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error:
            return res

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
                        expected(TokenType.RPAREN, Keyword.SETVAR, Keyword.SETIMMUTABLEVAR, Keyword.SETTEMPVAR, Keyword.SETSCOPEDVAR,
                                 Keyword.IF, Keyword.FOR, Keyword.WHILE, Keyword.SETFUNCTION,
                                 TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER,
                                 TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN, TokenType.LSQUARE, Keyword.NOT)
                    ))

                while self.current_tok.type == TokenType.COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

                if self.current_tok.type != TokenType.RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        expected(TokenType.COMMA, TokenType.RPAREN)
                    ))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
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
            if res.error:
                return res
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
            if res.error:
                return res
            return res.success(list_expr)

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

        elif tok.matches(TokenType.KEYWORD, Keyword.SETFUNCTION):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            expected(TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER,
                     TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN, TokenType.LSQUARE,
                     Keyword.IF, Keyword.FOR, Keyword.WHILE, Keyword.SETFUNCTION)
        ))

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
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
                    expected(TokenType.RSQUARE, Keyword.SETVAR, Keyword.SETIMMUTABLEVAR, Keyword.SETTEMPVAR, Keyword.SETSCOPEDVAR,
                             Keyword.FOR, Keyword.WHILE, Keyword.SETFUNCTION,
                             TokenType.INT, TokenType.FLOAT, TokenType.IDENTIFIER,
                             TokenType.PLUS, TokenType.MINUS, TokenType.LPAREN, TokenType.LSQUARE, Keyword.NOT)
                ))

            while self.current_tok.type == TokenType.COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error:
                    return res

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

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases(Keyword.IF))
        if res.error:
            return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def elseif_expr(self):
        return self.if_expr_cases(Keyword.ELSEIF)

    def else_expr(self):
        res = ParseResult()
        else_case = None

        res.register_advancement()
        self.advance()
            
        if self.current_tok.type == TokenType.LBRACE:
            res.register_advancement()
            self.advance()
            
            if self.current_tok.type == TokenType.NEWLINE:
                res.register_advancement()
                self.advance()
                
            statements = res.register(self.statements())
            if res.error:
                return res
            else_case = (statements, True)

            if self.current_tok.matches(TokenType.RBRACE):
                res.register_advancement()
                self.advance()
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.RBRACE)
                ))
        else:
            expr = res.register(self.statement())
            if res.error:
                return res
            else_case = (expr, False)

        return res.success(else_case)

    def if_expr_elseif_or_else(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_tok.matches(TokenType.KEYWORD, Keyword.ELSEIF):
            all_cases = res.register(self.elseif_expr())
            
            if res.error:
                return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.else_expr())
            if res.error:
                return res

        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TokenType.KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '{case_keyword}'"
            ))
        
        keyword_tok = self.current_tok
        
        res.register_advancement()
        self.advance()
        
        condition = res.register(self.expr())
        
        if res.error:
            return res

        if self.current_tok.matches(TokenType.LBRACE):
            res.register_advancement()
            self.advance()

            if self.current_tok.type == TokenType.NEWLINE:
                res.register_advancement()
                self.advance()

            statements = res.register(self.statements())
            if res.error:
                return res
            
            cases.append((condition, statements, True))
            
            if self.current_tok.matches(TokenType.RBRACE):
                if keyword_tok.matches(TokenType.KEYWORD, Keyword.IF) or keyword_tok.matches(TokenType.KEYWORD, Keyword.ELSEIF):
                    res.register_advancement()
                    self.advance()
                    
                    if self.current_tok.matches(TokenType.KEYWORD, Keyword.ELSEIF) or self.current_tok.matches(TokenType.KEYWORD, Keyword.ELSE):
                        all_cases = res.register(self.if_expr_elseif_or_else())
                        if res.error:
                            return res
                        
                        new_cases, else_case = all_cases
                        cases.extend(new_cases)
                    
                elif keyword_tok.matches(TokenType.KEYWORD, Keyword.ELSE):                
                    res.register_advancement()
                    self.advance()
                
                else:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        expected(Keyword.IF, Keyword.ELSEIF, Keyword.ELSE)
                    ))
                    
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.RBRACE)
                ))
        
        # Inline statements
        else:
            expr = res.register(self.statement())
            if res.error:
                return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_elseif_or_else())
            if res.error:
                return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)
            
        return res.success((cases, else_case))

    def for_expr(self):
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
        if res.error:
            return res

        if not self.current_tok.type == TokenType.SEMICOLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.SEMICOLON)
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error:
            return res

        if self.current_tok.type == TokenType.SEMICOLON:
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error:
                return res
        else:
            step_value = None

        if self.current_tok.type != TokenType.LBRACE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.LBRACE)
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type in (TokenType.NEWLINE, TokenType.SEMICOLON):
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if self.current_tok.type != TokenType.RBRACE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.RBRACE)
                ))

            res.register_advancement()
            self.advance()

            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

        body = res.register(self.statement())
        if res.error:
            return res
    
        if self.current_tok.type != TokenType.RBRACE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.RBRACE)
            ))

        res.register_advancement()
        self.advance()

        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TokenType.KEYWORD, Keyword.WHILE):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(Keyword.WHILE)
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if self.current_tok.type != TokenType.LBRACE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.LBRACE)
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type in (TokenType.NEWLINE, TokenType.SEMICOLON):
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if self.current_tok.type != TokenType.RBRACE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.RBRACE)
                ))

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))

        body = res.register(self.statement())
        if res.error:
            return res

        if self.current_tok.type != TokenType.RBRACE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.RBRACE)
            ))

        res.register_advancement()
        self.advance()
            
        return res.success(WhileNode(condition, body, False))

    def func_def(self):
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
        arg_type_toks = []
        arg_default_value_toks = []
        
        failsafe = -1
        
        while True:
            failsafe += 1
            if failsafe > 5 or self.current_tok.type == TokenType.RPAREN: break
            
            arg_name_set = False

            if self.current_tok.type == TokenType.IDENTIFIER:
                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()
                
                failsafe = -1
                arg_name_set = True
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.IDENTIFIER)
                ))             
                
            if self.current_tok.type == TokenType.COLON and arg_name_set:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TokenType.IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        expected(TokenType.IDENTIFIER)
                    ))

                arg_type_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()
                
                failsafe = -1
                
            elif arg_name_set:
                arg_type_toks.append(Token(TokenType.IDENTIFIER, "Value"))
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.IDENTIFIER)
                ))
            
            if self.current_tok.type == TokenType.EQUALS and arg_name_set:
                res.register_advancement()
                self.advance()

                arg_default_value_toks.append(self.current_tok)
                
                res.register_advancement()
                self.advance()
                
                failsafe = -1
            elif arg_name_set:
                arg_default_value_toks.append(Token(TokenType.GENERIC, None))
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    expected(TokenType.IDENTIFIER)
                ))

            if self.current_tok.type == TokenType.COMMA and arg_name_set:
                res.register_advancement()
                self.advance()
                
                failsafe = -1

        if self.current_tok.type != TokenType.RPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.IDENTIFIER, TokenType.COLON, TokenType.EQUALS, TokenType.COMMA, TokenType.RPAREN)
            ))
                
        res.register_advancement()
        self.advance()

        if self.current_tok.type == TokenType.ARROW:
            res.register_advancement()
            self.advance()

            body = res.register(self.expr())
            if res.error:
                return res

            return res.success(FuncDefNode(
                var_name_tok,
                arg_name_toks,
                arg_type_toks,
                arg_default_value_toks,
                body,
                True
            ))

        if self.current_tok.type != TokenType.LBRACE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.ARROW, TokenType.LBRACE)
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res
        
        if self.current_tok.type != TokenType.RBRACE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                expected(TokenType.RBRACE)
            ))

        res.register_advancement()
        self.advance()

        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            arg_type_toks,
            arg_default_value_toks,
            body,
            False
        ))

    ###################################

    def bin_op(self, func_a: Callable, ops: tuple[TokenType | Keyword], func_b: Callable = None):
        if func_b is None:
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
