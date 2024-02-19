from .value.number import Number
from .value.function import Function
from .value.string import String
from .value.list import List
from .value.null import Null
from .context import Context
from .node import (Node, NumberNode, StringNode,
                   ListNode, VarAccessNode, VarAssignNode,
                   ImmutableVarAssignNode, TempVarAssignNode, BinOpNode,
                   UnaryOpNode, IfNode, ForNode, WhileNode,
                   FuncDefNode, CallNode, ReturnNode, ContinueNode, BreakNode)
from .token import TokenType, Keyword
from .runtime import RunTimeResult
from .error import RunTimeError
from .utils.error_messages import is_not_defined, cannot_overwrite_immutable_var, no_method_defined


class Interpreter:
    def visit(self, node: Node, context: Context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node: Node, context: Context):
        raise Exception(no_method_defined.format(f"visit_{type(node).__name__}"))

    ###################################

    def visit_NumberNode(self, node: NumberNode, context: Context):
        return RunTimeResult().success(
            Number(node.tok.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_StringNode(self, node: StringNode, context: Context):
        return RunTimeResult().success(
            String(node.tok.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node: ListNode, context: Context):
        res = RunTimeResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return():
                return res

        return res.success(
            List(elements).set_context(context).set_pos(
                node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node: VarAccessNode, context: Context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)
        
        if not context.symbol_table.exists(var_name):
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                is_not_defined.format(var_name),
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node: VarAssignNode, context: Context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return():
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)
    
    def visit_ImmutableVarAssignNode(self, node: ImmutableVarAssignNode, context: Context):
        res = RunTimeResult()
        immutable_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        success = context.symbol_table.set_as_immutable(immutable_name, value)
        
        if success: return res.success(value)
        else: return res.failure(RunTimeError(
            node.pos_start, node.pos_end,
            cannot_overwrite_immutable_var.format(immutable_name),
            context
        ))
 
    def visit_TempVarAssignNode(self, node: TempVarAssignNode, context: Context):
        res = RunTimeResult()
        temp_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        temp_lifetime = node.lifetime_tok.value
        success = context.symbol_table.set_as_temp(temp_name, value, temp_lifetime)
        
        if success: return res.success(value)
        else: return res.failure(RunTimeError(
            node.pos_start, node.pos_end,
            cannot_overwrite_immutable_var.format(temp_name),
            context
        ))
        
    def visit_BinOpNode(self, node: BinOpNode, context: Context):
        res = RunTimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return():
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.should_return():
            return res

        if node.op_tok.type == TokenType.PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TokenType.MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TokenType.MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TokenType.DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TokenType.POWER:
            result, error = left.powed_by(right)
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
        if res.should_return():
            return res

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

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return():
                return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return():
                    return res
                return res.success(Null.null if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(self.visit(expr, context))
            if res.should_return():
                return res
            return res.success(Null.null if should_return_null else expr_value)

        return res.success(Null.null)

    def visit_ForNode(self, node: ForNode, context: Context):
        res = RunTimeResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return():
            return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return():
            return res

        if node.step_value_node:
            step_value = res.register(
                self.visit(node.step_value_node, context))
            if res.should_return():
                return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            def condition(): return i < end_value.value
        else:
            def condition(): return i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False:
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Null.null if node.should_return_null else
            List(elements).set_context(context).set_pos(
                node.pos_start, node.pos_end)
        )

    def visit_WhileNode(self, node: WhileNode, context: Context):
        res = RunTimeResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return():
                return res

            if not condition.is_true():
                break

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False:
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Null.null if node.should_return_null else
            List(elements).set_context(context).set_pos(
                node.pos_start, node.pos_end)
        )

    def visit_FuncDefNode(self, node: FuncDefNode, context: Context):
        res = RunTimeResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(
            context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node: CallNode, context: Context):
        res = RunTimeResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return():
            return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return():
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return():
            return res
        return_value = return_value.copy().set_pos(
            node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)

    def visit_ReturnNode(self, node: ReturnNode, context: Context):
        res = RunTimeResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return():
                return res
        else:
            value = Null.null

        return res.success_return(value)

    def visit_ContinueNode(self, node: ContinueNode, context: Context):
        return RunTimeResult().success_continue()

    def visit_BreakNode(self, node: BreakNode, context: Context):
        return RunTimeResult().success_break()
