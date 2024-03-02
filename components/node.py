from .token import Token
from .datatypes.value import Value
from .utils.debug import DebugMessage
from .position import Position

debug_message = DebugMessage("")

class Node:
    def __init__(self, tok: Token = None, pos_start: Position = None, pos_end: Position = None, should_return_null: bool = False):
        self.tok = tok

        self.pos_start = self.tok.pos_start if pos_start is None else pos_start
        self.pos_end = self.tok.pos_end if pos_end is None else pos_end

        self.should_return_null = should_return_null

        self.display = self.tok
        debug_message.set_message(f"NODE: CREATED: {self}").display()

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.display}>"

class NumberNode(Node):
    def __init__(self, tok: Token):
        super().__init__(tok)

class StringNode(Node):
    def __init__(self, tok: Token):
        super().__init__(tok)

class ListNode(Node):
    def __init__(self, element_nodes: list[Node], pos_start: Position, pos_end: Position):
        self.element_nodes = element_nodes
        
        self.pos_start = pos_start
        self.pos_end = pos_end
        
        debug_message.set_message(f"NODE: CREATED: {self}").display()
        
        #super().__init__()
    def __repr__(self):
        return f"<{self.__class__.__name__}:{len(self.element_nodes)}>"

class VarAccessNode(Node):
    def __init__(self, var_name_tok: Token):
        self.var_name_tok = var_name_tok
        super().__init__(var_name_tok)

class VarAssignNode(Node):
    def __init__(self, var_name_tok: Token, value_node: Node, var_value_type_tok: Value, var_assign_type_tok: Token, method: str, lifetime: int):
        self.method = method
        self.var_name_tok = var_name_tok
        self.var_value_type_tok = var_value_type_tok
        self.lifetime = lifetime
        self.var_assign_type_tok = var_assign_type_tok
        self.value_node = value_node
        super().__init__(var_name_tok)
        self.display = f"{self.var_name_tok}:{self.var_value_type_tok.value}:{self.value_node}"
        self.pos_end = self.value_node.pos_end

class VarReassignNode(Node):
    def __init__(self, var_name_tok: Token, value_node: Node, var_assign_type_tok: Token):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.var_assign_type_tok = var_assign_type_tok
        super().__init__(var_name_tok)
        self.pos_end = self.value_node.pos_end

class BinOpNode(Node):
    def __init__(self, left_node: Node, op_tok: Token, right_node: Node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        super().__init__(op_tok)
        self.display = f"({self.left_node}, {self.op_tok}, {self.right_node})"
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

class UnaryOpNode(Node):
    def __init__(self, op_tok: Token, node: Node):
        self.op_tok = op_tok
        self.node = node
        super().__init__(op_tok)
        self.display = f"({self.op_tok}, {self.node})"
        self.pos_end = self.node.pos_end

class IfNode(Node):
    def __init__(self, cases: tuple[tuple[Token]], else_case: tuple):
        self.cases = cases
        self.else_case = else_case
        super().__init__(cases[0][0])
        self.pos_end = (
            else_case or self.cases[len(self.cases) - 1])[0].pos_end

class ForNode(Node):
    def __init__(self, var_name_tok: Token, start_value_node: Node, end_value_node: Node, step_value_node: Node, body_node: Node, should_return_null: bool):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        super().__init__(var_name_tok, should_return_null = should_return_null)
        self.pos_end = self.body_node.pos_end

class WhileNode(Node):
    def __init__(self, condition_node: Node, body_node: Node, should_return_null: bool):
        self.condition_node = condition_node
        self.body_node = body_node
        super().__init__(condition_node, should_return_null = should_return_null)
        self.pos_end = self.body_node.pos_end

class ClassNode(Node):
    def __init__(self, class_name_tok: Token, body_node: ListNode, pos_start: Position, pos_end: Position):
        self.class_name_tok = class_name_tok
        self.body_node = body_node
        super().__init__(class_name_tok, pos_start, pos_end)
        
class FuncDefNode(Node):
    def __init__(self, func_name_tok: Token, arg_name_toks: list[Token], arg_type_toks: list[Token], arg_default_value_toks: list[Token], body_node: ListNode, should_auto_return: bool):
        self.func_name_tok = func_name_tok
        self.arg_name_toks = arg_name_toks
        self.arg_type_toks = arg_type_toks
        self.arg_default_value_toks = arg_default_value_toks
        self.body_node = body_node
        self.should_auto_return = should_auto_return
        
        if self.func_name_tok:
            to_tok_base = self.func_name_tok
        elif len(arg_name_toks) > 0:
            to_tok_base = self.arg_name_toks[0]
        else:
            to_tok_base = self.body_node

        super().__init__(to_tok_base)

        self.pos_end = self.body_node.pos_end

class CallNode(Node):
    def __init__(self, node_to_call: Node, arg_nodes: list[Node]):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        super().__init__(self.node_to_call)

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[-1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

class ReturnNode(Node):
    def __init__(self, node_to_return: Node, pos_start: Position, pos_end: Position):
        self.node_to_return = node_to_return
        super().__init__(node_to_return, pos_start, pos_end)
class ContinueNode(Node):
    def __init__(self, pos_start: Position, pos_end: Position):
        super().__init__(pos_start=pos_start, pos_end=pos_end)
class BreakNode(Node):
    def __init__(self, pos_start: Position, pos_end: Position):
        super().__init__(pos_start=pos_start, pos_end=pos_end)
