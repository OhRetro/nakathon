from .datatypes.all import (
    Number, Function, String, List, Null,
    BaseFunction, Class, Object, Value, Instance,
    make_value, make_value_type
)
from .context import Context
from .node import (Node, NumberNode, StringNode, ClassNode, ObjectNode,
                   ListNode, VarAccessNode, VarAssignNode, VarReassignNode,
                   BinOpNode, UnaryOpNode, IfNode, ForNode, WhileNode,
                   FuncDefNode, CallNode, ReturnNode, ContinueNode, BreakNode)
from .token import Token, TokenType
from .keyword import Keyword
from .runtime import RunTimeResult
from .error import RunTimeError
from .utils.strings_template import (IS_NOT_DEFINED_ERROR, CANNOT_OVERWRITE_IMMUTABLE_BUILTIN_VAR_FUNC_ERROR, VAR_TYPE_INVALID_ERROR,
                                     NO_METHOD_DEFINED_ERROR, VAR_TYPE_DECLARED_BUT_VALUE_TYPE_IS_NOT_SAME_ERROR,
                                     UNKNOWN_FAIL_TYPE_ERROR, VAR_TYPE_ALREADY_DECLARED_CANNOT_CHANGE_ERROR,
                                     WAS_NOT_INITIALIZED_ERROR)
from .utils.debug import DebugMessage

debug_message = DebugMessage("").set_auto_display(True)

