from enum import Enum, auto

class TokenType(Enum):
    BOX             = auto()    # box
    OPEN            = auto()    # open
    ASM             = auto()    # asm
    SHELF           = auto()    # shelf
    NAMESPACE       = auto()    # namespace
    RET             = auto()    # ret
    
    
    # data type
    NUM16           = auto()    # num16
    NUM24           = auto()    # num24
    CHAR            = auto()    # char
    F16             = auto()    # f16
    F24             = auto()    # f24
    VOID            = auto()    # void
    
    
    # arythmetic
    PLUS            = auto()    # +
    MINUS           = auto()    # -
    STAR            = auto()    # *
    SLASH           = auto()    # /
    
    # literals
    IDENT           = auto()    # my_variable
    INT_LIT         = auto()    # 123
    FLOAT_LIT       = auto()    # 123.45
    STR_LIT         = auto()    # "abc"
    CHAR_LIT        = auto()    # 'c'
    
    # other
    ARROW           = auto()    # ->
    DOT             = auto()    # .
    COLON_D         = auto()    # ::
    COLON           = auto()    # :
    SEMICOLON       = auto()    # ;
    OPEN_PAREN      = auto()    # (
    CLOSE_PAREN     = auto()    # )
    OPEN_BRACKET    = auto()    # [
    CLOSE_BRACKET   = auto()    # ]
    COMMA           = auto()    # ,
    LESS_THAN       = auto()    # <
    GREATHER_THAN   = auto()    # >
    OPEN_BRACE      = auto()    # {
    CLOSE_BRACE     = auto()    # }
    AMPERSAND       = auto()    # &
    
    UNKNOWN         = auto()    # UNK
    EOF             = auto()    # End Of File
    
    
class Token:
    def __init__(self, type: TokenType, lexeme: str, line: int, column: int, file: str):
        self.type = type;
        self.lexeme = lexeme;
        self.line = line;
        self.column = column;
        self.file = file;
    
    def __repr__(self):
        return f"[TOKEN] {self.type} : {self.lexeme} : {self.line} : {self.column} : {self.file}\n";