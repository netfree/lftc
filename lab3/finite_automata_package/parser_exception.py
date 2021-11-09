class ParserException(RuntimeError):
    def __init__(self, line_number: int, message: str):
        self.args = (line_number, message)

    def get_line_number(self) -> int:
        return self.args[0]

    def get_message(self) -> str:
        return self.args[1]