class Interpreter:
    def visit(self, node: Node, context: Context):
        method_name = f'visit_{type(node).__name__}'
        debug_message.set_message(f"VISIT: {method_name}")
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node: Node, context: Context):
        raise Exception(NO_METHOD_DEFINED_ERROR.format(f"visit_{type(node).__name__}"))

    ###################################

    def visit_NumberNode(self, node: NumberNode, context: Context) -> Number:
        return RunTimeResult().success(
            Number(node.tok.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_StringNode(self, node: StringNode, context: Context) -> String:
        return RunTimeResult().success(
            String(node.tok.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node: ListNode, context: Context) -> List:
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

    def visit_VarAccessNode(self, node: VarAccessNode, context: Context) -> Value:
        res = RunTimeResult()
        var_name_tok = node.var_name_tok
        var_extra_names_toks = node.var_extra_names_toks
        
        var_full_name: str = var_name_tok.value
        for extra_name_tok in var_extra_names_toks:
            var_full_name += f".{extra_name_tok.value}"
        
        value = context.symbol_table.get(var_full_name)
        
        if not context.symbol_table.exists(var_full_name):
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                IS_NOT_DEFINED_ERROR.format(var_full_name),
                context
            ))
            
        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    #! Code from the Radon Project, I will do my own implementation, using as a reference
    def visit_ObjectNode(self, node: ObjectNode, context: Context) -> Object:
        res = RunTimeResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return():
                return res

        return res.success(
            Object(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
        
    def visit_VarAssignNode(self, node: VarAssignNode, context: Context):
        return self._var_assign(node, context, node.method, node.lifetime)
    
    def visit_VarReassignNode(self, node: VarReassignNode, context: Context):
        res = RunTimeResult()
        var_name_tok = node.var_name_tok
        var_extra_names_toks = node.var_extra_names_toks
        
        var_full_name: str = var_name_tok.value
        
        if var_extra_names_toks != []:  
            for extra_name_tok in var_extra_names_toks:
                if not context.symbol_table.exists(var_full_name):
                    return res.failure(RunTimeError(
                        node.pos_start, node.pos_end,
                        IS_NOT_DEFINED_ERROR.format(var_full_name),
                        context
                    ))
                    
                var_full_name += f".{extra_name_tok.value}"
        
        var_symbols_table = context.symbol_table.exists_in(var_full_name)
        
        if var_symbols_table is not None:
            var_type = context.symbol_table.get_type(var_full_name)

            method = f"set_as_{var_symbols_table.removesuffix('_symbols')}" if var_symbols_table != "symbols" else "set"
            
            lifetime = None
            
            if var_symbols_table == "temporary_symbols":
                lifetime = getattr(context.symbol_table, var_symbols_table)[var_full_name][2]
                lifetime += -1
                
            type_token = Token(TokenType.IDENTIFIER, var_type.__qualname__)
                
            return self._var_assign(VarAssignNode(var_name_tok, var_extra_names_toks, node.value_node, type_token, node.var_assign_type_tok, method, lifetime), context, method, lifetime)
        else:
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                WAS_NOT_INITIALIZED_ERROR.format(var_full_name),
                context
            ))
    
    def _var_assign(self, node: VarAssignNode, context: Context, method: str, lifetime: int = None):
        res = RunTimeResult()
        var_name_tok = node.var_name_tok
        var_extra_names_toks = node.var_extra_names_toks
        
        var_full_name: str = var_name_tok.value
            
        if var_extra_names_toks != []:
            for extra_name_tok in var_extra_names_toks:
                if not context.symbol_table.exists(var_full_name):
                    return res.failure(RunTimeError(
                        node.pos_start, node.pos_end,
                        IS_NOT_DEFINED_ERROR.format(var_full_name),
                        context
                    ))
                    
                var_full_name += f".{extra_name_tok.value}"
        
        var_type = make_value_type(node.var_value_type_tok.value)
        var_assign = node.var_assign_type_tok
        value = res.register(self.visit(node.value_node, context))
        
        symbols_name = method.removeprefix("set").replace("_as_", "") + ("_symbols" if method != "set" else "symbols")

        if context.symbol_table._exists(var_full_name, symbols_name) and var_assign.type != TokenType.EQUALS:
            current_value = context.symbol_table.get(var_full_name)

            if var_assign.type == TokenType.PLUSE:
                value, error = current_value.added_to(value)
            elif var_assign.type == TokenType.MINUSE:
                value, error = current_value.subbed_by(value)
            elif var_assign.type == TokenType.MULE:
                value, error = current_value.multed_by(value)
            elif var_assign.type == TokenType.DIVE:
                value, error = current_value.dived_by(value)
            elif var_assign.type == TokenType.POWERE:
                value, error = current_value.powed_by(value)
            elif var_assign.type == TokenType.DIVRESTE:
                value, error = current_value.rest_of_dived_by(value)
            
            if error:
                return res.failure(error)

        if res.should_return():
            return res
        
        if var_type is None:
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                VAR_TYPE_INVALID_ERROR.format(var_full_name),
                context
            ))
            
        if not isinstance(value, var_type) and not issubclass(value.__class__, BaseFunction):
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                VAR_TYPE_DECLARED_BUT_VALUE_TYPE_IS_NOT_SAME_ERROR.format(var_full_name, var_type.__qualname__, value.__class__.__qualname__),
                context
            ))
        
        success, fail_type = getattr(context.symbol_table, method)(var_full_name, value, var_type) if lifetime is None else getattr(context.symbol_table, method)(var_full_name, value, var_type, lifetime)
        
        if success: return res.success(value)
        elif fail_type == "const": 
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                CANNOT_OVERWRITE_IMMUTABLE_BUILTIN_VAR_FUNC_ERROR.format(var_full_name),
                context
            ))
        elif fail_type == "type": 
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                VAR_TYPE_ALREADY_DECLARED_CANNOT_CHANGE_ERROR.format(var_full_name),
                context
            ))
        else: 
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                UNKNOWN_FAIL_TYPE_ERROR,
                context
            ))

    def visit_BinOpNode(self, node: BinOpNode, context: Context):
        res = RunTimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return():
            return res
        right = res.register(self.visit(node.right_node, context))

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
            context.symbol_table.set(node.var_name_tok.value, Number(i), Number)
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

    def visit_ClassNode(self, node: ClassNode, context: Context):
        res = RunTimeResult()
        
        class_name = node.class_name_tok.value
        body_node = node.body_node
        
        class_value = Class(class_name, body_node).set_context(context).set_pos(node.pos_start, node.pos_end)
        
        context.symbol_table.set(class_name, class_value, Class)
        return res.success(class_value)
    
    def visit_FuncDefNode(self, node: FuncDefNode, context: Context):
        res = RunTimeResult()

        func_name_tok = node.func_name_tok
        
        func_full_name: str = func_name_tok.value if func_name_tok else None
            
        body_node = node.body_node
        
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        arg_types = [make_value_type(arg_type.value) for arg_type in node.arg_type_toks]
        arg_default_values = [make_value(arg_default_value.value) for arg_default_value in node.arg_default_value_toks]
        
        func_value = Function(func_full_name, body_node, arg_names, arg_types, arg_default_values, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)

        if func_name_tok:
            context.symbol_table.set(func_full_name, func_value, Function)

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
