from src.Token import TokenType, Token
from src.ErrorReporter import ErrorReporter

class Lexer:
    def __init__(self, src: str, error_reporter: ErrorReporter):
        self.src = src;
        self.error_reporter = error_reporter;
        self.pos = 0;
        self.line = 1;
        self.column = 1;
        self.current_char = self.src[0] if self.src else None;
        self.current_file = "__main__";
        
        self.keywords = {
            'box': TokenType.BOX,
            'open': TokenType.OPEN,
            'asm': TokenType.ASM,
            'num16': TokenType.NUM16,
            'num24': TokenType.NUM24,
            'f16': TokenType.F16,
            'f24': TokenType.F24,
            'char': TokenType.CHAR,
            'void': TokenType.VOID,
            'namespace': TokenType.NAMESPACE,
            'ret': TokenType.RET,
        }
        
    def _error(self, message: str, suggestion: str = None):
        self.error_reporter.report(
            self.current_file, self.line, self.column,
            message, "LexerError", suggestion
        )
        
    def advance(self, count=1):
        for _ in range(count):
            if self.current_char == '\n':
                self.line += 1;
                self.column = 0;
            
            self.pos += 1;
            if self.pos > len(self.src) - 1:
                self.current_char = None;
            else:
                self.current_char = self.src[self.pos];
                self.column += 1;
                
    def peek_char(self, offset=1):
        peek_pos = self.pos + offset;
        if peek_pos > len(self.src) - 1:
            return None;
        return self.src[peek_pos];
                
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance();
    
    def skip_comment(self):
        if self.current_char == '#':
            while self.current_char is not None and self.current_char != '\n':
                self.advance();
                
    def create_token(self, type: TokenType, lexeme: str, line: int=None, column: int=None, file: str=None) -> Token:
        line = self.line if line is None else line;
        column = self.column if column is None else column;
        file = self.current_file if file is None else file;
        
        return Token(type, lexeme, line, column, file);
    
    def process_file_directive(self):
        self.advance(5)
        self.skip_whitespace()
        filename = self.parse_string_lit();
        self.current_file = filename
        
    def parse_string_lit(self):
        curr_str = '';
        self.advance();  # skip "
        
        while self.current_char is not None and self.current_char != '"':
            curr_str += self.current_char;
            self.advance();
                
        self.advance(); # skip "
        return curr_str;
    
    def parse_ident(self):
        start_line = self.line;
        start_column = self.column;
        result = '';
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char;
            self.advance();
        
        token_type = self.keywords.get(result, TokenType.IDENT);
        return self.create_token(token_type, result, start_line, start_column);
    
    def parse_char_lit(self):
        start_line, start_col = self.line, self.column
        self.advance() # skip '
        
        if self.current_char is None: 
            self.error_reporter.report(self.current_file, start_line, start_col, "unterminated character literal")
            return None
        
        if self.current_char == '\\':
            self.advance() # skip \
            if self.current_char is None:
                raise Exception("Unterminated char literal")
                
            escape_char = self.current_char
            if escape_char == 'n':
                char_value = ord('\n')
            elif escape_char == 't':
                char_value = ord('\t')
            elif escape_char == 'r':
                char_value = ord('\r')
            elif escape_char == '0':
                char_value = 0
            elif escape_char == '\\':
                char_value = ord('\\')
            elif escape_char == "'":
                char_value = ord("'")
            elif escape_char == '"':
                char_value = ord('"')
            elif escape_char == 'x':
                self.advance() # skip x
                if self.current_char is None:
                    raise Exception("Invalid hex escape sequence in char literal")
                h1 = self.current_char
                self.advance()
                if self.current_char is None:
                    raise Exception("Invalid hex escape sequence in char literal")
                h2 = self.current_char
                try:
                    char_value = int(h1 + h2, 16)
                except ValueError:
                    raise Exception(f"Invalid hex escape sequence: \\x{h1}{h2}")
            else:
                char_value = ord(escape_char)
            
            self.advance()
        else:
            char_value = ord(self.current_char)
            self.advance()
        
        if self.current_char != "'": 
            self._error("unterminated character literal", "Add a closing single quote (')")
            return None
        
        self.advance() # skip '
        return self.create_token(TokenType.CHAR_LIT, char_value)
    
    def parse_number(self):
        result = ''

        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
            
        return self.create_token(TokenType.INT_LIT, int(result))
    
    def hex_or_binary_number(self):
        start_col = self.column
        line = self.line
        
        self.advance()
        
        base = 10
        allowed_chars = "0123456789"
        
        if self.current_char in 'xX':
            base = 16
            allowed_chars = "0123456789abcdefABCDEF"
            self.advance()
        elif self.current_char in 'bB':
            base = 2
            allowed_chars = "01"
            self.advance()
        
        result_str = ''
        while self.current_char is not None and self.current_char in allowed_chars:
            result_str += self.current_char
            self.advance()
            
        if not result_str:
            return Token(TokenType.INT_LIT, 0, line, start_col)

        value = int(result_str, base)
        return self.create_token(TokenType.INT_LIT, value)
        
    def tokenize(self) -> list[Token]:
        tokens = [];
        while self.current_char is not None:
            if (self.src[self.pos:].startswith('$file')):
                self.process_file_directive();
                continue;

            if self.current_char.isspace():
                self.skip_whitespace();
                continue;
            if self.current_char == '#':
                self.skip_comment();
                continue;
            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.parse_ident());
                continue;
            if self.current_char == '"':
                tokens.append(self.create_token(TokenType.STR_LIT, self.parse_string_lit()));
                continue;
            if self.current_char == "'":
                tokens.append(self.parse_char_lit());
                continue;
            if self.current_char == '0' and self.peek_char() in 'xXbB':
                tokens.append(self.hex_or_binary_number())
                continue
            if self.current_char.isdigit():
                tokens.append(self.parse_number())
                continue
            
            char = self.current_char
            peek = self.peek_char()
            
            if (char == ':') and (peek == ':'):
                tokens.append(self.create_token(TokenType.COLON_D, '::'));
                self.advance(2); continue;
            if (char == '-') and (peek == '>'):
                tokens.append(self.create_token(TokenType.ARROW, '->'));
                self.advance(2); continue;
            
            symbol_map = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.STAR,
                '/': TokenType.SLASH,
                '[': TokenType.OPEN_BRACKET,
                ']': TokenType.CLOSE_BRACKET,
                '(': TokenType.OPEN_PAREN,
                ')': TokenType.CLOSE_PAREN,
                '<': TokenType.LESS_THAN,
                '>': TokenType.GREATHER_THAN,
                ':': TokenType.COLON,
                ';': TokenType.SEMICOLON,
                '&': TokenType.AMPERSAND,
                ',': TokenType.COMMA,
            }
            
            if char in symbol_map:
                tokens.append(self.create_token(symbol_map[char], char))
                self.advance()
                continue;
            
            self._error(f"unknown character '{self.current_char}'")
            self.advance()
        
        tokens.append(self.create_token(TokenType.EOF, ""));
        return tokens;