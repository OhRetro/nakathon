from .number import Number
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
            
        return res.success(value)
    
    def visit_VarAssignNode(self, node: VarAssignNode, context: Context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node: BinOpNode, context: Context):
        res = RunTimeResult()
        left: Number = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right: Number = res.register(self.visit(node.right_node, context))
        if res.error: return res

        error = None

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

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
