from .values.number import Number
from .values.function import Function

from .context import Context
from .node import *
from .token import *
from .runtime import *
from .error import *
from .symbol_table import *

class Interpreter:
    def visit(self, node, context: Context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context: Context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node: NumberNode, context: Context):
        return RunTimeResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
                
    def visit_VarAccessNode(self, node: VarAccessNode, context: Context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)
        
        if not value:
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                f"'{var_name} is not defined",
                context
            ))
        
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)
    
    def visit_VarAssignNode(self, node: VarAssignNode, context: Context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        success = context.symbol_table.set(var_name, value)
        
        if success: return res.success(value)
        else: return res.failure(RunTimeError(
            node.pos_start, node.pos_end,
            f"Cannot overwrite the immutable var '{var_name}'",
            context
        ))

    def visit_BinOpNode(self, node: BinOpNode, context: Context):
        res = RunTimeResult()
        left: Number = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right: Number = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_tok.type == TokenType.PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TokenType.MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TokenType.MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TokenType.DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TokenType.POWER:
            result, error = left.powered_by(right)
        elif node.op_tok.type == TokenType.DIVREST:
            result, error = left.rest_of_dived_by(right)
        elif node.op_tok.type == TokenType.EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TokenType.NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TokenType.LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TokenType.GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TokenType.LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TokenType.GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TokenType.KEYWORD, Keyword.AND):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TokenType.KEYWORD, Keyword.OR):
            result, error = left.ored_by(right)
   
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node: UnaryOpNode, context: Context):
        res = RunTimeResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res
        
        error = None
        
        if node.op_tok.type == TokenType.MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TokenType.KEYWORD, Keyword.NOT):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node: IfNode, context: Context):
        res = RunTimeResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)

        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(else_value)

        return res.success(None)

    def visit_ForNode(self, node: ForNode, context: Context):
        res = RunTimeResult()

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error: return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.error: return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.error: return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value
        
        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            res.register(self.visit(node.body_node, context))
            if res.error: return res

        return res.success(None)

    def visit_WhileNode(self, node: WhileNode, context: Context):
        res = RunTimeResult()

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error: return res

            if not condition.is_true(): break

            res.register(self.visit(node.body_node, context))
            if res.error: return res

        return res.success(None)
    
    def visit_FuncDefNode(self, node: FuncDefNode, context: Context):
        res = RunTimeResult()
        
        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        args_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, args_names).set_context(context).set_pos(node.pos_start, node.pos_end)
        
        if node.var_name_tok:
            success = context.symbol_table.set(func_name, func_value)

            if not success: return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                f"Cannot overwrite the immutable var '{func_name}'",
                context
            ))
            
        return res.success(func_value)
    
    def visit_CallNode(self, node: CallNode, context: Context):
        res = RunTimeResult()
        args = []
        
        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)
        
        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res
            
        return_value = res.register(value_to_call.execute(args))
        if res.error: return res
        return res.success(return_value)