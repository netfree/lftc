class LexicalError(RuntimeError):
    def __init__(self, line_number: int, message: str):
        self.args = (line_number, message)

    def get_line(self) -> int:
        return self.args[0]

    def get_additional_info(self) -> str:
        return self.args[1]
