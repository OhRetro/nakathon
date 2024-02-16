from enum import Enum
from .token import Token


class NodeType(Enum):
    # Data types
    Number = "Number"

    # Variables
    VarAccess = "VarAccess"
    VarAssign = "VarAssign"

    # Operations
    BinOp = "BinOp"
    UnaryOp = "UnaryOp"
    
    # Conditional
    If = "If"
    
    # Loops
    For = "For"
    While = "While"


class Node:
    def __init__(self, type_: NodeType, tok: Token):
        self.type = type_
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"<Node:{self.type.name}:{self.tok}>"


class NumberNode(Node):
    def __init__(self, tok: Token):
        super().__init__(NodeType.Number, tok)


class VarAccessNode(Node):
    def __init__(self, var_name_tok: Token):
        self.var_name_tok = var_name_tok
        super().__init__(NodeType.VarAccess, var_name_tok)


class VarAssignNode(Node):
    def __init__(self, var_name_tok: Token, value_node: Node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        super().__init__(NodeType.VarAssign, var_name_tok)
        self.pos_end = self.value_node.pos_end


class BinOpNode(Node):
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        super().__init__(NodeType.BinOp, op_tok)
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end


class UnaryOpNode(Node):
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        super().__init__(NodeType.UnaryOp, op_tok)
        self.pos_end = self.node.pos_end


class IfNode(Node):
    def __init__(self, cases: tuple[tuple[Token]], else_case):
        self.cases = cases
        self.else_case = else_case
        super().__init__(NodeType.If, cases[0][0])
        self.pos_end = (else_case or self.cases[len(self.cases) - 1][0]).pos_end
        

class ForNode(Node):
    def __init__(self, var_name_tok: Token, start_value_node: Node, end_value_node: Node, step_value_node: Node, body_node: Node):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        super().__init__(NodeType.For, var_name_tok)
        self.pos_end = self.body_node.pos_end
        

class WhileNode(Node):
    def __init__(self, condition_node: Node, body_node: Node):
        self.condition_node = condition_node
        self.body_node = body_node
        super().__init__(NodeType.While, condition_node)
        self.pos_end = self.body_node.pos_end
        