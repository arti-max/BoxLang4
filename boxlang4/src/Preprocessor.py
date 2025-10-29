from src.ErrorReporter import ErrorReporter

class Preprocessor:
    def __init__(self, error_reporter: ErrorReporter):
        self.error_reporter = error_reporter
        self.defines = {};
        self.out = "";
        self.skip_stack = [False]
        
    def process(self, lines: list[str], filename: str):
        if not self.skip_stack[-1]:
            self.out += f'$file "{filename}"\n'
        
        original_filename = filename    
        
        for line_number, line in enumerate(lines, 1):
            stripped_line = line.strip()
            
            if stripped_line.startswith("$"):
                directive_line = stripped_line[1:]

                if directive_line.startswith("ifndef"):
                    name = directive_line.split(' ', 1)[1]
                    if self.skip_stack[-1]:
                        self.skip_stack.append(True)
                    else:
                        self.skip_stack.append(name in self.defines)
                    continue

                elif directive_line.startswith("ifdef"):
                    name = directive_line.split(' ', 1)[1]
                    if self.skip_stack[-1]:
                        self.skip_stack.append(True)
                    else:
                        self.skip_stack.append(name not in self.defines)
                    continue

                elif directive_line.startswith("else"):
                    if len(self.skip_stack) > 1 and not self.skip_stack[-2]:
                        self.skip_stack[-1] = not self.skip_stack[-1]
                    continue

                elif directive_line.startswith("endif"):
                    if len(self.skip_stack) > 1:
                        self.skip_stack.pop()
                    continue

            if self.skip_stack[-1]:
                continue

            if stripped_line.startswith("$"):
                directive_line = stripped_line[1:]

                if directive_line.startswith("include"):
                    include_filename = ""
                    column = line.find(directive_line) + 1
                    
                    try:
                        if '<' in directive_line:
                            start = directive_line.find('<') + 1
                            end = directive_line.find('>')
                            path = directive_line[start:end]
                            include_filename = "boxlang4/lib/" + path
                            column += start
                        else:
                            start = directive_line.find('"') + 1
                            end = directive_line.rfind('"')
                            path = directive_line[start:end]
                            include_filename = path
                            column += start

                        if not path:
                            raise ValueError("Empty include path")

                    except (ValueError, IndexError):
                        self.error_reporter.report(
                            original_filename, line_number, column,
                            "invalid include directive",
                            "PreprocessorError",
                            "Usage: $include <path> or $include \"path\""
                        )
                        continue

                    try:
                        with open(include_filename, "r", encoding="utf-8") as f:
                            included_lines = f.readlines()
                            self.error_reporter.load_source_file(include_filename, included_lines)
                            self.process(included_lines, include_filename)
                            self.out += f'$file "{original_filename}"\n'
                    except FileNotFoundError:
                        self.error_reporter.report(
                            original_filename,
                            line_number,
                            column,
                            f"file '{include_filename}' not found",
                            "PreprocessorError",
                            "Check if the file exists and the path is correct."
                        )
                    continue

                elif directive_line.startswith("define"):
                    parts = directive_line.split(' ', 2)
                    if len(parts) >= 2:
                        name = parts[1]
                        value = parts[2] if len(parts) > 2 else "1"
                        self.defines[name] = value
                    continue
            else:
                self.out += line 
        
        return self.out