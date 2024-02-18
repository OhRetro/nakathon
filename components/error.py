from .utils.strings_with_arrows import string_with_arrows
from .context import Context
from .position import Position 


class Error:
    def __init__(self, pos_start: Position, pos_end: Position, error_name: str, details: str):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name}: {self.details}\n"
        result += f"    File {self.pos_start.fn}, line {self.pos_start.ln + 1}"
        result += "\n\n" + \
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        return result

    def __repr__(self) -> str:
        return f"<Error:{self.error_name}:\"{self.details}\">"


# Happens at Lexer Process
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)


class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Expected Character", details)
        
        
# Happens at AST Process
class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)


# Happens at Interpreter Process
class RunTimeError(Error):
    def __init__(self, pos_start, pos_end, details, context: Context):
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}"
        result += "\n\n" + \
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ""
        pos: Position = self.pos_start
        ctx = self.context

        while ctx:
            result += f"     File {pos.fn}, line {pos.ln +
                                                  1}, in {ctx.display_name}\n\n"
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return "Traceback (most recent call last):\n" + result
