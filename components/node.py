from .token import Token
from .utils.debug import DebugMessage


class Node:
    def __init__(self, tok: Token):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
        
        self.display = self.tok
        
        DebugMessage(f"Created {self}").display()

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.display}>"


class NumberNode(Node):
    def __init__(self, tok: Token):
        super().__init__(tok)
        
        
class StringNode(Node):
    def __init__(self, tok: Token):
        super().__init__(tok)
        

class VarAccessNode(Node):
    def __init__(self, var_name_tok: Token):
        self.var_name_tok = var_name_tok
        super().__init__(var_name_tok)


class VarAssignNode(Node):
    def __init__(self, var_name_tok: Token, value_node: Node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        super().__init__(var_name_tok)
        self.display = f"{self.var_name_tok}:{self.value_node}" 
        self.pos_end = self.value_node.pos_end


class BinOpNode(Node):
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        super().__init__(op_tok)
        self.display = f"({self.left_node}, {self.op_tok}, {self.right_node})" 
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

class UnaryOpNode(Node):
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        super().__init__(op_tok)
        self.display = f"({self.op_tok}, {self.node})" 
        self.pos_end = self.node.pos_end


class IfNode(Node):
    def __init__(self, cases: tuple[tuple[Token]], else_case):
        self.cases = cases
        self.else_case = else_case
        super().__init__(cases[0][0])
        self.pos_end = (else_case or self.cases[len(self.cases) - 1][0]).pos_end
        

class ForNode(Node):
    def __init__(self, var_name_tok: Token, start_value_node: Node, end_value_node: Node, step_value_node: Node, body_node: Node):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        super().__init__(var_name_tok)
        self.pos_end = self.body_node.pos_end
        

class WhileNode(Node):
    def __init__(self, condition_node: Node, body_node: Node):
        self.condition_node = condition_node
        self.body_node = body_node
        super().__init__(condition_node)
        self.pos_end = self.body_node.pos_end
        
        
class FuncDefNode(Node):
    def __init__(self, var_name_tok: Token, arg_name_toks: list[Token], body_node: Node):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        
        if self.var_name_tok:
            to_tok_base = self.var_name_tok
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
