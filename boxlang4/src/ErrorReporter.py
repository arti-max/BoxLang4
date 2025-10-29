import sys

class ErrorReporter:
    def __init__(self):
        self._errors = []
        self._had_error = False
        self._source_lines = {} 

    def load_source_file(self, filename: str, lines: list[str]):
        self._source_lines[filename] = lines

    def report(self, file: str, line: int, column: int, message: str, error_type: str = "SyntaxError", suggestion: str = None):
        full_message = self._format_error(file, line, column, message, error_type, suggestion)
        print(full_message, file=sys.stderr)
        
        self._errors.append(full_message)
        self._had_error = True

    def _format_error(self, file: str, line: int, column: int, message: str, error_type: str, suggestion: str) -> str:
        corrected_line = line - 1
        
        header = f"error[{error_type}]: {message}\n"
        location = f"  --> {file}:{corrected_line}:{column}\n"
        
        
        line_content = ""
        if file in self._source_lines and 1 <= corrected_line <= len(self._source_lines[file]):
            line_idx = corrected_line - 1
            line_content = self._source_lines[file][line_idx].rstrip()

            line_padding = " " * (len(str(corrected_line)) + 1)
            code_line = f"{corrected_line} | {line_content}\n"
            
            pointer_padding = " " * (column - 1)
            pointer_line = f"{line_padding}| {pointer_padding}^\n"
            
            context = code_line + pointer_line
        else:
            context = ""

        suggestion_text = ""
        if suggestion:
            suggestion_text = f"  = help: {suggestion}\n"

        return f"\n{header}{location}{context}{suggestion_text}"

    def had_error(self) -> bool:
        return self._had_error

    def clear(self):
        self._errors = []
        self._had_error = False
        self._source_lines = {}
